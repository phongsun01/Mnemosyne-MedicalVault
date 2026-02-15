# PHÁC THẢO CHI TIẾT - MEDICALVAULT BOT v2.2 PAPERLESS (CUỐI CÙNG)

**Jarvis y tế 1 ngày live - Paperless-ngx + AI + Telegram**
**Ngày:** 15/02/2026 | **Stack:** Paperless-ngx + Paperless-GPT + OpenClaw + MkDocs | **Chi phí:** 0đ đầu tư + 20k/th | **MVP:** Hôm nay!

---

## 🎯 MỤC TIÊU & ROI
Từ 1500 files lộn xộn → Live production 1 ngày:

- ✅ **MVP ngay hôm nay** (10 phút setup)
- ✅ **80% tính năng sẵn** (DMS + OCR + AI)
- ✅ **Customize 2 tuần** → 100% MedicalVault
- ✅ **ROI:** Tiết kiệm 4-6 tuần dev

*Team 3-5 người: Web UI đẹp + Telegram bot + Wiki sync.*

---

## 🏗️ KIẾN TRÚC PAPERLESS-BASED

```mermaid
graph TD
    User[USER INPUT] --> Web[Web Upload]
    User --> Consume[~/consume/ INBOX]
    User --> Email[Email forward]
    
    subgraph Core[PAPERLESS-NGX (Core DMS)]
        OCR[OCR Tesseract]
        Search[Full-text search]
        Tags[Tags/metadata]
        Preview[Preview/download]
    end
    
    Web --> Core
    Consume --> Core
    Email --> Core
    
    subgraph AI[PAPERLESS-GPT (AI Layer)]
        GPT[GPT-4o classify]
        AutoTag[Auto-tag/title]
        StructData[Structured data]
    end
    
    Core --> AI
    AI --> Core
    
    subgraph Custom[CUSTOM LAYER (MedicalVault)]
        OpenClaw[OpenClaw Telegram]
        MDGen[MD Generator]
        MkDocs[MkDocs Wiki]
        Chroma[ChromaDB opt]
    end
    
    Core --> Custom
```

---

## 📁 CẤU TRÚC DỮ LIỆU & WIKI (OPTION B)

### 1. Paperless Storage (Backend)
```text
~/medicalvault/
├── consume/              ⭐ INBOX
├── media/                # PDF gốc + OCR
├── data/                 # PostgreSQL
└── export/               # Backup
```

### 2. Wiki Structure (MkDocs - Frontend)
**Chiến lược:** Phân loại theo **LOẠI MÁY** (Device Type) để dễ so sánh.

```text
Wiki/ (MkDocs docs/)
├── index.md                          # Dashboard + search
├── chan_doan_hinh_anh/
│   ├── index.md                     # Overview category
│   ├── x_quang/
│   │   ├── index.md                 # Compare table all X-ray
│   │   ├── ge_optima_xr220.md       ⭐ Model page
│   │   ├── siemens_luminos.md
│   │   └── philips_digitaldiagnost.md
│   ├── ct_scanner/
│   │   ├── index.md
│   │   ├── ge_revolution.md
│   │   └── siemens_somatom.md
│   ├── mri/
│   └── sieu_am/
├── noi_soi/
│   ├── index.md
│   ├── noi_soi_da_day/
│   │   ├── hoya_ep_exera_iii.md
│   │   └── olympus_cv_190.md
│   └── noi_soi_dai_trang/
├── kiem_soat_nhiem_khuan/
│   └── may_tiet_trung/
│       ├── tuttnauer_3850.md
│       └── systec_vx_150.md
├── gay_me_hoi_suc/
│   ├── may_tho/
│   └── monitor/
├── phau_thuat/
├── xet_nghiem/
└── tags.md                          # Tag cloud (filter)
```

### 3. Format File .md (Auto-generated)
Mỗi file `.md` sẽ chứa metadata phong phú để search và filter.

