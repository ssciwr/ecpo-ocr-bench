# Installation Instructions

From [the DeepSeek-OCR README](https://github.com/deepseek-ai/DeepSeek-OCR?tab=readme-ov-file#install):
```bash
git clone https://github.com/deepseek-ai/DeepSeek-OCR.git
conda create -n deepseek-ocr python=3.12.9 -y
conda activate deepseek-ocr
pip install torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu118
pip install vllm-0.8.5+cu118-cp38-abi3-manylinux1_x86_64.whl
pip install -r requirements.txt
pip install flash-attn==2.7.3 --no-build-isolation
```
