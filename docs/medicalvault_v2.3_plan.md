# KẾ HOẠCH TRIỂN KHAI CHI TIẾT: MEDICALVAULT BOT v2.3

**Phiên bản**: 2.3 (Thay thế v2.2)
**Ngày lập**: 16/02/2026
**Mục tiêu**: Xây dựng hệ thống quản lý thiết bị y tế "MedicalVault" với kiến trúc Scalable (40TB), tìm kiếm thông minh (AI/Vector) và tự động hóa quy trình Ingestion.

---

## 1. Kiến trúc Hệ thống (System Architecture)

### 1.1. Hạ tầng Lưu trữ (Host-based Storage)
Chúng ta chuyển từ Docker Volumes ẩn sang cấu trúc thư mục phẳng trên Host (Mac Mini) để dễ dàng quản lý, backup và mở rộng.

**Cấu trúc thư mục (`/Users/phongsun/MedicalVault/`):**
```text
MedicalVault/
├── MedicalDevicesVault/          # ⭐ KHO DỮ LIỆU CHÍNH (Bind Mount vào Container)
│   ├── INBOX/                    # Nơi drop file PDF để xử lý
│   ├── Chan_doan_hinh_anh/       # File đã phân loại (Category)
│   │   ├── x_quang/              # Sub-category
│   │   └── ...
│   ├── chroma/                   # Dữ liệu Vector DB (Persist)
│   ├── devices.db                # SQLite Metadata (FTS5)
│   └── config.yaml               # File cấu hình mapping hãng/loại máy
└── medicalvault-wiki/            # MkDocs Source (Git Repo riêng)
    ├── docs/                     # Các file Markdown (model_*.md)
    └── mkdocs.yml
```

### 1.2. Các Service (Docker Compose)
Hệ thống gồm 4 service chính giao tiếp qua mạng nội bộ Docker (`backend` network):

1.  **OPENCLAW (Logic Core)**:
    -   **Vai trò**: Quản lý logic nghiệp vụ, giao tiếp Telegram, điều phối dữ liệu.
    -   **Nhiệm vụ**: Nhận JSON từ Kreuzberg -> Ghi DB -> Tạo Markdown -> Git Commit.

2.  **KREUZBERG (AI worker)**:
    -   **Vai trò**: Service xử lý nặng (OCR, Extraction).
    -   **Nhiệm vụ**: Watcher `INBOX` -> OCR -> Extract Metadata (Vendor, Specs) -> Output JSON.

3.  **Databases**:
    -   **SQLite**: Lưu metadata có cấu trúc (Model, Hãng, Năm, Giá, Project). Dùng cho filter chính xác.
    -   **ChromaDB**: Lưu vector embedding của mô tả thiết bị. Dùng cho Semantic Search ("/search máy chụp mạch máu não").

4.  **Frontend**:
    -   **MkDocs**: Static Site Generator, reload khi file `.md` thay đổi.
    -   **Telegram Client**: Giao diện người dùng chính.

---

## 2. Quy trình Xử lý Dữ liệu (Data Pipeline)

### Bước 1: Ingestion (KREUZBERG)
1.  **Watcher**: Lắng nghe sự kiện file mới tại `MedicalDevicesVault/INBOX/`.
2.  **Classification**: Dùng `config.yaml` và AI để xác định:
    *   Category: `chan_doan_hinh_anh/x_quang`
    *   Vendor: `GE`
    *   Model: `Optima XR220`
3.  **Extraction**: Trích xuất thông số kỹ thuật (Công suất, Kích thước) từ PDF.

### Bước 2: Processing & Storage (OPENCLAW)
1.  **Move File**: Di chuyển PDF từ `INBOX` -> `MedicalDevicesVault/chan_doan_hinh_anh/x_quang/GE_Optima_XR220/`.
2.  **Update DB**:
    *   Insert/Update `devices.db` (SQLite).
    *   Upsert Vector vào `ChromaDB`.
