from typing import Callable

import Levenshtein
import matplotlib.pyplot as plt
import numpy as np
import pathlib
import tqdm


def generate_image_gt_pairs(data_dir: pathlib.Path):
    for image in data_dir.rglob("*.png"):
        gt = image.parent / (str(image.stem) + ".txt")
        if not gt.exists():
            raise ValueError(f"Missing ground truth for image file {image.stem}")
        yield (image, gt)


def normalize(s: str) -> str:
    return s.replace("<lb/>", "").replace("\n", "").replace(" ", "").replace("e", "")


def normalize_ground_truth(filename: pathlib.Path) -> str:
    with open(filename, "r", encoding="utf-8") as f:
        return normalize(f.read())


def evaluate_ocr_tool(
    function: Callable[[pathlib.Path], str],
    data_dir: pathlib.Path = pathlib.Path(__file__).resolve().parent.parent / "data",
):
    result = {}
    pairs = list(generate_image_gt_pairs(data_dir))
    for image, gt in tqdm.tqdm(pairs):
        original_ocr_result = function(image)
        normalized_ocr_result = normalize(original_ocr_result)
        ground_truth = normalize_ground_truth(gt)
        editops = Levenshtein.editops(normalized_ocr_result, ground_truth)

        result[image.stem] = {
            "original_ocr_result": original_ocr_result,
            "normalized_ocr_result": normalized_ocr_result,
            "normalized_ground_truth": ground_truth,
            "distance": len(editops),
            "editops": {"replacements": [], "deletions": [], "insertions": []},
            "error_positions": [],
        }

        for op, src, dst in editops:
            result[image.stem]["error_positions"].append(dst)
            if op == "replace":
                result[image.stem]["editops"]["replacements"].append(
                    [normalized_ocr_result[src], ground_truth[dst]]
                )
            if op == "insert":
                result[image.stem]["editops"]["insertions"].append([ground_truth[dst]])
            if op == "delete":
                result[image.stem]["editops"]["deletions"].append(
                    [normalized_ocr_result[src]]
                )

    return result


def error_localization_histogram(data: dict):
    # Extract the data for the histogram
    histdata = sum(
        (
            [
                p / len(data[im]["normalized_ground_truth"])
                for p in data[im]["error_positions"]
            ]
            for im in data
        ),
        [],
    )

    # Create a new figure and axis
    fig, ax = plt.subplots()

    # Plot the histogram
    ax.hist(histdata, bins=1000, edgecolor="black")

    # Set labels and title
    ax.set_title("Error locality within text crop")
    ax.set_xlabel("Position within text crop")
    ax.set_ylabel("Error frequency")

    # Return the figure object
    return fig


def common_misrecognized_characters(data: dict, threshold: int = 1):
    mistakes = {}
    for stem in data:
        for _, real in data[stem]["editops"]["replacements"]:
            mistakes.setdefault(real, 0)
            mistakes[real] = mistakes[real] + 1

    # Apply thresholding
    mistakes = {
        char: number for char, number in mistakes.items() if number >= threshold
    }

    return mistakes
