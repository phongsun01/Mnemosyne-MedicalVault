
FROM python:3.9-slim

WORKDIR /docs

COPY requirements.txt .
RUN pip install --no-cache-dir mkdocs-material

CMD ["mkdocs", "serve", "-a", "0.0.0.0:8000"]
