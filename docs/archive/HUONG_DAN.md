# 📖 Hướng dẫn sử dụng hệ thống phân loại SPX

## 🎯 Giới thiệu

Hệ thống phân loại feedback khách hàng SPX sử dụng LLM với kiến trúc xử lý tập trung. Hệ thống tự động phân loại feedback từ khách hàng (Rider/Seller/Buyer) vào các danh mục đã định nghĩa sẵn.

## 🚀 Bắt đầu nhanh

### Bước 1: Cài đặt

#### Cách 1: Sử dụng Python trực tiếp

```bash
# Clone hoặc tải project về
cd spx_classification

# Cài đặt dependencies
pip install -r requirements.txt

# Tạo file cấu hình
cp .env.example .env
```

#### Cách 2: Sử dụng Docker (Khuyến nghị)

```bash
# Build và chạy
docker-compose up --build

# Hoặc chạy ở chế độ background
docker-compose up -d
```

### Bước 2: Cấu hình

Chỉnh sửa file `.env`:

```env
# Thông tin API (bắt buộc)
OPENAI_API_KEY=sk-xxxxxxxxxxxxx
OPENAI_BASE_URL=https://api.openai.com/v1
MODEL=gpt-4

# Cấu hình xử lý (tùy chọn)
MAX_WORKERS=10          # Số luồng xử lý song song
MAX_RETRY=3            # Số lần thử lại khi lỗi
RETRY_WAIT=0.5         # Thời gian chờ giữa các lần thử (giây)

# Tham số model (tùy chọn)
TEMPERATURE=0          # Độ ngẫu nhiên (0 = ổn định nhất)
MAX_TOKENS=150        # Số token tối đa cho kết quả
```

### Bước 3: Chạy ứng dụng

```bash
# Nếu dùng Python
streamlit run run.py

# Nếu dùng Docker, ứng dụng đã tự động chạy
```

Truy cập: http://localhost:8501

## 📊 Cách sử dụng

### 1. Chuẩn bị dữ liệu

File Excel đầu vào phải có **ít nhất 3 cột**:
- `Title`: Tiêu đề feedback
- `Content`: Nội dung chính
- `Description`: Mô tả chi tiết

Ví dụ:

| Title | Content | Description |
|-------|---------|-------------|
| Giao hàng nhanh | Tài xế rất nhiệt tình | Hài lòng với dịch vụ |
| Website lag | Trang web bị giật | Cần cải thiện |

### 2. Tải file lên

1. Click vào sidebar bên trái
2. Chọn "Tải lên file Excel (.xlsx)"
3. Chọn file từ máy tính
4. Hệ thống sẽ hiển thị preview 10 dòng đầu

### 3. Thực hiện phân loại

1. **Xem trước dữ liệu**: Kiểm tra dữ liệu đã tải đúng chưa
2. **Chọn tùy chọn**:
   - ☑️ "Xóa cache trước khi chạy" nếu muốn phân loại lại từ đầu
   - ☐ Bỏ chọn để sử dụng kết quả đã lưu (nhanh hơn)
3. **Click "🚀 Bắt đầu phân loại"**
4. **Theo dõi tiến trình**: Progress bar sẽ hiển thị % hoàn thành

### 4. Xem kết quả

Sau khi hoàn thành, hệ thống hiển thị:

#### Thống kê:
- **Tổng số dòng**: Số feedback đã xử lý
- **Cache hits**: Số kết quả lấy từ cache (không tốn API)
- **API calls**: Số lần gọi API mới
- **Thất bại**: Số feedback không phân loại được
- **Tỷ lệ thành công**: % phân loại thành công

#### Kết quả phân loại:
File output sẽ có thêm 5 cột mới:
- `label_en`: Label đầy đủ (VD: "RIDER / Driver Compensation & Benefits / Income")
- `label_1`: Cấp 1 (VD: "RIDER")
- `label_2`: Cấp 2 (VD: "Driver Compensation & Benefits")
- `label_3`: Cấp 3 (VD: "Income")
- `label_4`: Cấp 4 (nếu có)

### 5. Tải xuống kết quả

1. Click "📥 Tải xuống file Excel đã phân loại"
2. File sẽ được lưu với tên: `[tên_file_gốc]_classified.xlsx`

## 🔧 Tính năng nâng cao

### Cache thông minh

Hệ thống tự động lưu kết quả phân loại vào file `classification_cache.json`. Khi gặp feedback giống nhau, hệ thống sẽ:
- ✅ Lấy kết quả từ cache (nhanh, không tốn API)
- ❌ Không gọi API lại

**Lợi ích:**
- Tiết kiệm chi phí API
- Tăng tốc độ xử lý
- Kết quả nhất quán

