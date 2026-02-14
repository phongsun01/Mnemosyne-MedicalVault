FROM python:3.11-slim

# Install system dependencies for PDF and Image processing
RUN apt-get update && apt-get install -y \
    poppler-utils \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    chromadb \
    google-generativeai \
    python-docx \
    pandas \
    openpyxl \
    PyPDF2 \
    pdf2image \
    watchdog \
    httpx \
    python-telegram-bot \
    python-dotenv

# Copy code
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
