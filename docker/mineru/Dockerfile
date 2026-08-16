# CPU MinerU API for RAGFlow remote client (POST /file_parse, backend=pipeline).
# Official mineru:latest is vLLM/GPU; pipeline extra is the CPU path.
# Pin: mineru 3.4.5 (keeps /file_parse for RAGFlow v0.26.4). No vllm extra.
FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    MINERU_MODEL_SOURCE=huggingface

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libgl1 \
        libglib2.0-0 \
        libgomp1 \
        libsm6 \
        libxext6 \
        libxrender1 \
        fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

# CPU torch first so mineru[pipeline] does not pull a CUDA wheel.
RUN pip install --no-cache-dir \
        torch torchvision \
        --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir "mineru[pipeline]==3.4.5"

# pytorchocr (pipeline) imports six; mineru[pipeline] extra does not declare it.
RUN pip install --no-cache-dir six

EXPOSE 8000

HEALTHCHECK --interval=15s --timeout=10s --start-period=180s --retries=20 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=5)"

CMD ["mineru-api", "--host", "0.0.0.0", "--port", "8000"]
