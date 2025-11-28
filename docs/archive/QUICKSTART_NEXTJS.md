# ⚡ Quick Start - Next.js Version

## 🎯 Chạy trong 3 bước

### Bước 1: Cấu hình
```bash
# Tạo file .env
cp .env.example .env

# Chỉnh sửa .env với API credentials
nano .env  # hoặc dùng editor khác
```

Điền thông tin:
```env
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_BASE_URL=https://api.openai.com/v1
MODEL=gpt-4
```

### Bước 2: Chạy Backend

**Linux/Mac:**
```bash
cd backend
chmod +x run.sh
./run.sh
```

**Windows:**
```bash
cd backend
run.bat
```

**Hoặc chạy trực tiếp:**
```bash
pip install -r backend/requirements.txt
cd backend
uvicorn main:app --reload
```

Backend sẽ chạy tại: http://localhost:8000

### Bước 3: Chạy Frontend

**Terminal mới:**
```bash
cd frontend
npm install
npm run dev
```

Frontend sẽ chạy tại: http://localhost:3000

---

## 🐳 Hoặc dùng Docker (Dễ nhất)

```bash
# Một lệnh duy nhất
docker-compose -f docker-compose-fullstack.yml up --build
```

Truy cập: http://localhost:3000

---

## ✅ Kiểm tra

### Backend đang chạy?
```bash
curl http://localhost:8000/
# Kết quả: {"status":"ok","version":"2.0.0"}
```

### Frontend đang chạy?
Mở browser: http://localhost:3000

---

## 🎨 Sử dụng

1. **Upload file Excel** (.xlsx) với 3 cột: Title, Content, Description
2. **Click "Bắt đầu phân loại"** ở tab "Xử lý"
3. **Theo dõi progress** real-time
4. **Tải xuống kết quả** ở tab "Kết quả"

---

## ❓ Troubleshooting

### Lỗi: "System not initialized"
```bash
# Kiểm tra .env file
cat .env

# Kiểm tra prompt_template.txt
ls -la prompt_template.txt

# Restart backend
```

### Lỗi: Port đã được sử dụng
```bash
# Kill process trên port 8000
lsof -ti:8000 | xargs kill -9

# Kill process trên port 3000
lsof -ti:3000 | xargs kill -9
```

### Frontend không kết nối Backend
```bash
# Kiểm tra backend đang chạy
curl http://localhost:8000/api/config

# Kiểm tra CORS trong backend/main.py
# allow_origins=["http://localhost:3000"]
```

---

## 📚 Tài liệu đầy đủ

Xem **README_NEXTJS.md** để biết thêm chi tiết.

---

**Estimated Time**: 5 phút  
**Stack**: Next.js + FastAPI  
**Version**: 2.0.0
