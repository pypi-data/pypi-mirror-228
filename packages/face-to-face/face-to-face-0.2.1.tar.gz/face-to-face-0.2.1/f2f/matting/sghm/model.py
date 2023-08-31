"""
Code adapted from:
    https://github.com/cxgincsu/SemanticGuidedHumanMatting
"""
import os
from pathlib import Path
from types import MethodType
from typing import Any, Optional, Sequence, Tuple

import cv2
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor
from torchvision.models import ResNet, resnet50
from torchvision.models.segmentation.deeplabv3 import ASPP

from f2f.utils import get_onnx_cache_dir
from f2f.utils.onnx_ops import OnnxExport

CHECKPOINT_PATH = (
    Path(__file__).parents[2] / "assets" / "matting" / "SGHM-ResNet50.pth"
)


@OnnxExport()
def onnx_export() -> None:
    model = SemanticGuidedHumanMattingInference()
    input = torch.randn(1, 3, 1280, 1280)
    print(f"Exporting {model._get_name()} ONNX...")
    print(f"Use Input: {input.size()}")
    torch.onnx.export(
        model,
        input,
        str(Path(get_onnx_cache_dir()) / "SGHM-ResNet50.onnx"),
        opset_version=13,
        input_names=["input"],
        output_names=["alpha", "segmentation"],
        dynamic_axes={
            "input": {0: "batch_size"},
            "alpha": {0: "batch_size"},
            "segmentation": {0: "batch_size"},
        },
    )


class SemanticGuidedHumanMattingInference(nn.Module):
    kenel_7: Tensor
    kenel_15: Tensor
    resolution: int = 1280

    def __init__(self):
        super().__init__()
        self.model = SemanticGuidedHumanMatting(
            seg_threshold=0.8, checkpoint=str(CHECKPOINT_PATH)
        ).eval()
        self.model.requires_grad_(False)

        kernel_7 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
        kernel_15 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
        self.register_buffer(
            "kernel_7", torch.from_numpy(kernel_7).float()[None, None]
        )
        self.register_buffer(
            "kernel_15", torch.from_numpy(kernel_15).float()[None, None]
        )

    def train(self, mode: bool = True) -> None:
        return super().train(False)

    @torch.no_grad()
    def forward(self, input: Tensor) -> Tuple[Tensor, Tensor]:
        """
        Args:
            input: (B, 3, 1280, 1280), RGB image in range [-1, 1]
        Returns:
            alpha: (B, 1, 1280, 1280), alpha matte in range [0, 1]
            segmentation: (B, 1, 1280, 1280), segmentation mask in range [0, 1], not binary
        """
        outputs = self.model(input * 0.5 + 0.5)
        alpha_os8, alpha_os4, alpha_os1, segmentation = outputs

        # progressive refine alpha
        alpha = alpha_os8.clone()
        uncertain_8 = torch.zeros_like(alpha)
        uncertain_8[abs(alpha - 0.5) < 127.0 / 255.0] = 1.0
        uncertain_8 = F.conv2d(uncertain_8, self.kernel_15, padding=7).clamp(
            0, 1
        )
        alpha[uncertain_8 > 0] = alpha_os4[uncertain_8 > 0]

        uncertain_4 = torch.zeros_like(alpha)
        uncertain_4[abs(alpha - 0.5) < 127.0 / 255.0] = 1.0
        uncertain_4 = F.conv2d(uncertain_4, self.kernel_7, padding=3).clamp(
            0, 1
        )
        alpha[uncertain_4 > 0] = alpha_os1[uncertain_4 > 0]
        return alpha, segmentation


def resnet50_backbone(*args: Any, **kwargs: Any) -> ResNet:
    model = resnet50(*args, **kwargs)
    del model.avgpool
    del model.fc

    def _forward_impl(
        self: ResNet, x: Tensor
    ) -> Tuple[Tensor, Tensor, Tensor, Tensor, Tensor]:
        # See note [TorchScript super()]
        x0 = x  # 1/1

        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x1 = x  # 1/2

        x = self.maxpool(x)
        x = self.layer1(x)
        x2 = x  # 1/4

        x = self.layer2(x)
        x3 = x  # 1/8

        x = self.layer3(x)
        x = self.layer4(x)
        x4 = x  # 1/16

        return x4, x3, x2, x1, x0

    model._forward_impl = MethodType(_forward_impl, model)
    return model


