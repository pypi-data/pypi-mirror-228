from pathlib import Path
from typing import Dict, Union

import numpy as np
from numpy import ndarray
from PIL import Image

from f2f.core.onnx import BaseONNX
from f2f.landmark.synthetic.onnx import FDSyntheticLM2dONNX

ONNX_PATH = (
    Path(__file__).parents[1] / "assets" / "deca" / "EMOCA_v2_lr_mse_20.onnx"
)


class EMOCAONNX(BaseONNX):
    resolution: int = 224

    def __init__(self, device: Union[str, int] = "cpu"):
        self.FDLM = FDSyntheticLM2dONNX(
            detection_model="scrfd",
            device=device,
        )
        super().__init__(str(ONNX_PATH), device)

    def to(self, device: Union[str, int]) -> "EMOCAONNX":
        super().to(device)
        self.FDLM.to(device)
        return self

    def __call__(
        self, input: Union[ndarray, Image.Image]
    ) -> Dict[str, ndarray]:
        """
        Args:
            input: (H, W, 3), RGB image in range [0, 255] or PIL.Image
        Returns:
            outputs: dict of bbox, landmarks, flame_parameters
                {
                    bboxes: (F, 5), F is the number of faces
                    landmarks: (F, 68, 2)
                    identity: (F, 100),
                    texture: (F, 50),
                    expression: (F, 50),
                    neck_rotation: (F, 3),
                    jaw_rotation: (F, 3),
                    global_rotation: (F, 3),
                    light: (F, 27),
                }
        """
        bboxes, landmarks = self.FDLM(input)
        outputs = dict(
            bboxes=bboxes,
            landmarks=landmarks,
        )
        if isinstance(input, ndarray):
            input = Image.fromarray(input.astype(np.uint8))
        for output_name in self.output_names:
            outputs[output_name] = []
        for landmark in landmarks:  # landmarks: (F, 68, 2)
            left, top = np.min(landmark, axis=0)
            right, bottom = np.max(landmark, axis=0)
            center_w = (right + left) / 2.0
            center_h = (bottom + top) / 2.0

            old_size = (right - left + bottom - top) / 2 * 1.1
            crop_size = old_size * 1.25

            L = center_w - crop_size / 2.0
            T = center_h - crop_size / 2.0
            R = center_w + crop_size / 2.0
            B = center_h + crop_size / 2.0
            crop = input.crop((L, T, R, B))
            if crop.size != (self.resolution, self.resolution):
                crop = crop.resize(
                    (self.resolution, self.resolution), Image.Resampling.LANCZOS
                ).convert("RGB")
            session_input = (
                np.array(crop, dtype=np.float32).transpose(2, 0, 1)[None]
                / 255.0
            )
            flame_parameters = self.session_run(session_input)
            for k, v in zip(self.output_names, flame_parameters):
                outputs[k].append(v)
        for output_name in self.output_names:
            outputs[output_name] = np.concatenate(outputs[output_name], axis=0)
        return outputs
