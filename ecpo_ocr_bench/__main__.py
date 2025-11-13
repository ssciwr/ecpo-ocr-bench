from ecpo_ocr_bench.data import copy_data
from ecpo_ocr_bench.process import rerun_evaluate_ocr_tool

import json
import click
import pathlib
import shutil


@click.command()
@click.argument(
    "results",
    type=click.Path(
        path_type=pathlib.Path,
        exists=True,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
    ),
    required=True,
)
def update_analysis(results):
    # Make a backup copy of the data, so that we never lose valuable OCR
    # results due to a malformed analysis script.
    shutil.copy(results, results.parent / (results.name + ".bkp"))

    # Load the data
    with open(results, "r") as f:
        data = json.load(f)

    with open(results, "w") as f:
        json.dump(rerun_evaluate_ocr_tool(data), f)


@click.command()
@click.option(
    "--sds",
    "-s",
    type=click.Path(
        path_type=pathlib.Path,
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
    ),
    help="The SDS@HD mountpoint. Must point to the directory of the SV sd21c016.",
    default=pathlib.Path.home() / "sds" / "sd21c016",
    show_default=True,
)
@click.option(
    "--dest",
    "-d",
    type=click.Path(
        path_type=pathlib.Path,
        exists=False,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
    ),
    default="./data",
    help="The workspace directory to create.",
    show_default=True,
)
def copy_sds_data(sds, dest):
    copy_data(sds, dest)