class SemanticGuidedHumanMatting(nn.Module):
    def __init__(
        self, seg_threshold: float = 0.5, checkpoint: Optional[str] = None
    ) -> None:
        super().__init__()
        self.seg_threshold = seg_threshold
        self.backbone = resnet50_backbone(
            replace_stride_with_dilation=[False, False, True]
        )
        self.aspp = ASPP(2048, [3, 6, 9])
        self.decoder = Decoder(
            channels=[256, 128, 64, 48, 32 + 1 + 1],
            feature_channels=[512, 256, 64, 3],
        )

        self.shortcut_inplane = [3 + 1, 3 + 1, 64 + 1, 256 + 1, 512 + 1]
        self.shortcut_plane = [32, 32, 32, 64, 128]
        self.shortcut = nn.ModuleList()
        for stage, inplane in enumerate(self.shortcut_inplane):
            self.shortcut.append(
                self._make_shortcut(inplane, self.shortcut_plane[stage])
            )

        self.refine = MattingRefiner()

        if checkpoint is not None:
            self.load(checkpoint)

    def _make_shortcut(self, inplane, planes):
        """
        Construct Attentive Shortcut Module
        """
        conv_1 = nn.Conv2d(
            inplane, planes, kernel_size=3, padding=1, bias=False
        )
        conv_2 = nn.Conv2d(planes, planes, kernel_size=3, padding=1, bias=False)
        nn.utils.spectral_norm(conv_1)
        nn.utils.spectral_norm(conv_2)
        return nn.Sequential(
            conv_1,
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(planes),
            conv_2,
            nn.ReLU(inplace=True),
            nn.BatchNorm2d(planes),
            ECALayer(),
        )

    def forward(
        self, image: Tensor, guide_segmentation: Optional[Tensor] = None
    ) -> Tuple[Tensor, Tensor, Tensor, Tensor]:
        """
        image: (B, 3, 1280, 1280) RGB image in range [0, 1]
        guide_segmentation: (B, 1, 1280, 1280) segmentation mask in range [0, 1]
        """
        image_quarter = F.interpolate(
            image,
            scale_factor=1.0 / 4,
            mode="bilinear",
            align_corners=False,
            recompute_scale_factor=True,
        )
        x4, x3, x2, x1, x0 = self.backbone(
            image_quarter
        )  # 1/64, 1/32, 1/16, 1/8, 1/4
        x4 = self.aspp(x4)  # 1/64

        if guide_segmentation is None:
            pred_seg: Tensor = self.decoder(x4, x3, x2, x1, x0)
            pred_seg = torch.sigmoid(pred_seg[:, :1])
            guide_segmentation = F.interpolate(
                pred_seg,
                scale_factor=4.0,
                mode="bilinear",
                align_corners=False,
                recompute_scale_factor=True,
            )
        # not eval mode, use threshold 0.5
        if self.training:
            threshold = 0.5
        else:
            threshold = self.seg_threshold
        mask = guide_segmentation.gt(threshold).type(guide_segmentation.dtype)
        mask_quarter = F.interpolate(
            mask,
            scale_factor=0.25,
            mode="bilinear",
            align_corners=False,
            recompute_scale_factor=True,
        )

        # Sharing features
        m = mask
        x = torch.cat((image, m), dim=1)
        mid_fea = self.shortcut[0](x)  # 1/1

        m0 = mask_quarter
        x0 = torch.cat((x0, m0), dim=1)
        mid_fea0 = self.shortcut[1](x0)  # 1/4

        m1 = F.interpolate(
            m0, scale_factor=1.0 / 2, mode="bilinear", align_corners=False
        )
        x1 = torch.cat((x1, m1), dim=1)
        mid_fea1 = self.shortcut[2](x1)  # 1/8

        m2 = F.interpolate(
            m0, scale_factor=1.0 / 4, mode="bilinear", align_corners=False
        )
        x2 = torch.cat((x2, m2), dim=1)
        mid_fea2 = self.shortcut[3](x2)  # 1/16

        m3 = F.interpolate(
            m0, scale_factor=1.0 / 8, mode="bilinear", align_corners=False
        )
        x3 = torch.cat((x3, m3), dim=1)
        mid_fea3 = self.shortcut[4](x3)  # 1/32

        # Matting decoder
        x_os8, x_os4, x_os1 = self.refine(
            x4, mid_fea3, mid_fea2, mid_fea1, mid_fea0, mid_fea
        )
        return x_os8, x_os4, x_os1, guide_segmentation

    def load(self, checkpoint: str) -> None:
        """
        Load pretrained weights
        """
        if not os.path.exists(checkpoint):
            raise FileNotFoundError(f"{checkpoint} not found")
        refine_state_dict = dict()
        state_dict = torch.load(checkpoint, map_location="cpu")
        for k, v in state_dict.items():
            k = k.replace("module.", "")
            k = k.replace("_bar", "_orig")
            refine_state_dict[k] = v
        self.load_state_dict(refine_state_dict)
        print(f"{self._get_name()} Loaded weights from {checkpoint}")


