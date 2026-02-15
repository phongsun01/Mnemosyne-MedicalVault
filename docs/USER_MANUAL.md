# 📘 Hướng dẫn sử dụng MedicalVault v2.2

Chào mừng bạn đến với **MedicalVault** - Hệ thống quản lý tài liệu thiết bị y tế thông minh.
Tài liệu này sẽ hướng dẫn bạn từng bước để khai thác tối đa hiệu quả của hệ thống.

---

## 1. 🔑 Truy cập hệ thống

Hệ thống bao gồm 3 thành phần chính:

| Thành phần | Đường dẫn | Chức năng | Tài khoản mặc định |
|---|---|---|---|
| **Kho tài liệu (DMS)** | `http://localhost:8000` | Nơi upload, quản lý file gốc | `admin` / `admin` |
| **Wiki tra cứu** | `http://localhost:8001` | Xem so sánh thiết bị, thông số | *(Không cần)* |
| **Telegram Bot** | App Telegram | Tìm nhanh tài liệu qua chat | *(Chat trực tiếp)* |

---

## 2. 📤 Quy trình Upload tài liệu

Để tài liệu tự động xuất hiện trên Wiki và Bot, bạn hãy làm theo quy trình sau:

### Cách 1: Upload qua Web (Khuyên dùng)
1. Truy cập [DMS](http://localhost:8000).
2. Bấm nút **Upload** (góc trên bên phải) hoặc kéo thả file vào.
3. **Quan trọng:** Tại ô **Tags**, hãy chọn loại thiết bị tương ứng:
   - `x-quang`: Máy X-Quang
   - `sieu-am`: Máy Siêu âm
   - `mri`: Máy MRI
   - `noi-soi-da-day`: Máy nội soi dạ dày
   - *(Nếu không chọn tag, file sẽ vào mục "Chưa phân loại")*
4. Bấm **Start upload**.

### Cách 2: Upload qua thư mục (Auto Import)
1. Copy file PDF vào thư mục `consume/` trong máy tính.
2. Hệ thống sẽ tự động quét và xử lý sau 1-2 phút.
3. *Lưu ý: Cách này AI sẽ tự dự đoán Tag, có thể không chính xác 100%.*

---

## 3. 🤖 Sử dụng Telegram Bot

Bot giúp bạn tìm tài liệu ngay trên điện thoại mà không cần mở máy tính.

- **Tìm tài liệu:** Gõ lệnh `/search <tên máy>`
  - VD: `/search mri`, `/search fujifilm`
  - Bot sẽ trả về link tải file gốc.

- **Xem file mới nhất:** Gõ lệnh `/recent`
  - Xem 5 tài liệu vừa được đưa lên hệ thống.

---

## 4. 📚 Sử dụng Wiki & Cập nhật dữ liệu

Wiki là nơi trình bày thông tin đẹp mắt, dễ đọc hơn so với kho file gốc.

### Xem Wiki
- Truy cập [Wiki](http://localhost:8001).
- Chọn danh mục bên trái (VD: *Chẩn đoán hình ảnh > X-Quang*).
- Bấm vào tên máy để xem chi tiết.

### Cập nhật Wiki (Khi vừa upload file mới)
Wiki không tự động cập nhật *tức thời* (để tiết kiệm tài nguyên). Khi bạn vừa upload xong 1 lô tài liệu, hãy chạy lệnh sau để làm mới Wiki:

1. Mở Terminal (Command Prompt).
2. Chạy lệnh:
   ```bash
   cd docker_paperless
   docker-compose exec mkdocs python3 /docs/docs/generate_wiki.py
   ```
3. F5 lại trang Wiki để thấy thay đổi.

---

## 5. 🛠️ Xử lý sự cố thường gặp (FAQ)

**Q: Tôi upload rồi nhưng không thấy trên Wiki?**
A: Kiểm tra 2 việc:
1. File đã xử lý xong trên Paperless chưa? (Thanh *Processing* phải biến mất).
2. Bạn đã chạy lệnh cập nhật Wiki chưa? (Bước 4).
3. Nếu vẫn không thấy, hãy vào mục **"📂 Chưa phân loại (Inbox)"** trên Wiki để tìm.

**Q: Bot Telegram không trả lời?**
A: Thử gõ `/start` để đánh thức Bot. Nếu vẫn không được, hãy kiểm tra Docker xem container `openclaw` có đang chạy không.

**Q: Tôi muốn thêm loại máy mới (VD: Máy thở)?**
A: Bạn cần tạo Tag `may-tho` trong Paperless, sau đó cập nhật script `generate_wiki.py` để map tag này vào thư mục mới. (Liên hệ Admin kỹ thuật để hỗ trợ).

---
*MedicalVault v2.2 Documentation - 2026*
