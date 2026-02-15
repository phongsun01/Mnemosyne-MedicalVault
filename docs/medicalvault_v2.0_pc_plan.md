# 📋 MEDICALVAULT BOT v2.0 - PC EDITION

**Hệ thống quản lý hồ sơ thiết bị y tế cho team 3-5 người**

- **Stack:** PC 24/7 + Docker + Gemini 2.0 + ChromaDB + Outline Wiki
- **Chi phí:** 0đ đầu tư + 100-300k/tháng API
- **Timeline:** 4-6 tuần → MVP live

---

## 🎯 MỤC TIÊU & ROI

### Vấn đề hiện tại
- 1500 files (3.7GB) lộn xộn trong Explorer/Drive.
- Tìm brochure/specs phải mò 5-10 phút.
- Gửi tài liệu cho khách hàng phải search manual.
- So sánh thiết bị phải mở nhiều file PDF.
- Không biết giá/specs nhanh.

### Sau khi triển khai
- **Search 3 giây:** "máy xquang GE" → list đầy đủ + specs + giá.
- **Gửi khách hàng:** Copy link wiki hoặc export PDF tự động.
- **So sánh:** Bảng specs 3-5 thiết bị tự động generate.
- **Extract auto:** OCR → giá, thông số → MD file.
- **Remote:** Telegram search ở mọi nơi.

### ROI
- **Tiết kiệm:** 20-30 phút/ngày × 3 người = 1.5h/ngày.
- **Giá trị:** 30 giờ/tháng × 500k/giờ = 15 triệu/tháng.
- **Chi phí:** 100-300k/tháng API.
- **ROI:** 50-150x.

---

## 🏗️ KIẾN TRÚC ĐƠN GIẢN HÓA

```text
┌─────────────────────────────────────────┐
│         PC 24/7 (Windows/Linux)         │
│                                         │
│  ┌─────────────┐    ┌────────────────┐ │
│  │ Docker      │    │ File Watcher   │ │
│  │ Compose     │◄───┤ (watchdog)     │ │
│  └──────┬──────┘    └────────────────┘ │
│         │                               │
│  ┌──────▼──────────────────────────┐   │
│  │  CORE SERVICES (containers)     │   │
│  │                                  │   │
│  │  • ChromaDB (vector search)     │   │
│  │  • Outline Wiki (team UI)       │   │
│  │  • FastAPI Backend              │   │
│  │  • PostgreSQL (metadata)        │   │
│  │  • Telegram Bot (remote)        │   │
│  └──────────────────────────────────┘   │
│                                         │
│  ┌──────────────────────────────────┐   │
│  │  STORAGE (ổ phụ)                │   │
│  │  • /vault/raw/  (PDFs, files)   │   │
│  │  • /vault/md/   (markdown DB)   │   │
│  │  • /vault/backup/ (daily)       │   │
│  └──────────────────────────────────┘   │
└─────────────────────────────────────────┘
           │
           ├──► Gemini 2.0 Flash (OCR + Extract)
           └──► Groq (classify nhanh, free tier)
```

**ACCESS:**
- **LAN:** `http://pc-ip:3000` (Outline Wiki)
- **Remote:** Telegram Bot (`@medvault_bot`)
- **Edit:** Obsidian sync với `/vault/md/`

---

## 📁 VAULT STRUCTURE (Đơn Giản)

```text
D:/MedicalVault/              # Ổ phụ của bạn
├── raw/                      # Files gốc
│   ├── Chan_doan_hinh_anh/
│   │   └── X_quang/
│   │       ├── GE_Optima_XR220_brochure.pdf
│   │       ├── GE_Optima_XR220_specs.xlsx
│   │       └── GE_Optima_XR220_price_2025.pdf
│   └── Sieu_am/
│       └── ...
│
├── md/                       # Markdown database (Obsidian)
│   ├── devices/
│   │   ├── X_quang_GE_Optima_XR220.md
│   │   ├── Sieu_am_Mindray_DC70.md
│   │   └── ...
│   ├── templates/
│   │   └── device_template.md
│   └── _index/
│       └── by_category.md
│
├── docker/                   # Docker configs
│   ├── docker-compose.yml
│   ├── .env
│   └── configs/
│
└── backup/                   # Auto backup
    ├── 2026-02-13/
    └── ...
```

---

## 📄 MARKDOWN FILE STRUCTURE (Auto-Generate)

**File:** `md/devices/X_quang_GE_Optima_XR220.md`

