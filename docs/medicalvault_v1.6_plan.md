# 📋 PHÁC THẢO CHI TIẾT - MEDICALVAULT BOT v1.6 (CUỐI CÙNG)

**Hệ thống quản lý hồ sơ thiết bị y tế tự động**

- **Ngày:** 12/02/2026
- **Stack:** OpenClaw + LangExtract + ChromaDB + DS1522+
- **Chi phí:** 65.5tr + 15-30k/th

---

## 🎯 MỤC TIÊU & ROI

Từ Explorer lộn xộn → Zero manual work:

- **Telegram Bot:** Search/classify từ xa
- **OpenClaw:** AI brain (memory + tools)
- **LangExtract:** OCR → JSON structured
- **NAS 40TB:** Vault + SQLite index
- **Obsidian/MkDocs:** Edit/view

**ROI:** 37tr/th → Hoàn vốn tháng 2.

---

## 🏗️ KIẾN TRÚC

```text
┌──────────────┐
│ TELEGRAM     │
└──────┬───────┘
       │
┌──────▼───────┐    ┌─────────────────┐
│ OPENCLAW     │───▶│ MEDICAL SERVICE │
│ 🧠 AI Brain  │    │ - OCR           │
│ Memory/Tools │    │ - LangExtract   │
│ Skills       │    │ - YAML/SQLite   │
└──────┬───────┘    └─────────────────┘
       │
┌──────▼───────┐
│ DS1522+ NAS  │ ←── GIT + Synology Drive
│ 40TB Vault   │
│ ChromaDB     │
│ SQLite FTS5  │
│ MkDocs Wiki  │
└──────────────┘
```

---

## 📁 VAULT STRUCTURE

```text
MedicalDevicesVault/
├── Chan_doan_hinh_anh/
│   └── X_quang/
│       └── GE_Optima_XR220/
│           ├── model_ge_optima_xr220.md  ← YAML + tables
│           ├── ky_thuat/
│           │   └── brochure_en.pdf
│           ├── thong_so/
│           │   └── cau_hinh.xlsx
│           └── hop_dong/
│               └── bach_mai.pdf
```

### model.md format:

```markdown
---
device_id: "uuid-1234"
model: "GE Optima XR220"
brand: "GE Healthcare"
price_range_vnd: [5200000000, 6500000000]
fda_approved: true
---
# 📋 BẢNG TÓM TẮT (Auto)
## 📚 Kỹ thuật (2 files)
| File | Ngày | Loại |
|------|------|------|
| brochure_en.pdf | 2026-02-05 | Catalog |
```

---

## 🤖 WORKFLOW TỰ ĐỘNG

1. **Copy PDF** → `/data/Xquang/`
2. **File watcher** → OpenClaw detect
3. **OpenClaw:** `medical_classify("/data/new.pdf")`
4. **Medical Service:**
   - OCR (PaddleOCR)
   - LangExtract → JSON structured
   - Update YAML + SQLite + MD table
5. **OpenClaw:** `git_commit()` + `mkdocs_build()`
6. **Telegram:** "✅ Classified specs.pdf"

**User search:**
> `/search x-quang GE` → Vector search ChromaDB → "Optima XR220 5.2ty 📄"

---

## 🧠 TECH STACK CHI TIẾT

- **FRONTEND:** Telegram Bot (OpenClaw native)
- **AI BRAIN:** OpenClaw (memory + tools + skills)
- **DOMAIN EXPERT:** Python FastAPI service
  - **OCR:** PaddleOCR + Gemini Vision
  - **Extract:** LangExtract (JSON structured)
  - **Storage:** YAML frontmatter + SQLite FTS5 + ChromaDB (vectors)
  - **Index:** Auto-sync khi file đổi
- **EDIT:** Obsidian Desktop + Git plugin
- **VIEW:** MkDocs Material Wiki (build cron 5p)
- **STORAGE:** DS1522+ 40TB RAID5

**Multi-API:**
- **Gemini Flash:** OCR + LangExtract (primary)
- **Groq Llama3.2:** Classify nhanh
- **Llama3 local:** Simple tasks (0đ)

---

## 💰 CHI PHÍ

**ĐẦU TƯ BAN ĐẦU: 65.5tr**
- DS1522+ + 40TB: 65tr
- NVMe cache: 0.5tr

**DUY TRÌ THÁNG: 15-30k**
- OpenClaw + LangExtract: 15k
- Telegram Premium (optional): 120k
- Điện NAS: 15k

---

## 🗓️ ROADMAP 11 TUẦN

- **TUẦN 0:** NAS + vault setup
- **TUẦN 1:** OpenClaw + Telegram + file watcher
- **TUẦN 2-3:** Core search (#2,5,6) + ChromaDB
- **TUẦN 4:** Multi-Agent OpenClaw skills (#1)
- **TUẦN 5:** OCR + LangExtract (#3) ⭐
- **TUẦN 6:** Smart Routing (#10)
- **TUẦN 7:** Event + Cache (#4,8)
- **TUẦN 8:** Auto-Tag (#9)
- **TUẦN 9-11:** Audit + Wiki (#7)

**GO-LIVE:** 24/04/2026

---

## 📱 USER EXPERIENCE

- **ĐỒNG NGHIỆP (View):**
  - Telegram: `/search x-quang GE` → "Optima XR220 📄"
  - Wiki: `http://nas/wiki` → Dashboard + search
- **BẠN (Edit):**
  - Obsidian: Edit MD → Git auto-sync → Wiki live
- **AUTO:**
  - Copy PDF → 3s → Classified + indexed + notified

---

## 🔍 TÍNH NĂNG NỔI BẬT

- ✅ 99.5% classify accuracy (Multi-Agent + LangExtract)
- ✅ Semantic search (ChromaDB vectors)
- ✅ Persistent memory (OpenClaw)
- ✅ OCR tiếng Việt 98% (PaddleOCR + Gemini)
- ✅ Zero manual YAML (auto-extract)
- ✅ Wiki realtime (MkDocs cron)
- ✅ Audit trail Git + SQLite
- ✅ Remote Telegram (4G everywhere)
- ✅ Chi phí 15k/th (hybrid optimize)

---

## 🎯 PHƯƠNG ÁN TRIỂN KHAI

- **PHASE 0 (Tuần 0):** NAS + vault
- **PHASE 1 (Tuần 1-3):** OpenClaw + core bot
- **PHASE 2 (Tuần 4-6):** LangExtract pipeline ⭐
- **PHASE 3-4 (Tuần 7-11):** Scale + enterprise

**MVP LIVE:** Tuần 3 (11/03) → **Full production:** 24/04

**PHÁC THẢO HOÀN CHỈNH:** OpenClaw brain + LangExtract extract + ChromaDB search + NAS vault = Jarvis y tế tự động hóa 99%.
