# KẾ HOẠCH TRIỂN KHAI: MEDICALVAULT v2.4

**Phiên bản**: 2.4 (Core Foundation + Optional Graphiti Plugin)  
**Ngày lập**: 16/02/2026  
**Chiến lược**: Chậm mà chắc - Core pipeline hoàn thiện trước, Graphiti plugin sau  
**Tài nguyên**: Mac Mini 24GB RAM, Box Cloud Storage

---

## 1. TRIẾT LÝ V2.4: "Foundation First"

### 1.1. Mục tiêu Chính
- **v2.4 (Tuần 1-6)**: Xây dựng **Core Pipeline** vững chắc (Ingest + Search + Wiki)
- **v2.5 (Tuần 7-12)**: Thêm **Graphiti Plugin** cho advanced reasoning (tùy chọn)

### 1.2. Nguyên tắc Thiết kế
1. **Modular Architecture**: Graphiti là plugin, không phải core dependency
2. **Graceful Degradation**: Hệ thống hoạt động tốt ngay cả khi Graphiti tắt
3. **Cost-Conscious**: Ollama (free) cho MVP, Gemini/OpenAI cho production

---

## 2. KIẾN TRÚC HỆ THỐNG

### 2.1. Cấu trúc Thư mục (Box Cloud)
```text
/Users/xitrum/Library/CloudStorage/Box-Box/Tai lieu - Phong/Study2/Antigravity/ThanhGiong/
├── docker_paperless/              # Paperless-ngx (hiện tại)
├── MedicalDevicesVault/          # ⭐ VAULT MỚI (Core storage)
│   ├── INBOX/                    # Drop zone
│   ├── devices/                  # Phân loại theo category
│   │   ├── chan_doan_hinh_anh/
│   │   ├── hoi_suc_cap_cuu/
│   │   └── ...
│   ├── chroma/                   # ChromaDB data
│   ├── graphiti/                 # ⭐ OPTIONAL: Neo4j data (v2.5)
│   ├── devices.db                # SQLite
│   └── config.yaml
├── medicalvault-wiki/            # MkDocs source
└── docker/                       # Services mới (v2.4)
    ├── docker-compose.yml
    ├── kreuzberg/                # AI Service
    ├── openclaw/                 # Logic Service
    └── ollama/                   # Local LLM
```

### 2.2. Services (Docker Compose v2.4)
```yaml
services:
  # --- Phase 1: Core Services (v2.4) ---
  openclaw:
    build: ./openclaw
    volumes:
      - ../MedicalDevicesVault:/app/vault
      - ../medicalvault-wiki:/app/wiki
    environment:
      - GRAPHITI_ENABLED=false  # ⭐ Tắt mặc định
    depends_on:
      - sqlite
      - chromadb
      - kreuzberg

  kreuzberg:
    build: ./kreuzberg
    volumes:
      - ../MedicalDevicesVault:/app/vault
    environment:
      - LLM_PROVIDER=ollama
      - OLLAMA_BASE_URL=http://ollama:11434

  sqlite:
    image: nouchka/sqlite3:latest
    volumes:
      - ../MedicalDevicesVault:/data

  chromadb:
    image: chromadb/chroma:latest
    volumes:
      - ../MedicalDevicesVault/chroma:/chroma/chroma
    environment:
      - ANONYMIZED_TELEMETRY=false

  ollama:
    image: ollama/ollama:latest
    volumes:
      - ollama_models:/root/.ollama
    command: serve

  mkdocs:
    image: squidfunk/mkdocs-material:latest
    volumes:
      - ../medicalvault-wiki:/docs
    ports:
      - "8001:8000"

  # --- Phase 2: Graphiti Plugin (v2.5) ---
  # Uncomment khi cần
  # neo4j:
  #   image: neo4j:5.15-community
  #   volumes:
  #     - ../MedicalDevicesVault/graphiti/data:/data
  #   environment:
  #     - NEO4J_dbms_memory_heap_max__size=6G
  #     - NEO4J_dbms_memory_pagecache_size=3G

volumes:
  ollama_models:
```