```markdown
---
device_id: "xray-ge-optima-xr220"
model: "GE Optima XR220"
brand: "GE Healthcare"
category: "Chẩn đoán hình ảnh/X-quang"
subcategory: "X-quang kỹ thuật số DR"

# THÔNG SỐ KỸ THUẬT (Auto-extracted)
specs:
  power: "400mA"
  voltage: "150kV"
  detector: "CsI scintillator 17×17 inch"
  resolution: "3.5 lp/mm"
  
# GIÁ CẢ (Auto-extracted)
pricing:
  price_range_vnd: [5200000000, 6500000000]
  last_updated: "2025-11-15"
  source: "Danh mục thầu BV Bạch Mai"

# FILES ĐÍNH KÈM
attachments:
  - file: "GE_Optima_XR220_brochure.pdf"
    type: "Tài liệu kỹ thuật"
    pages: 24
    language: "en"
  - file: "GE_Optima_XR220_specs.xlsx"
    type: "Bảng thông số"
  - file: "GE_Optima_XR220_price_2025.pdf"
    type: "Báo giá"
    hospital: "Bệnh viện Bạch Mai"

# METADATA
created: "2026-02-13"
updated: "2026-02-13"
confidence: 0.95
status: "verified"
---

# GE Optima XR220 - X-quang Kỹ Thuật Số DR

## 📊 Tóm Tắt Nhanh
- **Loại**: X-quang kỹ thuật số (DR)
- **Hãng**: GE Healthcare (Mỹ)
- **Giá tham khảo**: 5.2-6.5 tỷ VNĐ
- **Ứng dụng**: X-quang chụp đứng + nằm

## 🔧 Thông Số Kỹ Thuật Chi Tiết

| Thông số | Giá trị |
|----------|---------|
| Công suất | 400mA |
| Điện áp | 150kV |
| Detector | CsI 17×17 inch |
| Độ phân giải | 3.5 lp/mm |

## 💰 Lịch Sử Giá

| Ngày | Bệnh viện | Giá (VNĐ) | Nguồn |
|------|-----------|-----------|-------|
| 2025-11 | Bạch Mai | 5,800,000,000 | Gói thầu BM-2025-123 |
| 2025-08 | 108 | 6,200,000,000 | Đấu thầu rộng rãi |

## 📎 Tài Liệu Đính Kèm

- [Brochure kỹ thuật](../raw/Chan_doan_hinh_anh/X_quang/GE_Optima_XR220_brochure.pdf) (EN, 24 trang)
- [Bảng specs](../raw/Chan_doan_hinh_anh/X_quang/GE_Optima_XR220_specs.xlsx)
- [Báo giá BV Bạch Mai](../raw/Chan_doan_hinh_anh/X_quang/GE_Optima_XR220_price_2025.pdf)

## 🏥 Bệnh Viện Đã Mua
- Bệnh viện Bạch Mai (2025)
- Bệnh viện 108 (2025)

---
*Auto-generated by MedicalVault Bot | Last updated: 2026-02-13*
```

---

## 🤖 WORKFLOW TỰ ĐỘNG

### 1. Nhận File Mới (3 cách)
- **Cách 1:** Đồng nghiệp copy vào `/vault/raw/new/`
- **Cách 2:** Gửi file qua Telegram Bot
- **Cách 3:** Upload qua Outline Wiki interface

### 2. Auto-Processing Pipeline
- **Step 1:** File Watcher phát hiện file mới
- **Step 2:** Gemini 2.0 Flash Vision OCR toàn bộ → Extract text + tables + images
- **Step 3:** Gemini 2.0 Flash Structured Output → Parse thành JSON
- **Step 4: HUMAN REVIEW** (Telegram notification) → Confirm trong 5 phút hoặc auto-approve (confidence > 90%)
- **Step 5:** Generate/Update Markdown file
- **Step 6:** ChromaDB embedding → Vector search ready
- **Step 7:** Outline Wiki sync
- **Step 8:** Move file: `/vault/raw/new/` → `/vault/raw/classified/`
- **Step 9:** Telegram notify: "✅ Đã xử lý PDF"

### 3. Search & Retrieve
- **USER → Telegram:** `/search xquang ge`
- **ChromaDB:** Semantic search
- **Return:** List thiết bị + specs/giá
- **USER:** "Chi tiết XR220" → Bot gửi MD + PDF links

---

## 🛠️ TECH STACK CHI TIẾT

- **Core Backend:** FastAPI (Python), ChromaDB, PostgreSQL, Redis.
- **AI Services:** 
  - **Gemini 2.0 Flash:** OCR + Structured extraction (Cost: ~$0.075/1k tokens).
  - **Groq Llama 3.1:** Quick classify (Free tier).
  - **OpenAI GPT-4o-mini:** Backup.
