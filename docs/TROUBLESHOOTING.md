# Hướng dẫn Khắc phục Sự cố MedicalVault

## Các vấn đề thường gặp

### 1. Containers không khởi động được
- **Triệu chứng**: `docker-compose up` thất bại hoặc containers tự tắt ngay lập tức.
- **Kiểm tra**:
    - Đảm bảo các port `8000` và `8001` đang rảnh.
    - Kiểm tra logs: `docker-compose logs -f webserver`.
    - Xác minh file `.env` đã tồn tại và có chứa các token hợp lệ.

### 2. Lỗi OCR (Tiếng Việt)
- **Triệu chứng**: Văn bản tiếng Việt bị lỗi font hoặc không tìm kiếm được.
- **Khắc phục**:
    - Đảm bảo `PAPERLESS_OCR_LANGUAGE: vie+eng` đã được thiết lập trong `docker-compose.yml`.
    - Nếu mới thay đổi, bạn có thể cần consume lại tài liệu hoặc đặt `PAPERLESS_OCR_MODE: redo_ocr`.

### 3. Vấn đề Telegram Bot
- **Triệu chứng**: Bot không phản hồi lệnh `/start`.
- **Kiểm tra**:
    - Container `openclaw` có đang chạy không?
    - Kiểm tra logs: `docker-compose logs -f openclaw`.
    - Xác minh `TELEGRAM_BOT_TOKEN`.
    - Đảm bảo `PAPERLESS_API_TOKEN` hợp lệ và chính xác.

### 4. Lỗi kết nối Database
- **Triệu chứng**: Webserver báo lỗi kết nối DB.
- **Khắc phục**:
    - Service `webserver` hiện tại đã được cấu hình chờ `db` health check. Nếu still timeout, có thể DB khởi động quá lâu hoặc quyền truy cập volume bị sai.
    - Kiểm tra logs `db`: `docker-compose logs -f db`.

## Bảo trì
- **Sao lưu (Backup)**:
    ```bash
    docker-compose exec webserver document_exporter ../export
    ```
- **Cập nhật (Update)**:
    ```bash
    git pull
    docker-compose pull
    docker-compose up -d
    ```
