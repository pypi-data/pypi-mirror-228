from typing import Dict, Optional

import torch.nn as nn
from torch import Tensor

from f2f.flame import FLAME, FLAMETexture


class FLAMERenderer(nn.Module):
    def __init__(self, use_texture: bool = False) -> None:
        super().__init__()
        self.flame = FLAME()
        if use_texture:
            self.flame_tex = FLAMETexture()
        else:
            self.flame_tex = None

    def forward(
        self,
        identity_params: Optional[Tensor] = None,
        expression_params: Optional[Tensor] = None,
        global_rotation: Optional[Tensor] = None,
        neck_rotation: Optional[Tensor] = None,
        jaw_rotation: Optional[Tensor] = None,
        eyes_rotation: Optional[Tensor] = None,
        texture_params: Optional[Tensor] = None,
    ) -> Dict[str, Tensor]:
        pass
