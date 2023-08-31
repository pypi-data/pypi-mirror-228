import os
import re
from typing import Tuple

import torch

from f2f.arcface.iresnet import IBasicBlock, IResNet


def architecture_from_checkpoint(checkpoint: str) -> Tuple[int, ...]:
    """
    Get the architecture from checkpoint.
    """
    state_dict = torch.load(checkpoint, map_location="cpu")
    layers = [0, 0, 0, 0]
    for key, val in state_dict.items():
        pass


class Arcface(IResNet):
    def __init__(
        self,
        checkpoint=None,
    ):
        super().__init__(
            block=IBasicBlock,
            layers=[3, 13, 30, 3],
            num_features=512,
        )
