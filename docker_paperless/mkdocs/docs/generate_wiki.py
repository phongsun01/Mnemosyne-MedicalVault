
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

def get_tags():
    headers = {"Authorization": f"Token {PAPERLESS_API_TOKEN}"}
    try:
        response = requests.get(f"{PAPERLESS_API_URL}/tags/", headers=headers)
        response.raise_for_status()
        results = response.json().get('results', [])
        return {t['id']: t['name'] for t in results}
    except Exception as e:
        logging.error(f"Error fetching tags: {e}")
        return {}

def generate_wiki():
    logging.info("Starting Wiki Generation...")
    
    # Fetch Tag Map (ID -> Name)
    tag_id_map = get_tags()
    logging.info(f"Loaded {len(tag_id_map)} tags.")

    # 1. Ensure Directory Structure & Indices
    # Use Emojis for Lark-like visual hierarchy
    structure_paths = [
        "🏥 Thiết bị y tế",
        "🏥 Thiết bị y tế/🖼️ Chẩn đoán hình ảnh",
        "🏥 Thiết bị y tế/🖼️ Chẩn đoán hình ảnh/🦴 X-Quang",
        "🏥 Thiết bị y tế/🖼️ Chẩn đoán hình ảnh/🌀 CT Scanner",
        "🏥 Thiết bị y tế/🖼️ Chẩn đoán hình ảnh/🧲 MRI",
        "🏥 Thiết bị y tế/🖼️ Chẩn đoán hình ảnh/🌊 Siêu âm", 
        "🏥 Thiết bị y tế/🔭 Nội soi",
        "🏥 Thiết bị y tế/🔭 Nội soi/🤢 Nội soi dạ dày",
        "🏥 Thiết bị y tế/🛡️ Kiểm soát nhiễm khuẩn",
        "🏥 Thiết bị y tế/🛡️ Kiểm soát nhiễm khuẩn/🔥 Máy tiệt trùng",
        "🏥 Thiết bị y tế/🚑 Hồi sức cấp cứu (ICU)"
    ]

    for path_str in structure_paths:
        path = WIKI_ROOT / path_str
        path.mkdir(parents=True, exist_ok=True)
        # Create index with the folder name as title
        create_category_index(path, path_str.split('/')[-1])

    # 2. Sync Documents
    docs = get_documents()
    logging.info(f"Found {len(docs)} documents to sync.")
    
    # Structure mapping (Tag -> User-friendly Folder)
    tag_map = {
        # Chẩn đoán hình ảnh
        "x_quang": "🏥 Thiết bị y tế/🖼️ Chẩn đoán hình ảnh/🦴 X-Quang",
        "ct_scanner": "🏥 Thiết bị y tế/🖼️ Chẩn đoán hình ảnh/🌀 CT Scanner",
        "mri": "🏥 Thiết bị y tế/🖼️ Chẩn đoán hình ảnh/🧲 MRI",
        "sieu_am": "🏥 Thiết bị y tế/🖼️ Chẩn đoán hình ảnh/🌊 Siêu âm",
        
        # Nội soi
        "noi_soi_da_day": "🏥 Thiết bị y tế/🔭 Nội soi/🤢 Nội soi dạ dày",
        
        # Kiểm soát nhiễm khuẩn
        "may_tiet_trung": "🏥 Thiết bị y tế/🛡️ Kiểm soát nhiễm khuẩn/🔥 Máy tiệt trùng",
        
        # Hồi sức cấp cứu
        "hoi_suc_cap_cuu": "🏥 Thiết bị y tế/🚑 Hồi sức cấp cứu (ICU)",
        "may_tho": "🏥 Thiết bị y tế/🚑 Hồi sức cấp cứu (ICU)",
        "monitor": "🏥 Thiết bị y tế/🚑 Hồi sức cấp cứu (ICU)"
    }

    # Prepare lists for indices
    category_content = {k: [] for k in tag_map.values()}
    category_content["Inbox (Chưa phân loại)"] = []

    for doc in docs:
        metadata = generate_frontmatter(doc)
        doc_id = metadata['device_id']
        title = metadata['model']
        
        # Determine Path
        target_folder = "Inbox (Chưa phân loại)"
        
        # Resolve Tag IDs to Names
        doc_tags = metadata['tags'] # List of IDs
        tag_names = []
        logging.info(f"Doc {doc_id} raw tags: {doc_tags}") 
        
        for t_id in doc_tags:
            if isinstance(t_id, int) and t_id in tag_id_map:
                tag_names.append(tag_id_map[t_id])
            elif isinstance(t_id, dict):
                 tag_names.append(t_id.get('name', ''))
            else:
                 tag_names.append(str(t_id))
        
        
        for tag_name in tag_names:
            slug_tag = slugify(tag_name)
            if slug_tag in tag_map:
                target_folder = tag_map[slug_tag]
                break
        
        # Create MD Content
        file_name = f"{doc_id}_{slugify(title)}.md"
        if target_folder == "Inbox (Chưa phân loại)":
             # Create uncategorized folder if not exists
             (WIKI_ROOT / "Inbox (Chưa phân loại)").mkdir(exist_ok=True)
             
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
            # Ensure folder exists (Auto-create for any new tag)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
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
        
        # Prepare content list
        list_content = "\n".join(links)
        
        if index_path.exists():
            current_content = index_path.read_text(encoding='utf-8')
            # Simple overwrite for Demo:
            if "## 📋 Danh sách thiết bị" in current_content:
                base_header = current_content.split("## 📋 Danh sách thiết bị")[0]
            else:
                # Fallback Title
                clean_title = folder.replace('_', ' ').split('/')[-1].title()
                # Direct Lookup
                # if folder in structure: -- Removed as folder is now the title itself
                #    clean_title = structure[folder]
                
                base_header = f"# {clean_title}\n\n"

            new_content = f"{base_header}## 📋 Danh sách thiết bị\n{list_content}\n\n## 📊 Thống kê"
            index_path.write_text(new_content, encoding='utf-8')
            logging.info(f"Updated index for {folder}")
        else:
            # Create new index if not exists
            clean_title = folder.replace('_', ' ').split('/')[-1].title()
            
            new_content = f"""# {clean_title}

## 📋 Danh sách thiết bị
{list_content}

## 📊 Thống kê
- **Tổng số:** {len(links)}
"""
            index_path.write_text(new_content, encoding='utf-8')
            logging.info(f"Created new index for {folder}")
    
    logging.info("Wiki Generation Complete.")

if __name__ == "__main__":
    generate_wiki()
