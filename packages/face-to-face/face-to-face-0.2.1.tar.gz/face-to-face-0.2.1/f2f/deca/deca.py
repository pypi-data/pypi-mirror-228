import os
from pathlib import Path
from types import MethodType
from typing import Dict, Optional, Tuple

import torch
import torch.nn as nn
from torch import Tensor
from torchvision.models import ResNet, resnet50

from f2f.deca.renderer import Renderer
from f2f.flame import FLAME, FLAMETexture
from f2f.utils.onnx_ops import OnnxExport

CHECKPOINT_PATH = (
    Path(__file__).parents[1] / "assets" / "deca" / "deca_model.tar"
)


@OnnxExport()
def onnx_export():
    # export flame encoder only
    model = DECA(
        use_detail=False, use_diffuse=False, checkpoint=str(CHECKPOINT_PATH)
    ).eval()
    input = torch.randn(1, 3, model.resolution, model.resolution)
    print(f"Exporting {model._get_name()} ONNX...")
    print(f"Use Input: {input.size()}")
    output_names = list(model.flame_features.keys())
    torch.onnx.export(
        model,
        input,
        str(CHECKPOINT_PATH.parent / "deca_encoder_flame.onnx"),
        opset_version=13,
        input_names=["input"],
        output_names=output_names,
        dynamic_axes={
            "input": {0: "batch_size"},
            **{k: {0: "batch_size"} for k in output_names},
        },
    )


class DECA(nn.Module):
    resolution: int = 224

    def __init__(
        self,
        use_detail: bool = True,
        use_diffuse: bool = False,
        checkpoint: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.use_detail = use_detail
        self.use_diffuse = use_diffuse
        self.flame_features: Dict[str, Tuple[int, int]] = {
            "identity": (0, 100),  # n_shape 100
            "texture": (100, 150),  # n_tex 50
            "expression": (150, 200),  # n_exp 50
            "neck_rotation": (200, 203),  # n_pose[:3] 3
            "jaw_rotation": (203, 206),  # n_pose[3:6] 3
            "global_rotation": (206, 209),  # n_cam 3
            "light": (209, 236),  # n_light 27
        }
        n_flame_features = max(self.flame_features.values())[-1]
        self.E_flame = ResNetEncoder(n_flame_features)
        if self.use_detail:
            self.E_detail = ResNetEncoder(128)
            # detail displacement map generator, not vertex displacement
            self.D_detail = Generator(latent_dim=512)
        else:
            self.E_detail = None
            self.D_detail = None
        self.flame = FLAME()

        if self.use_diffuse:
            self.renderer = Renderer()
            self.flame_tex = FLAMETexture()
        else:
            self.flame_tex = None

        if checkpoint is not None:
            self.load(checkpoint)

    def load(self, checkpoint: str) -> None:
        if not os.path.exists(checkpoint):
            raise FileNotFoundError(f"{checkpoint} does not exist.")
        state_dict = torch.load(checkpoint, map_location="cpu")
        self.E_flame.load_state_dict(state_dict["E_flame"])
        if self.use_detail:
            self.E_detail.load_state_dict(state_dict["E_detail"])
            self.D_detail.load_state_dict(state_dict["D_detail"])
        print(f"{self._get_name()} Loaded weights from {checkpoint}")

    def forward(
        self, input: Tensor, use_detail: bool = False, use_diffuse: bool = False
    ) -> Dict[str, Optional[Tensor]]:
        outputs = dict()
        flame_coeffs = self.encode_flame(input)
        outputs.update(flame_coeffs)
        if not self.use_detail and not self.use_diffuse:
            return outputs

        vertices, dynamic_lm17, static_lm68 = self.flame(
            identity_params=flame_coeffs["identity"],
            expression_params=flame_coeffs["expression"],
            global_rotation=flame_coeffs["global_rotation"],
            neck_rotation=flame_coeffs["neck_rotation"],
            jaw_rotation=flame_coeffs["jaw_rotation"],
            eyes_rotation=None,
        )
        if self.use_diffuse and use_diffuse:
            raise NotImplementedError()

            diffuse_dict = self.flame_tex(
                flame_coeffs["texture"],
            )
            diffuse_map = self.renderer(**diffuse_dict)
        if self.use_detail and use_detail:
            raise NotImplementedError()

            detail_code = self.E_detail(input)
            displacement_map = self.decode(flame_coeffs, detail_code)
        return outputs

    def encode_flame(self, input: Tensor) -> Dict[str, Tensor]:
        coeffs = self.E_flame(input)
        return self.decompose_flame_coeffs(coeffs)

    def decompose_flame_coeffs(self, input: Tensor) -> Dict[str, Tensor]:
        """
        Decompose the input coefficients into the flame parameters.
        """
        parameters = dict()
        start = 0
        for name, (start, end) in self.flame_features.items():
            parameters[name] = input[:, start:end]
            start = end
        return parameters

    def decode(self, flame_coeffs: Tensor, detail_code: Tensor) -> Tensor:
        raise NotImplementedError()


def resnet50_backbone() -> ResNet:
    model = resnet50()
    del model.fc

    def _forward_impl(self: ResNet, x: Tensor) -> Tensor:
        # See note [TorchScript super()]
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)

        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)

        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        # x = self.fc(x)

        return x

    model._forward_impl = MethodType(_forward_impl, model)
    return model


