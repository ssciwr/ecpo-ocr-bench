from ecpo_ocr_bench.data import copy_data

import click
import pathlib


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
