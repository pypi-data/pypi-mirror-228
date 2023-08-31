import math
import os
from typing import Any, Callable, List, Optional, Union, cast

import librosa
import numpy as np
import torch
import torch.nn as nn
from numpy import ndarray
from torch import Tensor
from transformers import Wav2Vec2Processor

from f2f.wav2mm.faceformer.wav2vec2 import Wav2Vec2Model


# Temporal Bias, inspired by ALiBi: https://github.com/ofirpress/attention_with_linear_biases
def init_biased_mask(n_head, max_seq_len, period):
    def get_slopes(n):
        def get_slopes_power_of_2(n):
            start = 2 ** (-(2 ** -(math.log2(n) - 3)))
            ratio = start
            return [start * ratio**i for i in range(n)]

        if math.log2(n).is_integer():
            return get_slopes_power_of_2(n)
        else:
            closest_power_of_2 = 2 ** math.floor(math.log2(n))
            return (
                get_slopes_power_of_2(closest_power_of_2)
                + get_slopes(2 * closest_power_of_2)[0::2][
                    : n - closest_power_of_2
                ]
            )

    slopes = torch.Tensor(get_slopes(n_head))
    bias = torch.arange(start=0, end=max_seq_len, step=period).unsqueeze(
        1
    ).repeat(1, period).view(-1) // (period)
    bias = -torch.flip(bias, dims=[0])
    alibi = torch.zeros(max_seq_len, max_seq_len)
    for i in range(max_seq_len):
        alibi[i, : i + 1] = bias[-(i + 1) :]
    alibi = slopes.unsqueeze(1).unsqueeze(1) * alibi.unsqueeze(0)
    mask = (torch.triu(torch.ones(max_seq_len, max_seq_len)) == 1).transpose(
        0, 1
    )
    mask = (
        mask.float()
        .masked_fill(mask == 0, float("-inf"))
        .masked_fill(mask == 1, float(0.0))
    )
    mask = mask.unsqueeze(0) + alibi
    return mask


# Alignment Bias
def enc_dec_mask(device, T, S):
    mask = torch.ones(T, S)
    for i in range(T):
        mask[i, i] = 0
    return (mask == 1).to(device=device)


