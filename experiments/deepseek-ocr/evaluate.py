from ecpo_ocr_bench import evaluate_ocr_tool
from transformers import AutoModel, AutoTokenizer

import json
import os
import pathlib
import tempfile
import torch


os.environ["CUDA_VISIBLE_DEVICES"] = "0"
model_name = "deepseek-ai/DeepSeek-OCR"

tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModel.from_pretrained(
    model_name,
    _attn_implementation="flash_attention_2",
    trust_remote_code=True,
    use_safetensors=True,
)
model = model.eval().cuda().to(torch.bfloat16)


def run_deepseek_ocr(image: pathlib.Path):
    with tempfile.TemporaryDirectory() as tmp:
        model.infer(
            tokenizer,
            prompt="<image>\nOCR this image.",
            image_file=image,
            output_path=tmp,
            crop_mode=False,
            save_results=True,
            test_compress=False,
        )

        with open(tmp / "result.mmd", "r") as f:
            return f.read()


result = evaluate_ocr_tool(run_deepseek_ocr)

with open("deep-seek-ocr.json", "w") as f:
    json.dump(result, f)
