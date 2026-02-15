
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
    
    # Structure mapping (Tag -> Folder)
    tag_map = {
        "x-quang": "chan_doan_hinh_anh/x_quang",
        "ct-scanner": "chan_doan_hinh_anh/ct_scanner",
        "mri": "chan_doan_hinh_anh/mri",
        "sieu-am": "chan_doan_hinh_anh/sieu_am",
        "noi-soi-da-day": "noi_soi/noi_soi_da_day",
        "tiet-trung": "kiem_soat_nhiem_khuan/may_tiet_trung"
    }

    # Prepare lists for indices
    category_content = {k: [] for k in tag_map.values()}
    category_content["uncategorized"] = []

    for doc in docs:
        metadata = generate_frontmatter(doc)
        doc_id = metadata['device_id']
        title = metadata['model']
        
        # Determine Path
        target_folder = "uncategorized"
        for tag in metadata['tags']:
            slug_tag = slugify(tag.get('name', '') if isinstance(tag, dict) else str(tag)) # Handle dict or ID
            if slug_tag in tag_map:
                target_folder = tag_map[slug_tag]
                break
        
        # Create MD Content
        file_name = f"{doc_id}_{slugify(title)}.md"
        if target_folder == "uncategorized":
             # Create uncategorized folder if not exists
             (WIKI_ROOT / "uncategorized").mkdir(exist_ok=True)
             
        file_path = WIKI_ROOT / target_folder / file_name
        
        md_content = f"""---
title: {title}
---
# {title}

**ID:** {doc_id}
**Updated:** {metadata['last_updated']}

[Xem tài liệu gốc]({PAPERLESS_API_URL.replace('/api', '')}/documents/{doc_id}/preview)

## 📄 Nội dung Preview
*(Nội dung trích xuất từ AI sẽ hiển thị tại đây)*
"""
        try:
            file_path.write_text(md_content, encoding='utf-8')
            link = f"- [{title}]({file_name})"
            category_content[target_folder].append(link)
            logging.info(f"Generated {file_path}")
        except Exception as e:
            logging.error(f"Failed to write {file_path}: {e}")

    # 3. Update Index Files
    for folder, links in category_content.items():
        if not links:
            continue
            
        index_path = WIKI_ROOT / folder / "index.md"
        if index_path.exists():
            current_content = index_path.read_text(encoding='utf-8')
            # Append list if not already present (Simple append for MVP)
            new_list = "\n\n## 🆕 Thiết bị mới cập nhật\n" + "\n".join(links)
            
            # Reset file to clean state before appending to avoid duplication in loop runs? 
            # For MVP, let's just rewrite the list section or append. 
            # Safer: Rewrite the "Danh sách thiết bị" section.
            
            # Simple overwrite for Demo:
            base_header = current_content.split("## 📋 Danh sách thiết bị")[0]
            new_content = f"{base_header}## 📋 Danh sách thiết bị\n" + "\n".join(links) + "\n\n## 📊 Thống kê"
            
            index_path.write_text(new_content, encoding='utf-8')
            logging.info(f"Updated index for {folder}")
    
    logging.info("Wiki Generation Complete.")

if __name__ == "__main__":
    generate_wiki()