### 2.3. Resource Allocation (24GB RAM)
| Service | RAM | CPU | Priority |
|---------|-----|-----|----------|
| Paperless-ngx | 4GB | 2 cores | HIGH |
| PostgreSQL | 2GB | 1 core | HIGH |
| ChromaDB | 2GB | 1 core | MEDIUM |
| Ollama | 8GB | 4 cores | MEDIUM |
| OPENCLAW | 1GB | 1 core | MEDIUM |
| KREUZBERG | 2GB | 2 cores | MEDIUM |
| **Buffer** | **3GB** | - | - |
| **TOTAL** | **22GB** | **11 cores** | - |

*Graphiti (v2.5): +6GB khi bật*

---

## 3. DATA SCHEMA & ENTITIES

### 3.1. Config Mapping (config.yaml)
```yaml
version: "2.4"
categories:
  chan_doan_hinh_anh:
    x_quang:
      vendors: [GE, Siemens, Philips]
      tags: [digital-radiography, dr-panel, fda-approved]
    ct_scanner:
      vendors: [GE, Toshiba, Siemens, Philips]
    mri:
      vendors: [GE, Siemens, Philips]
  hoi_suc_cap_cuu:
    may_tho:
      vendors: [Drager, Maquet, Hamilton]
    monitor:
      vendors: [Philips, GE, Mindray]
  # ... 23 categories khác
```

### 3.2. SQLite Schema (v2.4)
```sql
-- Core tables
CREATE TABLE devices (
    slug TEXT PRIMARY KEY,
    model_name TEXT NOT NULL,
    vendor TEXT,
    category_path TEXT,
    risk_class TEXT,
    year INTEGER,
    price_min_usd REAL,
    price_max_usd REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_slug TEXT,
    filename TEXT,
    file_type TEXT, -- brochure, manual, spec
    path TEXT,
    FOREIGN KEY (device_slug) REFERENCES devices(slug)
);

CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_slug TEXT,
    hospital_name TEXT,
    deployment_date DATE,
    budget_usd REAL,
    status TEXT,
    FOREIGN KEY (device_slug) REFERENCES devices(slug)
);

-- FTS5 for full-text search
CREATE VIRTUAL TABLE devices_fts USING fts5(
    model_name, vendor, category_path, specs_text,
    content=devices
);

-- v2.5: Thêm cột này khi enable Graphiti
-- ALTER TABLE devices ADD COLUMN graphiti_node_id TEXT;
```

---

## 4. CORE PIPELINE (V2.4)

### 4.1. Ingestion Workflow
```
PDF in INBOX
    ↓
[1] KREUZBERG: OCR + Extract
    ↓
[2] KREUZBERG: Classify (Ollama Llama3)
    ↓
[3] OPENCLAW: Validate + Store
    ↓
[4] OPENCLAW: Move file to /devices/category/
    ↓
[5] Update: SQLite + ChromaDB + Wiki
```

### 4.2. Search Workflow (v2.4)
```
User Query (Telegram /search)
    ↓
[1] SQLite FTS5 (exact match)
    ↓
[2] ChromaDB (semantic similarity)
    ↓
[3] Reciprocal Rank Fusion
    ↓
Return Top 5 + Wiki links
```

### 4.3. KREUZBERG: AI Extraction (parser.py)
```python
import ollama

async def extract_metadata(pdf_path: str) -> dict:
    """Extract device metadata using Ollama Llama3"""
    
    # 1. OCR
    text = await ocr_pdf(pdf_path)
    
    # 2. Classify with Ollama
    prompt = f"""
    Classify this medical device brochure:
    {text[:2000]}
    
    Extract:
    - Vendor (GE, Siemens, etc.)
    - Model name
    - Category (x_quang, ct_scanner, mri, etc.)
    - Specs (power, weight, dimensions)
    
    Output JSON only.
    """
    
    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}]
    )
    
    metadata = json.loads(response['message']['content'])
    
    return {
        "device": metadata,
        "raw_text": text,
        "confidence": 0.9  # Placeholder
    }
```

