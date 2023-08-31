from pathlib import Path
from typing import Tuple, Union

import numpy as np
from numpy import ndarray
from PIL import Image

from f2f.core.onnx import BaseONNX

ONNX_PATH = (
    Path(__file__).parents[2] / "assets" / "matting" / "SGHM-ResNet50.onnx"
)


class SemanticGuidedHumanMattingONNX(BaseONNX):
    resolution: int = 1280

    def __init__(
        self, seg_threshold: float = 0.8, device: Union[str, int] = "cpu"
    ) -> None:
        super().__init__(str(ONNX_PATH), device)
        self.seg_threshold = seg_threshold

    def single_forward(
        self, input: Union[ndarray, Image.Image]
    ) -> Tuple[ndarray, ndarray]:
        """
        Args:
            input: (H, W, 3), RGB image in range [0, 255] or PIL.Image
        Returns:
            alpha: (H, W), alpha matte in range [0, 1]
            segmentation: (H, W), binary segmentation mask by thresholding
        """
        if isinstance(input, ndarray):
            input = Image.fromarray(input.astype(np.uint8))
        W, H = input.size
        S, L = sorted((W, H))
        if L == self.resolution:
            new_W = W
            new_H = H
        else:
            ratio = self.resolution / L
            new_W, new_H = int(W * ratio), int(H * ratio)
            input = input.resize((new_W, new_H), Image.Resampling.LANCZOS)

        session_input = np.zeros(
            (1, 3, self.resolution, self.resolution), dtype=np.float32
        )
        session_input[0, :, :new_H, :new_W] = np.array(
            input.convert("RGB"), dtype=np.float32
        ).transpose(2, 0, 1)
        alpha, segmentation = self.session_run(session_input / 127.5 - 1.0)
        alpha = alpha[0, 0, :new_H, :new_W]
        segmentation = segmentation[0, 0, :new_H, :new_W]
        if L != self.resolution:
            alpha_image = Image.fromarray((alpha * 255.0).astype(np.uint8))
            alpha_image = alpha_image.resize((W, H), Image.Resampling.LANCZOS)
            alpha = np.array(alpha_image, dtype=np.float32) / 255.0

            seg_image = Image.fromarray((segmentation * 255.0).astype(np.uint8))
            seg_image = seg_image.resize((W, H), Image.Resampling.LANCZOS)
            segmentation = np.array(seg_image, dtype=np.float32) / 255.0

        # make binary segmentation mask
        segmentation = (segmentation > self.seg_threshold).astype(np.float32)
        return alpha, segmentation

    def __call__(
        self, input: Union[ndarray, Image.Image]
    ) -> Tuple[ndarray, ndarray]:
        """
        input: (H, W, 3), RGB image in range [0, 255] or PIL.Image
        """
        return self.single_forward(input)
