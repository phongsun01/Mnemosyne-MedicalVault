# Tài liệu API MedicalVault

## Tổng quan
MedicalVault (Paperless-ngx) cung cấp một REST API để quản lý tài liệu. Telegram Bot và các dịch vụ khác sử dụng API này.

**Base URL**: `http://localhost:8000/api`
**Xác thực**: Token-based. Thêm header `Authorization: Token <YOUR_TOKEN>`.

## Các Endpoint chính

### 1. Tài liệu (Documents)
- **Tìm kiếm**: `GET /documents/?query=<query>`
- **Danh sách gần đây**: `GET /documents/?ordering=-created`
- **Tải lên**: `POST /documents/post_document/`

### 2. Metadata
- **Tags**: `GET /tags/`
- **Người gửi (Correspondents)**: `GET /correspondents/`
- **Loại tài liệu (Document Types)**: `GET /document_types/`

## Tích hợp Telegram Bot
Bot OpenClaw chủ yếu sử dụng:
- `/documents/?query={query}`: Cho chức năng tìm kiếm.
- `/documents/?ordering=-created`: Cho lệnh "recent" (gần đây).

## Xử lý lỗi
- **401 Unauthorized**: Kiểm tra `PAPERLESS_API_TOKEN`.
- **429 Too Many Requests**: Vượt quá giới hạn tốc độ API (nếu được cấu hình).
