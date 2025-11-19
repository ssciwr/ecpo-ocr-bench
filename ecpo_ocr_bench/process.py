from PIL import Image
from typing import Callable

import functools
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


@functools.lru_cache()
def modern_character_replacement_dict():
    """Load our replacements into a dictionary."""

    with open(pathlib.Path(__file__).parent / "replacements.txt", "r") as f:
        return {l[0]: l[1] for l in f.readlines()}


def normalize(
    s: str,
    normalize_punctuation=True,
    normalize_modern_chars=True,
    ignore_linebreaks=False,
    ignore_punctuation=False,
) -> str:
    # These are some replacement that we specifically apply to our
    # groundtruth to remove conventions of that ground truth annotation.
    s = s.replace("<lb/>", "").replace("e", "").replace("c", "").replace("&gaiji;", "¤")

    # Here are some replacements that we unconditionally apply.
    s = (
        s.replace(" ", "")  # We are not interested in whitespace detection
        .replace("　", "")
        .replace("︵", "（")  # Round brackets pointing up and down were
        .replace("︶", "）")  # not known to Matthias and are not in the GT
        .replace("｜", "－")  # Assuming this is the same problem
    )

    if normalize_punctuation:
        s = (
            s.replace("『", "「")  # The "quotation marks" do not really matter to
            .replace("』", "」")  # us, so we unconditionally harmonize them.
            .replace("、", "，")  # We harmonize the idiographic commata
            .replace("(", "（")
            .replace(")", "）")
            .replace(",", "，")
        )

    if ignore_linebreaks:
        s = s.replace("\n", "")

    if ignore_punctuation:
        for p in "『』「」、，()（）,。．一—：；⋯！":
            s = s.replace(p, "")

    if normalize_modern_chars:
        for old, new in modern_character_replacement_dict().items():
            s = s.replace(old, new)

    # At the very end - strip the final newline character
    s = s.strip()

    return s


def load_ground_truth(filename: pathlib.Path) -> str:
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()


def evaluate_ocr_tool(
    function: Callable[[pathlib.Path], str],
    data_dir: pathlib.Path = pathlib.Path(__file__).resolve().parent.parent / "data",
    normalize_punctuation=True,
    normalize_modern_chars=True,
    ignore_linebreaks=False,
    ignore_punctuation=False,
):
    def _norm(s):
        return normalize(
            s,
            normalize_punctuation=normalize_punctuation,
            normalize_modern_chars=normalize_modern_chars,
            ignore_linebreaks=ignore_linebreaks,
            ignore_punctuation=ignore_punctuation,
        )

    result = {}
    pairs = list(generate_image_gt_pairs(data_dir))
    for image, gt in tqdm.tqdm(pairs):
        original_ocr_result = function(image)
        normalized_ocr_result = _norm(original_ocr_result)
        ground_truth = _norm(load_ground_truth(gt))
        editops = Levenshtein.editops(normalized_ocr_result, ground_truth)

        # Filter out those edit-ops that replace against a character not in the encoding set
        editops = [
            (o, s, d)
            for o, s, d in editops
            if not (((o == "replace") or (o == "insert")) and (ground_truth[d] == "¤"))
        ]

        width, height = Image.open(image).size

        result[image.stem] = {
            "original_ocr_result": original_ocr_result,
            "normalized_ocr_result": normalized_ocr_result,
            "normalized_ground_truth": ground_truth,
            "distance": len(editops),
            "editops": {"replacements": [], "deletions": [], "insertions": []},
            "error_positions": [],
            "width": width,
            "height": height,
        }

        for op, src, dst in editops:
            result[image.stem]["error_positions"].append(dst)
            if op == "replace":
                result[image.stem]["editops"]["replacements"].append(
                    [normalized_ocr_result[src], ground_truth[dst]]
                )
            if op == "insert":
                result[image.stem]["editops"]["insertions"].append(ground_truth[dst])
            if op == "delete":
                result[image.stem]["editops"]["deletions"].append(
                    normalized_ocr_result[src]
                )

    return result


def rerun_evaluate_ocr_tool(
    previous_results,
    data_dir: pathlib.Path = pathlib.Path(__file__).resolve().parent.parent / "data",
):
    """Redoes the analysis, if our analysis code changed.

    Valueable if we are still tweaking the code and want to avoid running
    costly OCR steps.
    """

    def func(image):
        return previous_results[image.stem]["original_ocr_result"]

    return evaluate_ocr_tool(func, data_dir)


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
