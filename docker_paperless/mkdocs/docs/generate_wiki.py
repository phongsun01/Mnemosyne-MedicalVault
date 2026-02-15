
import os
import requests
import yaml
import logging
from pathlib import Path
from datetime import datetime

# Configuration
PAPERLESS_API_URL = os.getenv("PAPERLESS_API_URL", "http://webserver:8000/api")
PAPERLESS_API_TOKEN = os.getenv("PAPERLESS_API_TOKEN")
WIKI_ROOT = Path("/docs/docs")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def slugify(text):
    return text.lower().replace(" ", "_").replace("-", "_")

def get_documents(query=None):
    headers = {"Authorization": f"Token {PAPERLESS_API_TOKEN}"}
    url = f"{PAPERLESS_API_URL}/documents/"
    if query:
        url += f"?query={query}"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get('results', [])
    except Exception as e:
        logging.error(f"Error fetching documents: {e}")
        return []

def generate_frontmatter(doc):
    # Default metadata
    metadata = {
        "device_id": doc['id'],
        "model": doc['title'], # Fallback
        "brand": "Unknown",
        "category": "Uncategorized",
        "tags": [tag for tag in doc['tags']],
        "last_updated": datetime.now().strftime("%Y-%m-%d")
    }

    # Extract Custom Fields if available
    # Note: Paperless API returns custom_fields as list of dicts or list of ids depending on version/config
    # Here we assume a simplified structure or need to fetch custom fields definition.
    # For MVP, we'll try to parse from content or tags if custom fields aren't easy.
    # In v2.2 plan, user mentioned custom_fields['category']. 
    # Let's try to extract from custom_fields if they exist in the response.
    
    for field in doc.get('custom_fields', []):
        # This part depends heavily on how custom fields are returned in API. 
        # For now, we will mock slightly or use tags as fallback for category.
        pass

    # Use tags for category if not found
    # Example tag: "Category: X-Quang"
    for tag in doc.get('tags', []):
         # In real Paperless, tags are initially IDs, need to fetch tag details.
         # For this MVP script, we assume 'tags' might be hydrated or we just use raw data.
         pass
         
    return metadata

def create_category_index(category_path, title):
    index_file = category_path / "index.md"
    if not index_file.exists():
        content = f"""# {title}

## 📋 Danh sách thiết bị
Đang cập nhật dữ liệu từ Paperless...

## 📊 Thống kê
- **Tổng số:** 0
"""
        index_file.write_text(content, encoding='utf-8')
        logging.info(f"Created index for {category_path}")

def generate_wiki():
    logging.info("Starting Wiki Generation...")
    
    # 1. Ensure Directory Structure & Indices (To fix 404s)
    structure = {
        "chan_doan_hinh_anh": "Chẩn đoán hình ảnh",
        "chan_doan_hinh_anh/x_quang": "X-Quang",
        "chan_doan_hinh_anh/ct_scanner": "CT Scanner",
        "chan_doan_hinh_anh/mri": "MRI",
        "noi_soi": "Nội soi",
        "noi_soi/noi_soi_da_day": "Nội soi dạ dày",
        "kiem_soat_nhiem_khuan": "Kiểm soát nhiễm khuẩn",
        "kiem_soat_nhiem_khuan/may_tiet_trung": "Máy tiệt trùng"
    }

    for path_str, title in structure.items():
        path = WIKI_ROOT / path_str
        path.mkdir(parents=True, exist_ok=True)
        create_category_index(path, title)

    # 2. Sync Documents
    docs = get_documents()
    logging.info(f"Found {len(docs)} documents to sync.")
    
    for doc in docs:
        # MVP: Create simple pages for now
        # Logic to be enhanced in "Week 1"
        pass
        
    logging.info("Wiki Generation Complete.")

if __name__ == "__main__":
    generate_wiki()
