from importlib import metadata

__version__ = metadata.version(__package__)
del metadata


from ecpo_ocr_bench.process import (
    evaluate_ocr_tool,
    error_localization_histogram,
    common_misrecognized_characters,
)
