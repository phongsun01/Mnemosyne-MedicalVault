#!/bin/bash

# MedicalVault Git Sync Tool for Mac
# Chức năng: Add, Commit, Push và tạo Tag chỉ với 1 lệnh.

# 0. Kiểm tra thư mục Git
if [ ! -d ".git" ]; then
    echo "❌ Error: Đây không phải là thư mục Git! Vui lòng chạy 'git init' trước."
    exit 1
fi

# 1. Nhập message commit (nếu không có tham số)
COMMIT_MSG=$1
if [ -z "$COMMIT_MSG" ]; then
    echo -n "📝 Nhập nội dung thay đổi (Commit message): "
    read COMMIT_MSG
fi

# Nếu không nhập gì, tự lấy ngày giờ
if [ -z "$COMMIT_MSG" ]; then
    COMMIT_MSG="Update MedicalVault: $(date '+%Y-%m-%d %H:%M:%S')"
fi

echo ""
echo "🚀 [1/3] Đang staging các thay đổi (git add .)..."
git add .

echo "📦 [2/3] Đang commit với nội dung: \"$COMMIT_MSG\""
git commit -m "$COMMIT_MSG"

echo "☁️ [3/3] Đang đẩy code lên GitHub..."
# Thử đẩy lên nhánh hiện tại
CURRENT_BRANCH=$(git branch --show-current)
git push -u origin "$CURRENT_BRANCH"

if [ $? -ne 0 ]; then
    echo "⚠️ Git push thất bại. Đang thử thiết lập upstream explicitly..."
    git push --set-upstream origin "$CURRENT_BRANCH"
fi

echo ""
echo "✅ HOÀN THÀNH SYNC!"
echo ""

# 4. Hỏi về việc tạo Tag (Version)
echo -n "🏷️ Bạn có muốn tạo Tag (phiên bản) cho bản này không? (y/n): "
read CREATE_TAG

if [[ "$CREATE_TAG" =~ ^[Yy]$ ]]; then
    echo -n "📌 Nhập tên Tag (VD: v2.0.1): "
    read TAG_NAME
    if [ ! -z "$TAG_NAME" ]; then
        echo -n "💬 Nhập mô tả cho Tag: "
        read TAG_MSG
        echo "🔥 Đang tạo Tag $TAG_NAME..."
        git tag -a "$TAG_NAME" -m "$TAG_MSG"
        git push origin "$TAG_NAME"
        echo "🎯 ĐÃ TẠO VÀ PUSH TAG $TAG_NAME!"
    else
        echo "🚫 Bỏ qua: Không nhập tên Tag."
    fi
fi

echo ""
echo "🎉 TẤT CẢ ĐÃ XONG!"
