from ecpo_ocr_bench import evaluate_ocr_tool

import base64
import json
import openai
import pathlib


# Example: local vLLM/OpenAI-compatible server
client = openai.OpenAI(
    api_key="your_api_key_here",  # Some servers ignore this
    base_url="http://localhost:8080/v1",  # Custom OpenAI-compatible endpoint
)


PROMPT = """
Your task is to OCR this image written in traditional chinese.

Your result needs to fulfill **all** of these constraints:
* Give the result **exactly** as it appears on the image
* Keep line breaks from the original
* Do not modify to modern chinese, keep exactly as is.
* Denote numbers exactly like in the image, not in english writing.

Double-check your response so that it fulfills all contraints.
"""


def run_qwen3_vl(image: pathlib.Path):
    # Encode as base64
    with open(image, "rb") as f:
        image_base64 = base64.b64encode(f.read()).decode("utf-8")

    # Build a data URL for the image
    image_data_url = f"data:image/jpeg;base64,{image_base64}"

    # Create a multimodal chat request
    response = client.chat.completions.create(
        model="Qwen3-VL-235B-A22B-Instruct-1M-Q4_K_M-00001-of-00003.gguf",  # or your model name (depends on your server)
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": PROMPT},
                    {"type": "image_url", "image_url": {"url": image_data_url}},
                ],
            }
        ],
    )

    # Extract result
    return response.choices[0].message.content


result = evaluate_ocr_tool(run_qwen3_vl)

with open("qwen3-vl-235B.json", "w") as f:
    json.dump(result, f)