class ResNetEncoder(nn.Module):
    def __init__(self, out_features: int) -> None:
        super().__init__()
        self.encoder = resnet50_backbone().eval()
        self.resnet_feature_size = 2048
        self.layers = nn.Sequential(
            nn.Linear(self.resnet_feature_size, 1024),
            nn.ReLU(),
            nn.Linear(1024, out_features),
        )

    def features(self, input: Tensor) -> Tensor:
        return self.encoder(input)

    def forward(self, input: Tensor) -> Tensor:
        features = self.features(input)
        return self.layers(features)


class Reshape(nn.Module):
    def __init__(self, *shape: int) -> None:
        super().__init__()
        self.shape = shape

    def forward(self, input: Tensor) -> Tensor:
        return input.view(-1, *self.shape).contiguous()


class Generator(nn.Module):
    def __init__(self, latent_dim: int = 100, out_channels: int = 1) -> None:
        super().__init__()
        self.initial_resolution = 8
        sample_mode = "bilinear"
        self.layers = nn.Sequential(
            nn.Linear(latent_dim, 128 * self.initial_resolution**2),  # 8192
            Reshape(128, self.initial_resolution, self.initial_resolution),
            nn.BatchNorm2d(128),
            nn.Upsample(scale_factor=2, mode=sample_mode),  # 16
            nn.Conv2d(128, 128, 3, stride=1, padding=1),
            nn.BatchNorm2d(128, 0.8),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Upsample(scale_factor=2, mode=sample_mode),  # 32
            nn.Conv2d(128, 64, 3, stride=1, padding=1),
            nn.BatchNorm2d(64, 0.8),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Upsample(scale_factor=2, mode=sample_mode),  # 64
            nn.Conv2d(64, 64, 3, stride=1, padding=1),
            nn.BatchNorm2d(64, 0.8),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Upsample(scale_factor=2, mode=sample_mode),  # 128
            nn.Conv2d(64, 32, 3, stride=1, padding=1),
            nn.BatchNorm2d(32, 0.8),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Upsample(scale_factor=2, mode=sample_mode),  # 256
            nn.Conv2d(32, 16, 3, stride=1, padding=1),
            nn.BatchNorm2d(16, 0.8),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(16, out_channels, 3, stride=1, padding=1),
            nn.Tanh(),
        )

    def forward(self, input: Tensor) -> Tensor:
        return self.layers(input)
