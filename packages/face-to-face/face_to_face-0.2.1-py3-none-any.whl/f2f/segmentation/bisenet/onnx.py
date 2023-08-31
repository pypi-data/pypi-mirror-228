from pathlib import Path
from typing import Dict, Sequence, Union

import numpy as np
from numpy import ndarray
from PIL import Image

from f2f.core.onnx import BaseONNX

ONNX_PATH = (
    Path(__file__).parents[2] / "assets" / "segmentation" / "bisenet.onnx"
)


class FaceBiSeNetONNX(BaseONNX):
    resolution: int = 512
    parts: Dict[str, int] = {
        "background": 0,
        "skin": 1,
        "l_brow": 2,
        "r_brow": 3,
        "l_eye": 4,
        "r_eye": 5,
        "eye_glass": 6,
        "l_ear": 7,
        "r_ear": 8,
        "ear_ring": 9,
        "nose": 10,
        "mouth": 11,
        "u_lip": 12,
        "l_lip": 13,
        "neck": 14,
        "necklace": 15,
        "cloth": 16,
        "hair": 17,
        "hat": 18,
    }

    def __init__(self, device: Union[str, int] = "cpu") -> None:
        super().__init__(str(ONNX_PATH), device)

    def __call__(self, input: Union[ndarray, Image.Image]) -> ndarray:
        """
        Args:
            input: (H, W, 3), RGB image in range [0, 255] or PIL.Image
        Returns:
            segmentation: (H, W) segmentation mask in range [0, 18], background + 18 classes
        """
        if isinstance(input, Image.Image):
            input = np.array(input)
        session_input = (
            input.astype(np.float32).transpose(2, 0, 1)[None] / 127.5 - 1.0
        )
        segmentation = self.session_run(session_input)[0]
        return segmentation[0, 0]

    def segmentation_to_mask(
        self, segmentation: ndarray, parts: Sequence[Union[str, int]]
    ) -> ndarray:
        """
        Args:
            segmentation: (H, W) segmentation mask in range [0, 18], background + 18 classes
            parts: list of part names or indices to include in the mask
        Returns:
            mask: (H, W) boolean mask
        """
        mask = np.zeros_like(segmentation, dtype=bool)
        for part in parts:
            if isinstance(part, str):
                part = self.parts[part]
            mask[segmentation == part] = True
        return mask
