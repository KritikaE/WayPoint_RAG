FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

# Install CPU-only PyTorch (no NVIDIA/CUDA packages)
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/
COPY src/ src/
COPY chroma_db/ chroma_db/
COPY data/ data/

EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]gi