### 4.4. OPENCLAW: Storage Logic (storage.py)
```python
class DevicePipeline:
    def __init__(self):
        self.sqlite = SQLiteManager("vault/devices.db")
        self.chroma = ChromaClient(path="vault/chroma")
        self.graphiti = None  # v2.5
        
    async def process_device(self, metadata: dict):
        device = metadata["device"]
        slug = self.generate_slug(device)
        
        # 1. SQLite
        self.sqlite.upsert_device({
            "slug": slug,
            "model_name": device["model"],
            "vendor": device["vendor"],
            "category_path": device["category"]
        })
        
        # 2. ChromaDB
        self.chroma.add(
            ids=[slug],
            documents=[metadata["raw_text"]],
            metadatas=[device]
        )
        
        # 3. Move file
        dest = f"vault/devices/{device['category']}/{slug}/"
        shutil.move(metadata["pdf_path"], dest)
        
        # 4. Generate Wiki
        self.generate_wiki(device)
        
        # 5. (Optional) Graphiti
        if self.graphiti:
            await self.graphiti.add_episode(...)
```

---

## 5. LỘ TRÌNH TRIỂN KHAI

### PHASE 1: Setup & Infra (Tuần 1-2)
**Mục tiêu**: Môi trường sẵn sàng, data flow cơ bản

- [ ] **Week 1: Docker & Storage**
    - [ ] Tạo thư mục `MedicalDevicesVault/` trong Box Cloud
    - [ ] Viết `docker-compose.yml` cho v2.4 (không có Graphiti)
    - [ ] Deploy Ollama, pull model `llama3.2:3b`
    - [ ] Test Ollama: `ollama run llama3.2 "Hello"`
    - [ ] Tạo `config.yaml` với 5 categories test

- [ ] **Week 2: Database Setup**
    - [ ] Tạo SQLite schema (`init.sql`)
    - [ ] Setup ChromaDB collection `medical_devices`
    - [ ] Script kiểm tra: Insert 1 device thủ công → Verify search

### PHASE 2: Core Pipeline (Tuần 3-4)
**Mục tiêu**: Ingest tự động từ INBOX

- [ ] **Week 3: KREUZBERG Development**
    - [ ] Code `watcher.py` (watchdog library)
    - [ ] Code `ocr.py` (PyPDF2 + pytesseract)
    - [ ] Code `parser.py` (Ollama integration)
    - [ ] Test: 5 PDF mẫu → Extract metadata → Verify JSON

- [ ] **Week 4: OPENCLAW Development**
    - [ ] Code `storage.py` (SQLite + ChromaDB write)
    - [ ] Code `wiki_generator.py` (Jinja2 template)
    - [ ] Code `file_mover.py` (organize by category)
    - [ ] End-to-end test: INBOX → Auto-process → Wiki cập nhật

### PHASE 3: Search & Bot (Tuần 5-6)
**Mục tiêu**: Telegram bot hoạt động

- [ ] **Week 5: Search Engine**
    - [ ] Code `search.py` (SQLite FTS5 + ChromaDB query)
    - [ ] Implement RRF (Reciprocal Rank Fusion)
    - [ ] API endpoint `/search?q=...`
    - [ ] Benchmark: <1s latency với 100 devices

- [ ] **Week 6: Telegram Bot**
    - [ ] Commands: `/search`, `/stats`, `/recent`
    - [ ] Format response: Top 5 + Wiki links
    - [ ] Error handling: Fallback nếu ChromaDB down
    - [ ] Deploy + Test với users thật

---

### PHASE 4: V2.5 - Graphiti Plugin (Tuần 7-12)
**Mục tiêu**: Advanced reasoning (tùy chọn)