class ECALayer(nn.Module):
    """Constructs a ECA module.
    Args:
        channel: Number of channels of the input feature map
        k_size: Adaptive selection of kernel size
    """

    def __init__(self, kernel_size: int = 3) -> None:
        super().__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.conv = nn.Conv1d(
            1,
            1,
            kernel_size=kernel_size,
            padding=(kernel_size - 1) // 2,
            bias=False,
        )
        self.sigmoid = nn.Sigmoid()

    def forward(self, x: Tensor) -> Tensor:
        # feature descriptor on the global spatial information
        y: Tensor = self.avg_pool(x)

        # Two different branches of ECA module
        y = (
            self.conv(y.squeeze(-1).transpose(-1, -2))
            .transpose(-1, -2)
            .unsqueeze(-1)
        )

        # Multi-scale information fusion
        y = self.sigmoid(y)

        return x * y.expand_as(x)


class Decoder(nn.Module):
    """
    Decoder upsamples the image by combining the feature maps at all resolutions from the encoder.

    Input:
        x4: (B, C, H/16, W/16) feature map at 1/16 resolution.
        x3: (B, C, H/8, W/8) feature map at 1/8 resolution.
        x2: (B, C, H/4, W/4) feature map at 1/4 resolution.
        x1: (B, C, H/2, W/2) feature map at 1/2 resolution.
        x0: (B, C, H, W) feature map at full resolution.

    Output:
        x: (B, C, H, W) upsampled output at full resolution.
    """

    def __init__(
        self, channels: Sequence[int], feature_channels: Sequence[int]
    ) -> None:
        super().__init__()
        self.conv1 = nn.Conv2d(
            feature_channels[0] + channels[0],
            channels[1],
            3,
            padding=1,
            bias=False,
        )
        self.bn1 = nn.BatchNorm2d(channels[1])
        self.conv2 = nn.Conv2d(
            feature_channels[1] + channels[1],
            channels[2],
            3,
            padding=1,
            bias=False,
        )
        self.bn2 = nn.BatchNorm2d(channels[2])
        self.conv3 = nn.Conv2d(
            feature_channels[2] + channels[2],
            channels[3],
            3,
            padding=1,
            bias=False,
        )
        self.bn3 = nn.BatchNorm2d(channels[3])
        self.conv4 = nn.Conv2d(
            feature_channels[3] + channels[3], channels[4], 3, padding=1
        )
        self.relu = nn.ReLU(True)

    def forward(
        self, x4: Tensor, x3: Tensor, x2: Tensor, x1: Tensor, x0: Tensor
    ) -> Tensor:
        x = F.interpolate(
            x4, size=x3.shape[2:], mode="bilinear", align_corners=False
        )
        x = torch.cat([x, x3], dim=1)
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = F.interpolate(
            x, size=x2.shape[2:], mode="bilinear", align_corners=False
        )
        x = torch.cat([x, x2], dim=1)
        x = self.conv2(x)
        x = self.bn2(x)
        x = self.relu(x)
        x = F.interpolate(
            x, size=x1.shape[2:], mode="bilinear", align_corners=False
        )
        x = torch.cat([x, x1], dim=1)
        x = self.conv3(x)
        x = self.bn3(x)
        x = self.relu(x)
        x = F.interpolate(
            x, size=x0.shape[2:], mode="bilinear", align_corners=False
        )
        x = torch.cat([x, x0], dim=1)
        x = self.conv4(x)
        return x


