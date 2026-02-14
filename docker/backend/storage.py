import os
import chromadb
from chromadb.config import Settings
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Setup ChromaDB client
try:
    chroma_client = chromadb.HttpClient(host='chromadb', port=8000)
    collection = chroma_client.get_or_create_collection(name="medical_devices")
except Exception as e:
    logger.error(f"ChromaDB connection failed: {e}")
    collection = None

def save_to_markdown(metadata, source_file):
    base_path = "/vault/md/devices"
    os.makedirs(base_path, exist_ok=True)
    
    file_name = f"{metadata.get('model', 'unknown')}.md".replace("/", "_")
    target_path = os.path.join(base_path, file_name)
    
    template = f"""---
device_id: "{metadata.get('model')}"
model: "{metadata.get('model')}"
brand: "{metadata.get('brand')}"
origin: "{metadata.get('origin')}"
category: "{metadata.get('category')}"
created_at: "{datetime.now().strftime('%Y-%m-%d')}"
source: "{os.path.basename(source_file)}"
---

# {metadata.get('model')} ({metadata.get('brand')})

## Thông số kỹ thuật
{metadata.get('specs')}

## Thông tin bổ sung
- **Hãng:** {metadata.get('brand')}
- **Xuất xứ:** {metadata.get('origin')}
- **Giá dự kiến:** {metadata.get('price_range')}
"""
    
    with open(target_path, 'w') as f:
        f.write(template)
    
    logger.info(f"Markdown saved: {target_path}")
    return target_path

def index_in_chroma(metadata, doc_path):
    if not collection:
        return
    
    content = f"Model: {metadata.get('model')}, Brand: {metadata.get('brand')}, Origin: {metadata.get('origin')}, Specs: {metadata.get('specs')}"
    
    collection.add(
        documents=[content],
        metadatas=[{
            "model": str(metadata.get('model')),
            "brand": str(metadata.get('brand')),
            "path": doc_path
        }],
        ids=[str(metadata.get('model'))]
    )
    logger.info(f"Indexed in ChromaDB: {metadata.get('model')}")
