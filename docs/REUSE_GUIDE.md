# Hướng dẫn Tái sử dụng Công cụ Dự án (MedicalVault v2.0)

Tài liệu này cung cấp các đoạn code và quy trình chuẩn đã được tối ưu hóa cho dự án **MedicalVault v2.0** để bạn có thể áp dụng nhanh vào các dự án AI Pipeline, Docker hoặc FastAPI tương tự.

## 1. Script tự động hóa Git (`git_sync.sh`)

Vì bạn đang dùng Mac, hãy sử dụng script shell này thay vì file `.bat`. Lưu đoạn code sau vào file `git_sync.sh` ở thư mục gốc.

```bash
#!/bin/bash

# 0. Kiểm tra thư mục Git
if [ ! -d ".git" ]; then
    echo "[ERROR] Đây không phải là thư mục Git!"
    echo "Vui lòng chạy 'git init' trước."
    exit 1
fi

# 1. Nhập message commit
COMMIT_MSG=$1
if [ -z "$COMMIT_MSG" ]; then
    read -p "Nhập nội dung thay đổi (Commit message): " COMMIT_MSG
fi

# Nếu không nhập gì, tự lấy ngày giờ
if [ -z "$COMMIT_MSG" ]; then
    COMMIT_MSG="Update: $(date '+%Y-%m-%d %H:%M:%S')"
fi

echo ""
echo "[1/3] Đang staging các thay đổi (git add .)..."
git add .

echo "[2/3] Đang commit với nội dung: \"$COMMIT_MSG\""
git commit -m "$COMMIT_MSG"

echo "[3/3] Đang đẩy code lên server (git push)..."
git push

echo ""
echo "=== HOÀN THÀNH SYNC ==="
echo ""
```

## 2. Cấu hình `.gitignore` tối ưu

Dưới đây là cấu hình `.gitignore` cho dự án MedicalVault để tránh đẩy dữ liệu cá nhân, database và file rác lên GitHub:

```text
# OS files
.DS_Store
Thumbs.db

# Docker Data (Rất quan trọng - Không push dữ liệu thực)
docker/postgres_data/
docker/chroma_data/
/Users/xitrum/MedicalVault/

# Secrets & Env
.env
docker/.env
*.key
*.pem

# AI Agent & Workspace Data
.agent/
.gemini/
.antigravity/

# Logs & Temp
*.log
backend/__pycache__/
.pytest_cache/
```

## 3. Quy trình Triển khai nhanh

Khi muốn chạy dự án ở máy mới:
1. `git clone <repo_url>`
2. Cấu hình file `.env` (copy từ `.env.example`).
3. Chạy lệnh: `docker-compose up -d`.
4. Kiểm tra sức khỏe API: `curl http://localhost:8080/health`.

---
*Tài liệu được cập nhật bởi Antigravity cho MedicalVault v2.0*
