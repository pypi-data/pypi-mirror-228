import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[2]))

import argparse
import multiprocessing as mp
from typing import List, Optional

import numpy as np
import tqdm
from PIL import Image

from f2f.deca.onnx import EMOCAONNX


def run(args):
    process_id = args["process_id"]
    device = args["device"]
    model = EMOCAONNX(device=device)
    for path in tqdm.tqdm(
        args["paths"],
        desc=f"Process {process_id} GPU {device}",
        position=process_id,
    ):
        output = model(Image.open(path))
        relpath = Path(path).relative_to(args["root"])
        output_path = (
            Path(args["output"]) / relpath.parent / (Path(path).name + ".npz")
        )
        output_path.parent.mkdir(exist_ok=True, parents=True)
        np.savez_compressed(output_path, **output)


def gpu_args(arg: Optional[str] = None):
    if arg is None:
        return []
    if "," in arg:
        return [int(x) for x in arg.split(",")]
    return [int(arg)]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", type=str, required=True)
    parser.add_argument("--output", "-o", type=str, default="output_emoca")
    parser.add_argument("--re_pattern", "-rp", type=str, default="**/*.*g")
    parser.add_argument("--gpus", "-g", type=gpu_args, default=[0])
    parser.add_argument(
        "--workers_per_gpu",
        "-wg",
        type=int,
        default=2,
        help="Number of workers per GPU, each worker consume 2GB of GPU memory",
    )
    args = vars(parser.parse_args())

    images = list(Path(args["input"]).glob(args["re_pattern"]))
    images.sort()
    assert len(images) > 0, "No images found"
    print(f"Found {len(images)} images")

    n_gpus = len(args["gpus"])
    n_workers = n_gpus * args["workers_per_gpu"]
    print(f"Using {n_gpus} GPUs with {n_workers} workers")

    workers: List[mp.Process] = []
    for i in range(n_workers):
        workers.append(
            mp.Process(
                target=run,
                args=(
                    {
                        "device": args["gpus"][i % n_gpus],
                        "root": args["input"],
                        "paths": images[i::n_workers],
                        "process_id": i,
                        "output": args["output"],
                    },
                ),
            )
        )
    for worker in workers:
        worker.start()


if __name__ == "__main__":
    main()
