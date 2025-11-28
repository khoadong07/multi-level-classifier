# ⚡ Quick Start Guide - SPX Classification v2.0

## 🎯 Mục tiêu
Hướng dẫn nhanh để chạy hệ thống phân loại feedback SPX trong 5 phút.

## 📋 Yêu cầu
- Python 3.11+ hoặc Docker
- OpenAI API key (hoặc compatible API)

## 🚀 Cách 1: Chạy với Python (Khuyến nghị cho development)

### Bước 1: Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### Bước 2: Cấu hình
```bash
# Copy file mẫu
cp .env.example .env

# Chỉnh sửa .env
nano .env  # hoặc dùng editor khác
```

Điền thông tin:
```env
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_BASE_URL=https://api.openai.com/v1
MODEL=gpt-4
```

### Bước 3: Chạy
```bash
streamlit run run.py
```

### Bước 4: Truy cập
Mở browser: http://localhost:8501

---

## 🐳 Cách 2: Chạy với Docker (Khuyến nghị cho production)

### Bước 1: Cấu hình
```bash
cp .env.example .env
# Chỉnh sửa .env với API credentials
```

### Bước 2: Build và chạy
```bash
docker-compose up --build
```

### Bước 3: Truy cập
Mở browser: http://localhost:8501

---

## 📝 Sử dụng cơ bản

### 1. Chuẩn bị file Excel
File phải có 3 cột:
- `Title`: Tiêu đề
- `Content`: Nội dung
- `Description`: Mô tả

### 2. Upload file
- Click sidebar → "Tải lên file Excel"
- Chọn file từ máy

### 3. Phân loại
- Click "🚀 Bắt đầu phân loại"
- Đợi xử lý (có progress bar)

### 4. Tải kết quả
- Click "📥 Tải xuống file Excel đã phân loại"
- File sẽ có thêm 5 cột: `label_en`, `label_1`, `label_2`, `label_3`, `label_4`

---

## 🔧 Commands hữu ích

### Với Makefile:
```bash
make run              # Chạy app
make check-config     # Kiểm tra config
make clear-cache      # Xóa cache
make test             # Test hệ thống
make clean            # Dọn dẹp files
```

### Với Docker:
```bash
docker-compose up -d          # Chạy background
docker-compose logs -f        # Xem logs
docker-compose down           # Dừng
docker-compose restart        # Restart
```

---

## ⚙️ Tùy chỉnh nhanh

### Tăng tốc độ xử lý:
```env
MAX_WORKERS=20  # Tăng từ 10 lên 20
```

### Giảm chi phí:
```env
MODEL=gpt-3.5-turbo  # Thay vì gpt-4
MAX_TOKENS=100       # Giảm từ 150
```

### Tăng độ chính xác:
```env
MODEL=gpt-4          # Model tốt hơn
TEMPERATURE=0        # Kết quả ổn định nhất
```

---

## ❓ Troubleshooting nhanh

### Lỗi: "OPENAI_BASE_URL is not set"
```bash
# Tạo file .env
cp .env.example .env
# Điền thông tin API
```

### Lỗi: API rate limit
```bash
# Giảm workers trong .env
MAX_WORKERS=5
```

### Lỗi: File không đọc được
- Kiểm tra file có đúng format `.xlsx`
- Kiểm tra có đủ 3 cột: Title, Content, Description

### Cache không hoạt động
```bash
# Xóa cache và thử lại
python scripts/clear_cache.py
```

---

## 📚 Tài liệu đầy đủ

- **README.md**: English documentation
- **HUONG_DAN.md**: Hướng dẫn chi tiết tiếng Việt
- **ARCHITECTURE.md**: Kiến trúc hệ thống
- **CHANGELOG.md**: Lịch sử thay đổi

---

## 💡 Tips

### Tip 1: Sử dụng cache
- Không xóa cache khi không cần thiết
- Cache giúp tiết kiệm 70-80% API calls

### Tip 2: Batch processing
- Xử lý nhiều file cùng lúc để tận dụng cache

### Tip 3: Monitor progress
- Theo dõi "Cache hits" để biết hiệu quả cache
- "API calls" = chi phí thực tế

### Tip 4: Backup cache
```bash
cp classification_cache.json classification_cache_backup.json
```

---

## 🎉 Xong!

Bây giờ bạn đã có thể:
- ✅ Chạy hệ thống
- ✅ Upload và phân loại feedback
- ✅ Tải xuống kết quả
- ✅ Tùy chỉnh cấu hình

Nếu cần hỗ trợ thêm, xem **HUONG_DAN.md** hoặc **README.md**.

---

**Version**: 2.0.0  
**Last Updated**: November 2025  
**Estimated Setup Time**: 5 minutes
