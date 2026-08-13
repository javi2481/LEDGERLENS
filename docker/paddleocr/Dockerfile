# CPU PaddleOCR / PaddleX serving for RAGFlow remote client (POST /layout-parsing).
# Pin: PaddlePaddle 3.1.0 CPU + PaddleX 3.7.2 with serving plugin.
FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PADDLE_PDX_MODEL_SOURCE=huggingface

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libgl1 \
        libglib2.0-0 \
        libgomp1 \
        libgfortran5 \
        fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
        paddlepaddle==3.1.0 \
        paddlex==3.7.2 \
    && paddlex --install serving

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=10 \
    CMD python -c "import socket; s=socket.create_connection(('127.0.0.1',8080),5); s.close()"

CMD ["paddlex", "--serve", "--pipeline", "PP-StructureV3", "--device", "cpu", "--host", "0.0.0.0", "--port", "8080"]
