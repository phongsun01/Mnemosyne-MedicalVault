# Kiến trúc MedicalVault

## Tổng quan
MedicalVault là Hệ thống Quản lý Tài liệu (DMS) được xây dựng trên nền tảng Paperless-ngx, được tăng cường với các khả năng AI và giao diện Telegram.

## Sơ đồ hệ thống

```mermaid
graph TD
    subgraph "Mạng Backend (Nội bộ)"
        DB[(PostgreSQL)]
        Redis[(Redis)]
        Web[Paperless Webserver]
    end

    subgraph "Mạng Frontend"
        Web
        Bot[Telegram Bot (OpenClaw)]
        AI[Paperless-GPT]
        Wiki[MkDocs]
    end

    User((Người dùng)) -->|HTTP| Web
    User -->|Telegram| Bot
    
    Web <--> DB
    Web <--> Redis
    
    Bot -->|API| Web
    AI -->|API| Web
    Wiki -->|API| Web
    
    AI -->|External| OpenAI[OpenAI API]
    Bot -->|External| Telegram[Telegram API]
```

## Các thành phần chi tiết

### 1. Core (Paperless-ngx)
- **Webserver**: Ứng dụng Django. Xử lý giao diện người dùng, API và vòng lặp consumer.
- **Database**: PostgreSQL 16. Lưu trữ metadata và chỉ mục văn bản.
- **Broker**: Redis 7. Hàng đợi tác vụ cho Celery.

### 2. Extensions (Mở rộng)
- **Paperless-GPT**: Một AI agent tự động gắn thẻ tài liệu sử dụng GPT-4o. Lắng nghe tài liệu mới qua webhooks hoặc polling.
- **OpenClaw (Telegram Bot)**: Cập nhật cho người dùng và cho phép tìm kiếm qua Telegram. Viết bằng Python (`python-telegram-bot`).
- **MkDocs Wiki**: Tự động tạo trang web tĩnh từ metadata tài liệu cho giao diện "Knowledge Base".

## Mạng (Networking)
- **Mạng Backend**: Mạng cô lập cho dữ liệu bền vững (`db`, `broker`). Không có truy cập trực tiếp từ bên ngoài.
- **Mạng Frontend**: Expose các dịch vụ yêu cầu truy cập internet hoặc tương tác người dùng.
