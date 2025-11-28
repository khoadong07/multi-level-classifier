# ✅ SPX Classification System - READY TO USE

## 🎉 Hệ thống đã sẵn sàng!

Backend và cấu hình đã được thiết lập thành công:
- ✅ Model: **unsloth/Qwen2.5-7B-Instruct**
- ✅ API: **http://103.232.122.80:8000/v1/**
- ✅ Docker volumes: cache, uploads, outputs
- ✅ Environment variables: Configured

## 🚀 Chạy ngay (3 cách)

### 1️⃣ Docker - Full Stack (Khuyến nghị)

```bash
# Chạy cả Backend + Frontend
docker-compose -f docker-compose-fullstack.yml up -d

# Xem logs
docker-compose -f docker-compose-fullstack.yml logs -f

# Dừng
docker-compose -f docker-compose-fullstack.yml down
```

**Truy cập:**
- 🌐 Frontend: http://localhost:3000
- 🔌 Backend API: http://localhost:8000
- 📚 API Docs: http://localhost:8000/docs

---

### 2️⃣ Docker - Chỉ Backend

```bash
# Chạy backend
docker-compose -f docker-compose-fullstack.yml up -d backend

# Test
curl http://localhost:8000/api/config
```

Sau đó chạy frontend local:
```bash
cd frontend
npm install
npm run dev
```

---

### 3️⃣ Development Mode (No Docker)

**Terminal 1 - Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

---

## 📱 Sử dụng

### Bước 1: Truy cập
Mở browser: **http://localhost:3000**

### Bước 2: Upload File Excel
- Tab "Tải lên"
- File phải có 3 cột: **Title**, **Content**, **Description**
- Kéo thả hoặc click chọn file

### Bước 3: Phân loại
- Tab "Xử lý"
- Click "🚀 Bắt đầu phân loại"
- Xem progress real-time

### Bước 4: Tải kết quả
- Tab "Kết quả"
- Click "📥 Tải xuống file đã phân loại"
- File sẽ có thêm 5 cột: `label_en`, `label_1`, `label_2`, `label_3`, `label_4`

---

## 🔍 Kiểm tra

### Backend OK?
```bash
curl http://localhost:8000/
# {"status":"ok","version":"2.0.0"}

curl http://localhost:8000/api/config
# {"model":"unsloth/Qwen2.5-7B-Instruct",...}
```

### Frontend OK?
```bash
curl http://localhost:3000/
# Hoặc mở browser
```

### Docker containers?
```bash
docker-compose -f docker-compose-fullstack.yml ps
# Xem status của containers
```

---

## 📊 File Excel Format

### Input (Required):
| Title | Content | Description |
|-------|---------|-------------|
| Giao hàng nhanh | Tài xế nhiệt tình | Hài lòng |
| Website lag | Trang web giật | Cần cải thiện |

### Output (Added 5 columns):
| ... | label_en | label_1 | label_2 | label_3 | label_4 |
|-----|----------|---------|---------|---------|---------|
| ... | RIDER / Driver work condition / Workload & Work Hours | RIDER | Driver work condition | Workload & Work Hours | |

---

## 🛠️ Commands

### Docker:
```bash
# Start
docker-compose -f docker-compose-fullstack.yml up -d

# Logs
docker-compose -f docker-compose-fullstack.yml logs -f backend
docker-compose -f docker-compose-fullstack.yml logs -f frontend

# Restart
docker-compose -f docker-compose-fullstack.yml restart

# Stop
docker-compose -f docker-compose-fullstack.yml down

# Clean up (remove volumes)
docker-compose -f docker-compose-fullstack.yml down -v
```

### Development:
```bash
# Backend
cd backend
python3 check_env.py          # Check config
python3 test_connection.py    # Test API
uvicorn main:app --reload     # Run server

# Frontend
cd frontend
npm run dev                   # Development
npm run build                 # Build
npm start                     # Production
```

---

## ❓ Troubleshooting

### Port đã được sử dụng?
```bash
# Kill port 8000
lsof -ti:8000 | xargs kill -9

# Kill port 3000
lsof -ti:3000 | xargs kill -9
```

### Docker không chạy?
```bash
# Clean up
docker-compose -f docker-compose-fullstack.yml down -v
docker system prune -a

# Rebuild
docker-compose -f docker-compose-fullstack.yml up --build
```

### Frontend không kết nối Backend?
1. Check backend: `curl http://localhost:8000/`
2. Check CORS in `backend/main.py`
3. Restart both services

### Cache lỗi?
```bash
# Xóa cache volume
docker-compose -f docker-compose-fullstack.yml down -v
docker volume rm spx_new_112025_cache_data

# Hoặc xóa file local
rm classification_cache.json
```

---

## 📁 Cấu trúc Project

```
spx_classification/
├── frontend/              # Next.js app
│   ├── src/
│   │   ├── app/          # Pages
│   │   └── components/   # React components
│   └── package.json
│
├── backend/              # FastAPI app
│   ├── main.py          # API endpoints
│   ├── check_env.py     # Config checker
│   └── requirements.txt
│
├── app/                  # Core logic
│   ├── core/            # Business logic
│   ├── models/          # Data models
│   └── utils/           # Utilities
│
├── docker-compose-fullstack.yml
├── .env                 # Configuration
└── prompt_template.txt  # LLM prompt
```

---

## 📚 Documentation

- **START.md** - Quick start guide
- **SETUP.md** - Detailed setup
- **README_NEXTJS.md** - Next.js documentation
- **ARCHITECTURE.md** - System architecture
- **API Docs** - http://localhost:8000/docs

---

## 🎯 Quick Commands

```bash
# Start everything
docker-compose -f docker-compose-fullstack.yml up -d

# Check status
docker-compose -f docker-compose-fullstack.yml ps

# View logs
docker-compose -f docker-compose-fullstack.yml logs -f

# Stop everything
docker-compose -f docker-compose-fullstack.yml down
```

---

## 💡 Tips

1. **Cache**: Hệ thống tự động cache kết quả để tiết kiệm API calls
2. **Progress**: Theo dõi real-time progress trong tab "Xử lý"
3. **Statistics**: Xem chi tiết cache hits, API calls trong tab "Kết quả"
4. **API Docs**: Explore API tại http://localhost:8000/docs

---

## ✅ Checklist

- [x] Backend configured
- [x] Docker volumes created
- [x] Environment variables set
- [x] Cache system working
- [x] API connection tested
- [ ] Frontend running (run `docker-compose up -d`)
- [ ] Test with sample Excel file

---

## 🎉 Bắt đầu ngay!

```bash
# One command to rule them all
docker-compose -f docker-compose-fullstack.yml up -d

# Open browser
open http://localhost:3000
```

---

**Status**: ✅ Production Ready  
**Version**: 2.0.0  
**Stack**: Next.js + FastAPI + Docker  
**Model**: Qwen2.5-7B-Instruct (Self-hosted)  
**Last Updated**: November 2025