3.  **Generate Wiki**:
    *   Tạo file `wiki/docs/chan_doan_hinh_anh/x_quang/ge_optima_xr220.md` từ template.
    *   Cập nhật `index.md` của thư mục cha.

### Bước 3: Access & Search (Telegram/Wiki)
1.  **Telegram**: Người dùng gõ `/search x-quang ge`.
    *   Bot query SQLite (Full-text) + ChromaDB (Semantic).
    *   Trả về Top 3 kết quả + Link Wiki.
2.  **Wiki**: Người dùng xem bảng so sánh thông số chi tiết trên web.

---

## 3. Lộ trình Triển khai (Roadmap)

### Phase 1: Core Pipeline (Tuần 1-2)
**Mục tiêu**: **“Thả file vào, Wiki tự hiện ra”**

- [ ] **Setup**:
    - [ ] Tạo cấu trúc thư mục trên Host.
    - [ ] Viết `docker-compose.yml` v2.3 (Bind mounts).
    - [ ] Tạo `config.yaml` 25 categories cơ bản.
- [ ] **KREUZBERG Dev**:
    - [ ] Code `watcher.py` (Watchdog library).
    - [ ] Code `parser.py` (PyPDF2 + OpenAI API/Gemini Flash).
- [ ] **OPENCLAW Dev**:
    - [ ] Code `storage.py` (File operations).
    - [ ] Code `mkdocs_gen.py` (Markdown Template render).

### Phase 2: Search Intelligence (Tuần 3)
**Mục tiêu**: **“Hỏi gì cũng biết”**

- [ ] **Database Integration**:
    - [ ] Setup Schema SQLite (`models`, `files`, `projects`).
    - [ ] Setup ChromaDB Client.
- [ ] **Telegram Bot Upgrade**:
    - [ ] Command `/search` (Hybrid Search).
    - [ ] Command `/reclassify` (Sửa sai manual).
    - [ ] Command `/status` (Thống kê hệ thống).

### Phase 3: Reliability & Optimization (Tuần 4)
**Mục tiêu**: **“Chạy ổn định, không mất dữ liệu”**

- [ ] **Backup Strategy**: Script `rsync` định kỳ sang ổ cứng ngoài/Cloud.
- [ ] **Error Handling**: Cơ chế Retry khi Ingest lỗi, thư mục `FAILED_INBOX`.
- [ ] **Performance**: Tối ưu Ingest (<10s/file), Search (<1s).

---

## 4. Đặc tả API & Cấu hình (Specs)

### 4.1. Config Schema (`config.yaml`)
```yaml
categories:
  chan_doan_hinh_anh:
    - x_quang: ["GE", "Siemens", "Philips"]
    - ct: ...
  hoi_suc_cap_cuu:
    - may_tho: ["Drager", "Maquet"]
```

### 4.2. Database Schema (SQLite)
```sql
CREATE TABLE models (
    slug TEXT PRIMARY KEY,
    vendor TEXT,
    model_name TEXT,
    category_path TEXT,
    risk_class TEXT,
    full_text_search TEXT -- FTS5 content
);
```

### 4.3. Telegram Commands
- `/search <query>`: Tìm kiếm tổng hợp.
- `/files <model_slug>`: Liệt kê file PDF của model đó.
- `/stats`: Xem tổng số Model/File đã index.
- `/fix <file_id> <new_category>`: Chuyển category nếu AI nhận diện sai.

---

## 5. Yêu cầu Tài nguyên
- **Host**: Mac Mini (đã có).
- **Disk**: SSD ngoài cho `MedicalDevicesVault` (Khuyến nghị SSD NVMe để search vector nhanh).
- **API Key**: OpenAI (GPT-4o) hoặc Google Gemini Flash (Rẻ, context lớn).

---

**Kết luận**: Plan v2.3 tập trung tối đa vào **tính bền vững dữ liệu** (Host storage) và **khả năng mở rộng tìm kiếm** (Vector DB), loại bỏ các phụ thuộc phức tạp của phiên bản cũ.