```yaml
---
# METADATA (Paperless sync + search)
device_id: "ge-optima-xr220-uuid1234"
model: "GE Optima XR220"
brand: "GE Healthcare"
category: "Chan_doan_hinh_anh/X_quang"
price_range_vnd: [5200000000, 6500000000]
fda_approved: true
vietnam_moh_number: "12345/QĐ-BYT"

# PROJECTS (link to hospitals)
projects:
  - name: "Bệnh viện Bạch Mai 2025"
    contract_date: "2025-03-15"
    value_vnd: 5800000000
    status: "Đã nghiệm thu"

# TAGS (filter/search)
tags: ["x-quang", "chẩn-đoán", "fda", "5-7ty"]
last_updated: "2026-02-15"
---

# 📋 GE Optima XR220

**Giá tham khảo**: 5.2-6.5 tỷ VND | **FDA**: ✅ | **BYT**: 12345/QĐ-BYT

## 📊 Thông số kỹ thuật
| Thông số | Giá trị |
|---|---|
| Công suất ống | 50kW |
| Detector | DR Panel 43x43cm |

## 📁 Tài liệu (Auto từ Paperless)
| Loại | File | Ngày | Link |
|---|---|---|---|
| Kỹ thuật | [Brochure EN](paperless://doc/1234) | 2025-03-10 | 📄 |
| Hợp đồng | [Bạch Mai](paperless://doc/1236) | 2025-03-15 | 📃 |

## 🔗 Links
- [So sánh X-quang cùng phân khúc](./index.md#comparison)
- [Tất cả sản phẩm GE](../../tags.md#ge-healthcare)
```

---

## 🤖 WORKFLOW & AUTOMATION

### 1. Script Tự Động (Tuần 1)
`generate_wiki.py` sẽ chạy mỗi khi Paperless có webhook (hoặc chạy định kỳ).

```python
def sync_document(doc_id):
    # 1. Get doc from Paperless
    doc = requests.get(f"{PAPERLESS_API}{doc_id}/").json()
    
    # 2. Extract metadata & Category
    category = doc['custom_fields']['category']  # "chan_doan_hinh_anh/x_quang"
    model = doc['custom_fields']['model']        # "GE Optima XR220"
    
    # 3. Generate path & Markdown
    folder = WIKI_ROOT / category
    md_file = folder / f"{slugify(model)}.md"
    
    # 4. Generate Content (như mẫu trên)
    # 5. Rebuild MkDocs
```

### 2. Navigation & Search Strategy
- **File nav:** `mkdocs.yml` định nghĩa cây thư mục chính.
- **Index Pages:** Mỗi thư mục con (VD: `x_quang/index.md`) sẽ có bảng so sánh tự động.
- **Tags Page:** `tags.md` cho phép lọc theo Hãng, Giá, Dự án (VD: `#ge`, `#5-7ty`, `#bach-mai`).

---

## 🧠 TECH STACK

### CORE (SẴN)
- 📦 **Paperless-ngx:** DMS + OCR + Search + UI
- 🧠 **Paperless-GPT:** AI classify (GPT-4o-mini)
- 🗄️ **PostgreSQL:** Metadata DB
- 🔍 **Redis:** Task queue

### CUSTOM (TUẦN 1-2)
- 🤖 **OpenClaw:** Telegram bot
- 📝 **MkDocs (Material):** Wiki generator (Giao diện đẹp)
- 🐍 **Python Script:** Sync Logic

---

## � ROADMAP 3 TUẦN (CẬP NHẬT)

### HÔM NAY (ĐÃ XONG):
- [x] Setup Docker Paperless-ngx + GPT
- [x] Copy 20 files test → `consume/`
- [x] Bots & API Token ready

### TUẦN 1 (10h) - WIKI & BOT:
- [ ] Telegram bot: `/search`, `/recent` (Đang triển khai)
- [ ] **Wiki Setup:** Cài đặt MkDocs Material theme.
- [ ] **Wiki Content:** Viết script `generate_wiki.py` theo cấu trúc Option B.
- [ ] **Automation:** Config Webhook từ Paperless → Trigger script.

### TUẦN 2 (10h) - ADVANCED:
- [ ] OpenClaw: Re-classify nâng cao (AI Memory).
- [ ] Dashboard: Thống kê số lượng thiết bị, cảnh báo hết hạn bảo hành.
- [ ] ChromaDB: Semantic search (Tìm kiếm theo ý nghĩa).

**GO-LIVE: Tuần 3 (04/03/2026)**
