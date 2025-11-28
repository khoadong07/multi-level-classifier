# 🚀 START HERE - SPX Classification System

## ✅ Hệ thống đã sẵn sàng!

Backend đã được cấu hình và chạy thành công với:
- **Model**: unsloth/Qwen2.5-7B-Instruct
- **API**: http://103.232.122.80:8000/v1/
- **Cache**: 32 entries

## 🎯 Chạy hệ thống (Chọn 1 trong 3 cách)

### 🐳 Cách 1: Docker (Khuyến nghị - Đơn giản nhất)

```bash
# Chạy cả Backend + Frontend
docker-compose -f docker-compose-fullstack.yml up -d

# Xem logs
docker-compose -f docker-compose-fullstack.yml logs -f

# Dừng
docker-compose -f docker-compose-fullstack.yml down
```

**Truy cập:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

### 💻 Cách 2: Development Mode (Cho developers)

#### Terminal 1 - Backend:
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

#### Terminal 2 - Frontend:
```bash
cd frontend
npm install
npm run dev
```

**Truy cập:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

---

### ⚡ Cách 3: Chỉ Backend (API only)

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

**Test API:**
```bash
# Health check
curl http://localhost:8000/

# Get config
curl http://localhost:8000/api/config

# API docs
open http://localhost:8000/docs
```

---

## 📱 Sử dụng giao diện

### Bước 1: Truy cập
Mở browser: **http://localhost:3000**

### Bước 2: Upload file
- Tab "Tải lên"
- Kéo thả hoặc click chọn file Excel (.xlsx)
- File phải có 3 cột: **Title**, **Content**, **Description**

### Bước 3: Xử lý
- Chuyển sang tab "Xử lý"
- Tùy chọn: ☑️ "Xóa cache trước khi xử lý" (nếu muốn phân loại lại)
- Click "🚀 Bắt đầu phân loại"
- Theo dõi progress bar real-time

### Bước 4: Tải kết quả
- Chuyển sang tab "Kết quả"
- Xem thống kê (cache hits, API calls, success rate)
- Click "📥 Tải xuống file đã phân loại"

---

## 🔍 Kiểm tra hệ thống

### Backend đang chạy?
```bash
curl http://localhost:8000/
# Kết quả: {"status":"ok","version":"2.0.0"}
```

### Config đúng chưa?
```bash
curl http://localhost:8000/api/config
# Kết quả: {"model":"unsloth/Qwen2.5-7B-Instruct",...}
```

### Frontend đang chạy?
```bash
curl http://localhost:3000/
# Hoặc mở browser: http://localhost:3000
```

---

## 📊 Cấu trúc file Excel

### Input (Cần có 3 cột):
| Title | Content | Description |
|-------|---------|-------------|
| Giao hàng nhanh | Tài xế rất nhiệt tình | Hài lòng với dịch vụ |
| Website lag | Trang web bị giật | Cần cải thiện |

### Output (Thêm 5 cột mới):
| ... | label_en | label_1 | label_2 | label_3 | label_4 |
|-----|----------|---------|---------|---------|---------|
| ... | RIDER / Driver work condition / Workload & Work Hours | RIDER | Driver work condition | Workload & Work Hours | |

---

## 🛠️ Commands hữu ích

### Docker:
```bash
# Xem logs
docker logs spx_backend -f

# Restart
docker-compose -f docker-compose-fullstack.yml restart

# Stop
docker-compose -f docker-compose-fullstack.yml down

# Rebuild
docker-compose -f docker-compose-fullstack.yml up --build
```

### Development:
```bash
# Backend
cd backend
python3 check_env.py          # Kiểm tra config
python3 test_connection.py    # Test API connection
uvicorn main:app --reload     # Chạy server

# Frontend
cd frontend
npm run dev                   # Development
npm run build                 # Build production
npm start                     # Production server
```

---

## ❓ Troubleshooting

### Port đã được sử dụng?
```bash
# Kill port 8000 (Backend)
lsof -ti:8000 | xargs kill -9

# Kill port 3000 (Frontend)
lsof -ti:3000 | xargs kill -9
```

### Frontend không kết nối Backend?
1. Kiểm tra backend: `curl http://localhost:8000/`
2. Kiểm tra CORS trong `backend/main.py`
3. Restart cả 2 services

### Docker không chạy?
```bash
# Clean up
docker-compose -f docker-compose-fullstack.yml down -v
docker system prune -a

# Rebuild
docker-compose -f docker-compose-fullstack.yml up --build
```

---

## 📚 Tài liệu

- **SETUP.md** - Hướng dẫn setup chi tiết
- **README_NEXTJS.md** - Tài liệu đầy đủ Next.js version
- **QUICKSTART_NEXTJS.md** - Quick start guide
- **ARCHITECTURE.md** - Kiến trúc hệ thống
- **API Docs** - http://localhost:8000/docs

---

## 🎉 Bắt đầu ngay!

```bash
# Chạy Docker (Dễ nhất)
docker-compose -f docker-compose-fullstack.yml up -d

# Mở browser
open http://localhost:3000
```

Hoặc:

```bash
# Terminal 1
cd backend && uvicorn main:app --reload

# Terminal 2
cd frontend && npm run dev

# Browser
open http://localhost:3000
```

---

**Status**: ✅ Ready to use  
**Version**: 2.0.0  
**Stack**: Next.js + FastAPI + Docker  
**Model**: Qwen2.5-7B-Instruct