- **Frontend & UI:** Outline Wiki (Self-hosted), Telegram Bot, Obsidian.
- **Infrastructure:** Docker Compose, Traefik (Reverse proxy), Rclone (Backup to Google Drive).

---

## 💰 CHI PHÍ THỰC TẾ

- **Đầu tư ban đầu:** 0 VNĐ (Sử dụng PC & ổ cứng có sẵn).
- **Vận hành tháng:** ~250k VNĐ.
  - Gemini API: 150-200k.
  - Điện PC: 50k.
  - Backup & Domain: 0đ (Free tier).

---

## 🗓️ ROADMAP 6 TUẦN (Thực Tế)

- **TUẦN 0-1: Setup Infrastructure**
  - Install Docker, setup folders, Docker Compose (Postgres/Redis), backup script.
- **TUẦN 2: Core Search ⭐**
  - Deploy ChromaDB, embed 1500 files, FastAPI search endpoint. 
  - *Chi phí:* ~3tr VNĐ cho lần đầu embed.
- **TUẦN 3: Outline Wiki ⭐**
  - Deploy Wiki, import MD mẫu, config permissions, access qua Cloudflare Tunnel.
- **TUẦN 4: Auto Extract + MD Generator ⭐⭐⭐**
  - Gemini 2.0 integration, Template generator, Human review workflow.
- **TUẦN 5: File Watcher + Auto Pipeline**
  - Python watchdog, Queue system (Redis), Error handling.
- **TUẦN 6: Telegram Bot + Polish**
  - Build Telegram commands, custom Wiki theme, documentation. **MVP HOÀN THIỆN ✅**

---

## 📱 USER EXPERIENCE (MVP)

- **Đồng Nghiệp (View Only):** Vào Wiki → Search → Click thiết bị → Export PDF gửi khách.
- **Bạn (Admin):** Drop file vào folder → Kiểm tra Telegram → Confirm → Obsidian tự update.
- **Remote (Anywhere):** Dùng Telegram Bot `/search` để lấy thông tin tức thì.

---

## 🔍 TÍNH NĂNG CHI TIẾT

1. **Semantic Search:** Hiểu ngữ nghĩa "máy xquang giá rẻ dưới 5 tỷ".
2. **Smart Extract:** Gemini 2.0 parse PDF theo JSON schema định sẵn.
3. **Compare Mode:** So sánh specs/giá giữa các model (e.g., `/compare xr220 vs xr656`).
4. **Auto-Tag & Category:** Tự động phân loại dựa trên nội dung file.
5. **Audit Trail:** Log mọi hành động search, xem, export trong PostgreSQL.

---

## 🔒 BẢO MẬT (Đơn Giản Hóa Phase 1)

- **MVP:** Password protection cho Wiki, Whitelist Telegram IDs, LAN only, Daily backup.
- **Sau MVP:** Cloudflare Tunnel (HTTPS), Audit logs chi tiết, MFA.

---

## 🚀 DEPLOYMENT GUIDE (Simplified)

### 1. Prerequisites
- Install Docker Desktop (Windows) hoặc Engine (Linux).
- Tạo folder structure: `D:/MedicalVault/{raw,md,docker,backup}`.

### 2. Start Services
1. Tạo file `docker-compose.yml` và `.env` với các API key (Gemini, DB password).
2. Chạy `docker-compose up -d`.

---

## 📊 SUCCESS METRICS

- **Tuần 1-2:** Containers chạy stable, Search API hoạt động.
- **Tuần 3-4:** Embed đủ 1500 files, search accuracy > 85%.
- **Tuần 6:** MVP Live, search time < 3s, team satisfaction cao.

---

## 🎯 PHASE SAU MVP (Tuần 7+)

- **Phase 2:** Advanced Features (Multi-device compare, Price tracking).
- **Phase 3:** Compliance (Audit trail, retention policy).
- **Phase 4:** Scale (Migrate sang NAS nếu data > 10TB).

---

## ⚠️ RỦI RO & MITIGATION

- **PC chết:** UPS + Daily backup sang Cloud/HDD.
- **Gemini API limit:** Fallback sang Groq/GPT-4o-mini.
- **OCR sai:** Human review queue.
- **Data loss:** Tuân thủ quy tắc backup 3-2-1.

---

## 🎉 KẾT LUẬN

**Tại sao chọn v2.0 PC Edition cho MVP?**
- Đầu tư 0đ so với 65tr của bản NAS.
- Timeline chỉ 6 tuần thay vì 11 tuần.
- Phù hợp hoàn hảo cho quy mô 3-5 users và 1500 files.

**Next Steps:**
- Tuần này: Setup Docker trên PC.
- Tuần 1: Bắt đầu build Core Search.
