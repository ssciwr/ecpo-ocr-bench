import itertools
import pathlib
import shutil


def copy_data(sds: pathlib.Path, dest: pathlib.Path) -> None:
    """Copy data from SDS folder into our own data directory. """

    # Ensure existence of destination directory
    pathlib.Path(dest).mkdir(parents=True, exist_ok=True)

    # Select correct SDS subfolder
    sds = sds / "@DATA" / "annotated_crops"

    # Grep for files in all subfolders
    for subfolder in ["001-500", "501-1000"]:
        images = (sds / subfolder).rglob("*.png")
        gt = (sds / subfolder).rglob("[0-9]*.txt")

        for fn in itertools.chain(images, gt):
            if "cool" not in str(fn):
                shutil.copy(fn, dest)