- [ ] **Week 7-8: Graphiti Setup**
    - [ ] Deploy Neo4j + OpenSearch trong docker-compose
    - [ ] Viết `graphiti_client.py` wrapper
    - [ ] Define entities: MedicalDevice, Vendor, Project
    - [ ] Migrate 100 thiết bị hiện có → Graph

- [ ] **Week 9-10: Hybrid Search**
    - [ ] Update `search.py`: SQLite + Chroma + Graphiti
    - [ ] New commands: `/related`, `/ecosystem`
    - [ ] A/B test: So sánh accuracy

- [ ] **Week 11-12: Production Ready**
    - [ ] Backup strategy: Neo4j dump
    - [ ] Monitoring: Grafana dashboard
    - [ ] Docs: User guide + Admin guide

---

## 6. LLM STRATEGY

### Phase 1 (v2.4): Ollama (Free)
- **Model**: `llama3.2:3b` (< 4GB VRAM)
- **Use case**: Classification, simple extraction
- **Pros**: Miễn phí, privacy
- **Cons**: Chậm (~5-10s/file), accuracy 85%

### Phase 2 (v2.5): Gemini/OpenAI (Paid)
- **Model**: `gemini-1.5-flash` hoặc `gpt-4o-mini`
- **Use case**: Entity extraction cho Graphiti
- **Cost**: ~$0.01/file → $15 cho 1500 files
- **Pros**: Nhanh (<2s), accuracy 95%

### Hybrid Config (openclaw/config.py)
```python
LLM_CONFIG = {
    "classification": "ollama",  # Free
    "entity_extraction": "gemini",  # Chỉ khi Graphiti enabled
    "fallback": "ollama"
}
```

---

## 7. RỦI RO & MITIGATION

| Rủi ro | Tác động | Giải pháp |
|---------|----------|-----------|
| Ollama quá chậm | MEDIUM | Cache results, xử lý batch ban đêm |
| Box Cloud sync conflict | HIGH | Dùng `.boxignore` cho `chroma/`, `graphiti/` |
| RAM overflow (24GB) | MEDIUM | Monitor, giảm heap size nếu cần |
| Graphiti learning curve | LOW | V2.5 tùy chọn, không bắt buộc |

---

## 8. METRICS & KPI

### v2.4 Success Criteria
- ✅ Ingest: <15s/file (Ollama OK)
- ✅ Search: <1s latency
- ✅ Wiki: Auto-update trong 30s
- ✅ Uptime: 99% (Docker auto-restart)

### v2.5 Success Criteria (Optional)
- ✅ Graph query: <500ms
- ✅ Multi-hop reasoning working
- ✅ Cost: <$50/month

---

## 9. MIGRATION PATH

### Từ v2.3 sang v2.4
1. Tạo thư mục `MedicalDevicesVault/`
2. Deploy Docker Compose v2.4
3. Import 20 devices test
4. Verify search + wiki
5. Migrate toàn bộ Paperless docs (background job)

### Từ v2.4 sang v2.5
1. Uncomment Neo4j/OpenSearch trong docker-compose
2. Set `GRAPHITI_ENABLED=true`
3. Run migration script
4. Test `/related` command
5. Monitor performance 1 tuần

---

## 10. CHECKLIST HOÀN THIỆN

### v2.4 MVP (6 tuần)
- [ ] Docker environment running
- [ ] 100 devices ingested
- [ ] Telegram `/search` working
- [ ] Wiki auto-generated
- [ ] Documentation: README + User Guide

### v2.5 Production (12 tuần)
- [ ] Graphiti plugin enabled
- [ ] 1000+ devices + relationships
- [ ] Advanced commands working
- [ ] Backup/restore tested
- [ ] Monitoring dashboard live

---

**Kết luận v2.4**: Tập trung vào **foundation vững chắc** với SQLite + ChromaDB + Ollama. Graphiti là cherry on top, không phải yêu cầu bắt buộc. Chiến lược "Chậm mà chắc" đảm bảo mỗi bước đều kiểm soát được.
