from collections import defaultdict
from pathlib import Path
from typing import Dict, Optional

import torch
from torch import Tensor

from f2f.deca.deca import DECA, ResNetEncoder
from f2f.utils.onnx_ops import OnnxExport

CHECKPOINT_PATH = (
    Path(__file__).parents[1] / "assets" / "deca" / "EMOCA_v2_lr_mse_20.ckpt"
)


@OnnxExport()
def onnx_export():
    model = EMOCA(
        use_detail=False, use_diffuse=False, checkpoint=str(CHECKPOINT_PATH)
    ).eval()
    input = torch.randn(1, 3, model.resolution, model.resolution)
    print(f"Exporting {model._get_name()} ONNX...")
    print(f"Use Input: {input.size()}")
    output_names = list(model.flame_features.keys())
    torch.onnx.export(
        model,
        input,
        str(CHECKPOINT_PATH.parent / "EMOCA_v2_lr_mse_20.onnx"),
        opset_version=13,
        input_names=["input"],
        output_names=output_names,
        dynamic_axes={
            "input": {0: "batch_size"},
            **{k: {0: "batch_size"} for k in output_names},
        },
    )


class EMOCA(DECA):
    def __init__(
        self,
        use_detail: bool = True,
        use_diffuse: bool = False,
        checkpoint: Optional[str] = None,
    ) -> None:
        super().__init__(
            use_detail=use_detail,
            use_diffuse=use_diffuse,
            checkpoint=None,
        )
        self.E_expression = ResNetEncoder(50)
        if checkpoint is not None:
            self.load(checkpoint)

    def load(self, checkpoint: str) -> None:
        state_dict = torch.load(checkpoint, map_location="cpu")["state_dict"]
        refine_state_dict = defaultdict(dict)

        for key, val in state_dict.items():
            key = key.replace("deca.", "")
            module_key = key.split(".")[0]
            if module_key not in {
                "E_flame",
                "E_detail",
                "E_expression",
                "D_detail",
            }:
                continue
            refine_state_dict[module_key][
                key.replace(f"{module_key}.", "")
            ] = val

        self.E_flame.load_state_dict(refine_state_dict["E_flame"])
        self.E_expression.load_state_dict(refine_state_dict["E_expression"])
        if self.use_detail:
            self.E_detail.load_state_dict(refine_state_dict["E_detail"])
            self.D_detail.load_state_dict(refine_state_dict["D_detail"])
        print(f"{self._get_name()} Loaded weights from {checkpoint}")

    def encode_flame(self, input: Tensor) -> Dict[str, Tensor]:
        coeffs = super().encode_flame(input)
        exp_coeffs = self.E_expression(input)
        coeffs["expression"] = exp_coeffs
        return coeffs


class EMICA(EMOCA):
    def __init__(self) -> None:
        super().__init__()
