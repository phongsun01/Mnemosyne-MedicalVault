# PHỤ LỤC KỸ THUẬT: MedicalVault Bot v2.2

## 1. Hệ thống Lưu trữ & Volumes

### Cấu trúc Thư mục Host (Mac Mini)
```text
/Users/phongsun/MedicalVault/
├── MedicalDevicesVault/          # Kho dữ liệu chính (Scalable: 4GB -> 40TB)
│   ├── INBOX/                    # ⭐ Drop files vào đây để xử lý
│   ├── Chan_doan_hinh_anh/       # Phân loại tự động
│   ├── chroma/                   # Dữ liệu ChromaDB (Vector DB)
│   ├── devices.db                # SQLite FTS5 (Full-text search)
│   └── config.yaml               # Cấu hình Mapping Categories
└── medicalvault-wiki/            # MkDocs Repository (Git sync)
    ├── docs/                     # Chứa các file model_*.md
    └── mkdocs.yml                # Cấu hình Wiki
```

### Docker Volume Mapping
```yaml
services:
  openclaw:
    volumes:
      - /Users/phongsun/MedicalVault/MedicalDevicesVault:/app/vault
      - /Users/phongsun/MedicalVault/medicalvault-wiki:/app/wiki
  kreuzberg:
    volumes:
      - /Users/phongsun/MedicalVault/MedicalDevicesVault:/app/vault
  chromadb:
    volumes:
      - /Users/phongsun/MedicalVault/MedicalDevicesVault/chroma:/chroma
  mkdocs:
    volumes:
      - /Users/phongsun/MedicalVault/medicalvault-wiki:/docs
```

## 2. Schema Dữ liệu & Cấu hình

### Config Mapping (`config.yaml`)
Dựa trên Thông tư 30/2015/TT-BYT, chia làm 25 categories.
```yaml
categories:
  chan_doan_hinh_anh:
    - x_quang: ["GE", "Siemens", "Philips"]
    - ct: ["GE", "Toshiba", "Siemens"]
    - mri: ["GE", "Philips"]
  kiem_soat_nhiem_khuan:
    - may_tiet_trung: ["Getinge", "Steris"]
  noi_soi:
    - hoya_ep_exera: ["Hoya"]
```

### Model Markdown Template (`model_*.md`)
```markdown
---
vendor: GE
model: Optima XR220
category: chan_doan_hinh_anh/x_quang
year: 2018
risk_class: IIb
power_kw: 50
files:
  - ky_thuat/brochure.pdf
  - thong_so/spec.pdf
---

# GE Optima XR220

## Thông số chính
| Thông số | Giá trị |
|----------|---------|
| Công suất | 50kW |
| Kích thước | 2.5x1.8m |
| Trọng lượng | 1200kg |

## Tài liệu
- [Brochure kỹ thuật](ky_thuat/brochure.pdf)
- [Thông số chi tiết](thong_so/spec.pdf)
```

## 3. Cấu trúc API & Lệnh Telegram

### FastAPI Endpoints (Internal)
- `POST /ingest`: Xử lý file mới từ `INBOX`.
  - Input: `{"file_path": "..."}`
  - Output: `{"model_slug": "...", "wiki_url": "..."}`
- `GET /search`: Tìm kiếm thiết bị.
  - Query: `q=...&limit=...`
  - Output: JSON danh sách thiết bị + score.
- `POST /reclassify`: Sửa lại phân loại thủ công.

### Telegram Commands
- `/search <keyword>`: Tìm kiếm thiết bị (VD: `/search x-quang ge`). Trả về Top 3 + Link Wiki.
- `/status`: Xem trạng thái hệ thống (Số lượng files, models, độ chính xác).
- `/reclassify <filename> <category_path>`: Phân loại lại file sai.

## 4. Pipeline Xử lý Dữ liệu (I/O)

### Bước 1: File Watcher -> KREUZBERG (AI Service)
- **Input**: File PDF mới trong `INBOX`.
- **Process**: OCR + Trích xuất thông tin (Text, Tables, Metadata).
- **Output**: JSON chứa dữ liệu thô.

### Bước 2: KREUZBERG -> OPENCLAW (Logic Service)
- **Input**: JSON từ bước 1.
- **Process**:
  - Xác định Category path (dựa trên `config.yaml`).
  - Tạo slug model.
  - Chuẩn hóa metadata (Markdown fields, DB fields).
  - Tạo Embedding text cho Vector DB.
- **Output**: Dữ liệu đã chuẩn hóa.

### Bước 3: OPENCLAW -> Persistence Layers
- **ChromaDB**: Lưu embedding (`id=model_slug`, `document=text`).
- **SQLite**: Lưu metadata (`devices` table).
- **MkDocs**: Tạo/Cập nhật file `.md`, move file PDF vào folder đích, commit git.

## 5. Ràng buộc & Ưu tiên

### Hiệu năng
- **Ingest**: 5-10s/file (Chấp nhận chậm hơn vào ban đêm).
- **Search**: < 1s (Dùng Llama3 local hoặc optimize query).
- **Scale**: Kiến trúc phải hỗ trợ mở rộng volume lên 40TB.

### An toàn dữ liệu (Persistence Rules)
- **CRITICAL**: Dữ liệu phải được ghi xuống đĩa ngay lập tức (Bind mounts).
  - Vault, ChromaDB, SQLite, MkDocs source.
- **Stateful**: Container restart phải resume được công việc.
- **Backup**: Script backup hàng ngày (`rsync`, `git commit`).

### Lộ trình Ưu tiên (Coding)
1. **Phase 1**: File Watcher + Ingest Pipeline + Basic Search.
2. **Phase 1**: Telegram Bot Search cơ bản.
3. **Phase 2**: MkDocs Auto-build & Obsidian Sync.