class BaseBlock(nn.Module):
    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        stride: int = 1,
        upsample: bool = False,
    ) -> None:
        super().__init__()
        if stride > 1:
            self.conv1 = nn.ConvTranspose2d(
                in_channels,
                in_channels,
                kernel_size=4,
                stride=stride,
                padding=1,
                bias=False,
            )
        else:
            self.conv1 = nn.Conv2d(
                in_channels,
                in_channels,
                kernel_size=3,
                stride=1,
                padding=1,
                bias=False,
            )
        nn.utils.spectral_norm(self.conv1, dim=0)
        self.bn1 = nn.BatchNorm2d(in_channels)
        self.activation = nn.LeakyReLU(0.2, inplace=True)
        self.conv2 = nn.Conv2d(
            in_channels,
            out_channels,
            kernel_size=3,
            stride=1,
            padding=1,
            bias=False,
        )
        nn.utils.spectral_norm(self.conv2)
        self.bn2 = nn.BatchNorm2d(out_channels)

        if not upsample:
            self.upsample = None
        else:
            upsample_conv = nn.Conv2d(
                in_channels, out_channels, kernel_size=1, stride=1, bias=False
            )
            nn.utils.spectral_norm(upsample_conv)
            self.upsample = nn.Sequential(
                nn.UpsamplingNearest2d(scale_factor=2),
                upsample_conv,
                nn.BatchNorm2d(out_channels),
            )

    def forward(self, input: Tensor) -> Tensor:
        output = self.conv1(input)
        output = self.bn1(output)
        output = self.activation(output)
        output = self.conv2(output)
        output = self.bn2(output)

        if self.upsample is not None:
            identity = self.upsample(input)
        else:
            identity = input
        output = self.activation(output + identity)
        return output


class MattingRefiner(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.ConvTranspose2d(
            32, 32, kernel_size=4, stride=2, padding=1, bias=False
        )
        nn.utils.spectral_norm(self.conv1, dim=0)
        self.bn1 = nn.BatchNorm2d(32)

        self.conv2 = nn.ConvTranspose2d(
            32, 32, kernel_size=3, stride=1, padding=1, bias=False
        )
        nn.utils.spectral_norm(self.conv2, dim=0)
        self.bn2 = nn.BatchNorm2d(32)

        self.leaky_relu = nn.LeakyReLU(0.2, inplace=True)

        self.layer2 = self._make_layer(256, 128, 3)
        self.layer3 = self._make_layer(128, 64, 3)
        self.layer4 = self._make_layer(64, 32, 2)
        self.layer5 = self._make_layer(32, 32, 2)
        self.layer6 = self._make_layer(32, 32, 2)

        self.refine_OS1 = nn.Sequential(
            nn.Conv2d(32, 32, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(32),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(32, 1, kernel_size=3, stride=1, padding=1),
        )

        self.refine_OS4 = nn.Sequential(
            nn.Conv2d(32, 32, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(32),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(32, 1, kernel_size=3, stride=1, padding=1),
        )

        self.refine_OS8 = nn.Sequential(
            nn.Conv2d(32, 32, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(32),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(32, 1, kernel_size=3, stride=1, padding=1),
        )

    def _make_layer(self, in_channels: int, out_channels: int, n_blocks: int):
        layers = []
        stride = 2
        for _ in range(n_blocks):
            layer = BaseBlock(
                in_channels, out_channels, stride=stride, upsample=stride == 2
            )
            in_channels = out_channels
            stride = 1
            layers.append(layer)
        return nn.Sequential(*layers)

    def forward(
        self,
        x4: Tensor,
        x3: Tensor,
        x2: Tensor,
        x1: Tensor,
        x0: Tensor,
        x00: Tensor,
    ) -> Tuple[Tensor, Tensor, Tensor]:
        # 1/64, 1/32, 1/16, 1/8, 1/4, 1/1
        x = self.layer2(x4) + x3  # 1/32
        x = self.layer3(x) + x2  # 1/16
        x = self.layer4(x) + x1  # 1/8
        x_os8 = self.refine_OS8(x)

        x = self.layer5(x) + x0  # 1/4
        x_os4 = self.refine_OS4(x)

        x = self.layer6(x)  # 1/2

        x = self.conv1(x)  # 1/1
        x = self.bn1(x)
        x = self.leaky_relu(x)

        x = x + x00
        x = self.conv2(x)  # 1/1
        x = self.bn2(x)
        x = self.leaky_relu(x)
        x_os1 = self.refine_OS1(x)

        x_os4 = F.interpolate(
            x_os4, scale_factor=4.0, mode="bilinear", align_corners=False
        )
        x_os8 = F.interpolate(
            x_os8, scale_factor=8.0, mode="bilinear", align_corners=False
        )

        x_os1 = (torch.tanh(x_os1) + 1.0) / 2.0
        x_os4 = (torch.tanh(x_os4) + 1.0) / 2.0
        x_os8 = (torch.tanh(x_os8) + 1.0) / 2.0
        return x_os8, x_os4, x_os1