class PeriodicPositionalEncoding(nn.Module):
    pe: Tensor

    def __init__(
        self, d_model, dropout=0.1, period=25, max_seq_len=600
    ) -> None:
        super().__init__()
        self.dropout = nn.Dropout(p=dropout)
        pe = torch.zeros(period, d_model)
        position = torch.arange(0, period, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(
            torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model)
        )
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0)  # (1, period, d_model)
        repeat_num = (max_seq_len // period) + 1
        pe = pe.repeat(1, repeat_num, 1)
        self.register_buffer("pe", pe)

    def forward(self, x: Tensor) -> Tensor:
        x = x + self.pe[:, : x.size(1), :]
        return self.dropout(x)


class FaceFormer(nn.Module):
    def __init__(
        self,
        checkpoint: Optional[str] = None,
        device: Optional[Union[str, torch.device]] = None,
    ):
        super().__init__()
        self.dataset = "vocaset"
        self.vertice_dim = 5023
        self.feature_dim = 64
        self.period = 30
        self.sampling_rate = 16000
        # ***** DON'T SORT THE TRAIN SUBJECTS *****
        self._train_subjects = (
            "FaceTalk_170728_03272_TA",
            "FaceTalk_170904_00128_TA",
            "FaceTalk_170725_00137_TA",
            "FaceTalk_170915_00223_TA",
            "FaceTalk_170811_03274_TA",
            "FaceTalk_170913_03279_TA",
            "FaceTalk_170904_03276_TA",
            "FaceTalk_170912_03278_TA",
        )

        self.processor = Wav2Vec2Processor.from_pretrained(
            "facebook/wav2vec2-base-960h"
        )
        self.audio_encoder = Wav2Vec2Model.from_pretrained(
            "facebook/wav2vec2-base-960h"
        )
        # wav2vec 2.0 weights initialization
        self.audio_encoder.feature_extractor._freeze_parameters()
        self.audio_feature_map = nn.Linear(768, self.feature_dim)
        # motion encoder
        self.vertice_map = nn.Linear(self.vertice_dim * 3, self.feature_dim)
        # periodic positional encoding
        self.PPE = PeriodicPositionalEncoding(
            self.feature_dim, period=self.period
        )
        # temporal bias
        self.biased_mask = init_biased_mask(
            n_head=4, max_seq_len=600, period=self.period
        )
        decoder_layer = nn.TransformerDecoderLayer(
            d_model=self.feature_dim,
            nhead=4,
            dim_feedforward=2 * self.feature_dim,
            batch_first=True,
        )
        self.transformer_decoder = nn.TransformerDecoder(
            decoder_layer, num_layers=1
        )
        # motion decoder
        self.vertice_map_r = nn.Linear(self.feature_dim, self.vertice_dim * 3)
        # style embedding
        self.obj_vector = nn.Linear(
            len(self.train_subjects), self.feature_dim, bias=False
        )
        nn.init.constant_(self.vertice_map_r.weight, 0)
        nn.init.constant_(self.vertice_map_r.bias, 0)

        self.device = torch.device(device or "cpu")
        if checkpoint:
            if not os.path.exists(checkpoint):
                raise ValueError("Checkpoint not found.")
            self.load_state_dict(torch.load(checkpoint, map_location="cpu"))
            print("Loaded checkpoint from {}".format(checkpoint))
        self.to(self.device)

    @property
    def train_subjects(self) -> List[str]:
        return list(self._train_subjects)

    def _apply(self, fn: Callable[..., Any]) -> "FaceFormer":
        if "t" in fn.__code__.co_varnames:
            with torch.no_grad():
                null_tensor = torch.zeros(0, device=self.device)
                device = getattr(fn(null_tensor), "device", "cpu")
            self.device = torch.device(device)
        return super()._apply(fn)

    def forward(self, audio: Union[str, ndarray], style: int = 0) -> Tensor:
        self.eval()

        if 0 < style <= len(self.train_subjects):
            raise ValueError(
                f"style should be in range [0, {len(self.train_subjects)}), got {style}"
            )
        one_hot = torch.zeros(
            len(self.train_subjects), dtype=torch.float32, device=self.device
        )
        one_hot[style] = 1

        obj_embedding: Tensor = self.obj_vector(one_hot.unsqueeze(0))

        if isinstance(audio, str):
            speech_array = librosa.load(audio, sr=self.sampling_rate)[0]
            audio = np.array(
                self.processor(speech_array, sampling_rate=self.sampling_rate)[
                    "input_values"
                ]
            )
        audio = audio.squeeze()
        audio = (
            torch.from_numpy(audio)
            .view(-1, audio.shape[0])
            .to(dtype=torch.float32, device=self.device)
        )
        hidden_states = cast(
            Tensor, self.audio_encoder(audio).last_hidden_state
        )
        frame_num = hidden_states.size(1)
        hidden_states = self.audio_feature_map(hidden_states)

        for i in range(frame_num):
            if i == 0:
                vertice_emb = obj_embedding.unsqueeze(1)  # (1, 1, feature_dim)
                style_emb = vertice_emb
                vertice_input: Tensor = self.PPE(style_emb)
            else:
                vertice_input = self.PPE(vertice_emb)

            tgt_mask = (
                self.biased_mask[
                    :, : vertice_input.size(1), : vertice_input.size(1)
                ]
                .clone()
                .detach()
                .to(device=self.device)
            )
            memory_mask = enc_dec_mask(
                self.device,
                vertice_input.size(1),
                hidden_states.size(1),
            )
            vertice_out: Tensor = self.transformer_decoder(
                vertice_input,
                hidden_states,
                tgt_mask=tgt_mask,
                memory_mask=memory_mask,
            )
            vertice_out = self.vertice_map_r(vertice_out)
            new_output = self.vertice_map(vertice_out[:, -1, :]).unsqueeze(1)
            new_output = new_output + style_emb
            vertice_emb = torch.cat((vertice_emb, new_output), 1)

        return vertice_out.reshape(-1, self.vertice_dim, 3)
