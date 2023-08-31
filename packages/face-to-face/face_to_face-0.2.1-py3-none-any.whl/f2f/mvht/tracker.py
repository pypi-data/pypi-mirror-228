import argparse
import glob
import os

import numpy as np
import torch
import torch.nn as nn
from PIL import Image
from PIL.Image import Resampling


class Tracker:
    def __init__(self) -> None:
        pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True)
    parser.add_argument("--output", type=str, default="output")
    args = vars(parser.parse_args())


if __name__ == "__main__":
    main()