**Xóa cache khi nào?**
- Khi thay đổi prompt template
- Khi muốn phân loại lại với model mới
- Khi kết quả cũ không chính xác

### Xử lý song song

Hệ thống sử dụng `MAX_WORKERS` luồng để xử lý đồng thời nhiều feedback:
- `MAX_WORKERS=10`: Xử lý 10 feedback cùng lúc (mặc định)
- Tăng số này để xử lý nhanh hơn (cần API có rate limit cao)
- Giảm số này nếu gặp lỗi rate limit

### Retry tự động

Khi gọi API bị lỗi, hệ thống tự động thử lại:
- `MAX_RETRY=3`: Thử tối đa 3 lần
- `RETRY_WAIT=0.5`: Chờ 0.5 giây giữa các lần thử

## 🛠️ Scripts tiện ích

### Kiểm tra cấu hình

```bash
python scripts/check_config.py
```

Hiển thị:
- Thông tin API
- Cấu hình xử lý
- Tham số model
- Trạng thái files

### Xóa cache

```bash
python scripts/clear_cache.py
```

### Test hệ thống

```bash
python scripts/test_system.py
```

Kiểm tra:
- Classifier hoạt động
- Cache manager
- Central processor

## ❓ Xử lý sự cố

### Lỗi: "OPENAI_BASE_URL is not set"

**Nguyên nhân**: Chưa cấu hình file `.env`

**Giải pháp**:
```bash
cp .env.example .env
# Chỉnh sửa .env với thông tin API của bạn
```

### Lỗi: "Prompt template file not found"

**Nguyên nhân**: Thiếu file `prompt_template.txt`

**Giải pháp**: Đảm bảo file `prompt_template.txt` tồn tại trong thư mục gốc

### Lỗi: API rate limit

**Nguyên nhân**: Gọi API quá nhanh

**Giải pháp**:
- Giảm `MAX_WORKERS` trong `.env` (VD: từ 10 xuống 5)
- Tăng `RETRY_WAIT` (VD: từ 0.5 lên 1.0)

### Lỗi: File Excel không đọc được

**Nguyên nhân**: File không đúng định dạng hoặc thiếu cột

**Giải pháp**:
- Đảm bảo file có đuôi `.xlsx`
- Kiểm tra có đủ 3 cột: `Title`, `Content`, `Description`
- Thử mở file bằng Excel/LibreOffice để kiểm tra

### Kết quả phân loại không chính xác

**Giải pháp**:
1. Kiểm tra và cập nhật `prompt_template.txt`
2. Xóa cache: Click "Xóa cache trước khi chạy"
3. Thử với model khác (VD: gpt-4 thay vì gpt-3.5-turbo)
4. Điều chỉnh `TEMPERATURE` (0 = ổn định, 1 = sáng tạo)

## 📈 Tips tối ưu

### Tăng tốc độ xử lý

1. **Sử dụng cache**: Không xóa cache khi không cần thiết
2. **Tăng workers**: Nếu API cho phép, tăng `MAX_WORKERS`
3. **Batch processing**: Xử lý nhiều file cùng lúc

### Tiết kiệm chi phí

1. **Tận dụng cache**: Cache giúp không phải gọi API lại
2. **Giảm MAX_TOKENS**: Nếu label ngắn, giảm xuống 100
3. **Sử dụng model rẻ hơn**: VD: gpt-3.5-turbo thay vì gpt-4

### Cải thiện độ chính xác

1. **Cập nhật prompt**: Chỉnh sửa `prompt_template.txt` với ví dụ cụ thể
2. **Sử dụng model tốt hơn**: gpt-4 > gpt-3.5-turbo
3. **Giảm TEMPERATURE**: Đặt = 0 để kết quả ổn định nhất

## 🐳 Docker Commands

```bash
# Build image
docker-compose build

# Chạy container
docker-compose up

# Chạy ở background
docker-compose up -d

# Xem logs
docker-compose logs -f

# Dừng container
docker-compose down

# Xóa container và volumes
docker-compose down -v
```

## 📞 Hỗ trợ

Nếu gặp vấn đề:
1. Kiểm tra logs: `docker-compose logs -f`
2. Chạy test: `python scripts/test_system.py`
3. Kiểm tra config: `python scripts/check_config.py`

## 🔄 Cập nhật

Để cập nhật lên phiên bản mới:

```bash
# Pull code mới
git pull

# Rebuild Docker image
docker-compose down
docker-compose up --build
```

---

**Phiên bản**: 2.0.0  
**Cập nhật**: November 2025  
**Team**: SPX Vietnam
