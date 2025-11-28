# 🔧 Setup Guide - SPX Classification System

## ⚡ Quick Setup (5 phút)

### Bước 1: Clone/Download project

```bash
cd spx_classification
```

### Bước 2: Tạo file .env

```bash
# Copy file mẫu
cp .env.example .env

# Hoặc tạo mới
nano .env
```

**Nội dung file .env (BẮT BUỘC):**
```env
# API Configuration (Required)
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_BASE_URL=https://api.openai.com/v1
MODEL=gpt-4

# Processing (Optional - có giá trị mặc định)
MAX_WORKERS=10
MAX_RETRY=3
RETRY_WAIT=0.5
TEMPERATURE=0
MAX_TOKENS=150
```

### Bước 3: Kiểm tra cấu hình

```bash
cd backend
python3 check_env.py
```

Nếu thấy ✅ tất cả → OK!  
Nếu thấy ❌ → Sửa file .env theo hướng dẫn

### Bước 4: Chạy Backend

```bash
# Cách 1: Dùng script (khuyến nghị)
./run.sh

# Cách 2: Chạy trực tiếp
pip install -r requirements.txt
cd ..
uvicorn backend.main:app --reload
```

Backend chạy tại: http://localhost:8000

### Bước 5: Chạy Frontend

**Terminal mới:**
```bash
cd frontend
npm install
npm run dev
```

Frontend chạy tại: http://localhost:3000

---

## 🐳 Setup với Docker (Dễ nhất)

### Bước 1: Tạo .env
```bash
cp .env.example .env
# Chỉnh sửa .env với API credentials
```

### Bước 2: Chạy
```bash
docker-compose -f docker-compose-fullstack.yml up --build
```

Xong! Truy cập: http://localhost:3000

---

## ✅ Kiểm tra hệ thống

### 1. Kiểm tra Backend
```bash
# Health check
curl http://localhost:8000/
# Kết quả: {"status":"ok","version":"2.0.0"}

# Config check
curl http://localhost:8000/api/config
# Kết quả: {"model":"gpt-4","base_url":"...","max_workers":10,...}
```

### 2. Kiểm tra Frontend
Mở browser: http://localhost:3000

Bạn sẽ thấy giao diện với 4 tabs:
- ✅ Tải lên
- ✅ Cấu hình
- ⚠️  Xử lý (disabled cho đến khi upload file)
- ⚠️  Kết quả (disabled cho đến khi xử lý xong)

---

## 🔍 Troubleshooting

### Lỗi: "MODEL is not set"

**Nguyên nhân:** File .env chưa được tạo hoặc thiếu biến MODEL

**Giải pháp:**
```bash
# Kiểm tra file .env
cat .env

# Nếu không có, tạo từ mẫu
cp .env.example .env

# Chỉnh sửa và thêm:
MODEL=gpt-4
OPENAI_API_KEY=sk-your-key
OPENAI_BASE_URL=https://api.openai.com/v1
```

### Lỗi: "prompt_template.txt not found"

**Nguyên nhân:** Thiếu file prompt template

**Giải pháp:**
```bash
# Kiểm tra file có tồn tại không
ls -la prompt_template.txt

# File phải ở thư mục gốc của project
```

### Lỗi: "System not initialized"

**Nguyên nhân:** Backend khởi động thất bại do cấu hình sai

**Giải pháp:**
```bash
# Chạy script kiểm tra
cd backend
python3 check_env.py

# Xem logs backend để biết lỗi cụ thể
# Sửa theo hướng dẫn
```

### Lỗi: Port đã được sử dụng

**Backend (8000):**
```bash
# Linux/Mac
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Frontend (3000):**
```bash
# Linux/Mac
lsof -ti:3000 | xargs kill -9

# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Frontend không kết nối Backend

**Kiểm tra:**
1. Backend có đang chạy không? → `curl http://localhost:8000/`
2. CORS có được cấu hình đúng không? → Xem `backend/main.py`
3. URL có đúng không? → `http://localhost:8000` (không phải https)

**Sửa CORS (nếu cần):**
```python
# backend/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # ← Kiểm tra dòng này
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📋 Checklist Setup

- [ ] Python 3.11+ đã cài đặt
- [ ] Node.js 18+ đã cài đặt (cho frontend)
- [ ] File `.env` đã tạo với đầy đủ thông tin
- [ ] File `prompt_template.txt` tồn tại
- [ ] Backend dependencies đã cài: `pip install -r backend/requirements.txt`
- [ ] Frontend dependencies đã cài: `cd frontend && npm install`
- [ ] Backend chạy thành công tại port 8000
- [ ] Frontend chạy thành công tại port 3000
- [ ] Có thể truy cập http://localhost:3000

---

## 🎯 Sau khi setup xong

### Test hệ thống:
1. Mở http://localhost:3000
2. Upload file Excel mẫu (có 3 cột: Title, Content, Description)
3. Chuyển sang tab "Xử lý"
4. Click "Bắt đầu phân loại"
5. Xem progress bar
6. Chuyển sang tab "Kết quả"
7. Tải xuống file đã phân loại

### Xem API docs:
http://localhost:8000/docs

### Xem cache:
```bash
cat classification_cache.json
```

---

## 📚 Tài liệu thêm

- **README_NEXTJS.md** - Tài liệu đầy đủ về Next.js version
- **QUICKSTART_NEXTJS.md** - Hướng dẫn nhanh
- **ARCHITECTURE.md** - Kiến trúc hệ thống
- **HUONG_DAN.md** - Hướng dẫn chi tiết tiếng Việt

---

## 💡 Tips

### Tip 1: Sử dụng script check_env.py
```bash
cd backend
python3 check_env.py
```
Script này sẽ kiểm tra tất cả cấu hình và báo lỗi cụ thể.

### Tip 2: Xem logs backend
Backend sẽ in ra logs khi khởi động:
- ✅ System initialized successfully → OK
- ❌ Configuration error → Sửa .env
- ❌ File error → Kiểm tra prompt_template.txt

### Tip 3: Development mode
Backend và Frontend đều có auto-reload:
- Backend: `--reload` flag
- Frontend: `npm run dev`

Chỉnh sửa code → Tự động reload!

---

**Estimated Setup Time**: 5-10 phút  
**Difficulty**: Easy  
**Version**: 2.0.0
