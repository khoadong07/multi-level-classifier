# 🚀 SPX Classification System - Next.js Version

Hệ thống phân loại feedback SPX với giao diện Next.js và backend FastAPI.

## 🏗️ Kiến trúc

```
┌─────────────────┐         ┌─────────────────┐
│   Next.js       │ ◄─────► │   FastAPI       │
│   Frontend      │  HTTP   │   Backend       │
│   (Port 3000)   │         │   (Port 8000)   │
└─────────────────┘         └─────────────────┘
                                     │
                                     ▼
                            ┌─────────────────┐
                            │  Classification │
                            │     Engine      │
                            │  (app/core/)    │
                            └─────────────────┘
```

## 📁 Cấu trúc dự án

```
.
├── frontend/                 # Next.js application
│   ├── src/
│   │   ├── app/             # App router
│   │   │   ├── page.tsx     # Main page
│   │   │   ├── layout.tsx   # Root layout
│   │   │   └── globals.css  # Global styles
│   │   └── components/      # React components
│   │       ├── FileUpload.tsx
│   │       ├── ConfigPanel.tsx
│   │       ├── ProcessingPanel.tsx
│   │       └── ResultsPanel.tsx
│   ├── package.json
│   ├── tsconfig.json
│   └── tailwind.config.js
│
├── backend/                  # FastAPI application
│   ├── main.py              # API endpoints
│   └── requirements.txt     # Python dependencies
│
├── app/                      # Shared core logic
│   ├── core/                # Business logic
│   ├── models/              # Data models
│   └── utils/               # Utilities
│
├── docker-compose-fullstack.yml
├── Dockerfile.backend
└── frontend/Dockerfile
```

## 🚀 Quick Start

### Phương pháp 1: Development (Khuyến nghị)

#### 1. Backend Setup

```bash
# Cài đặt Python dependencies
pip install -r backend/requirements.txt

# Cấu hình environment
cp .env.example .env
# Chỉnh sửa .env với API credentials

# Chạy backend
cd backend
uvicorn main:app --reload --port 8000
```

Backend sẽ chạy tại: http://localhost:8000

#### 2. Frontend Setup

```bash
# Cài đặt Node dependencies
cd frontend
npm install

# Chạy development server
npm run dev
```

Frontend sẽ chạy tại: http://localhost:3000

### Phương pháp 2: Docker (Production)

```bash
# Build và chạy tất cả services
docker-compose -f docker-compose-fullstack.yml up --build

# Hoặc chạy ở background
docker-compose -f docker-compose-fullstack.yml up -d
```

Truy cập:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 🎨 Giao diện

### 1. Upload Tab
- Drag & drop hoặc click để chọn file Excel
- Validation file format (.xlsx)
- Hiển thị thông tin file sau khi upload

### 2. Config Tab
- Xem cấu hình hệ thống (Model, API, Workers)
- Quản lý cache (xem size, xóa cache)

### 3. Processing Tab
- Bắt đầu phân loại
- Tùy chọn xóa cache trước khi xử lý
- Progress bar real-time
- Hiển thị statistics (cache hits, API calls, failed)

### 4. Results Tab
- Xem thống kê chi tiết
- Tải xuống file đã phân loại
- Hiển thị tỷ lệ thành công

## 🔧 API Endpoints

### Backend API (FastAPI)

```
GET  /                          # Health check
GET  /api/config                # Get system config
POST /api/upload                # Upload Excel file
POST /api/classify/{job_id}     # Start classification
GET  /api/status/{job_id}       # Get job status
GET  /api/download/{job_id}     # Download result
DELETE /api/cache               # Clear cache
GET  /api/cache/stats           # Cache statistics
```

API Documentation: http://localhost:8000/docs

## 🎯 Features

### Frontend (Next.js)
- ✅ Modern UI với Tailwind CSS
- ✅ TypeScript cho type safety
- ✅ Real-time progress tracking
- ✅ Responsive design
- ✅ File upload với drag & drop
- ✅ Statistics visualization

### Backend (FastAPI)
- ✅ RESTful API
- ✅ Background task processing
- ✅ File upload/download
- ✅ Job queue management
- ✅ CORS support
- ✅ Auto-generated API docs

### Core Engine
- ✅ Concurrent processing
- ✅ Smart caching
- ✅ Retry logic
- ✅ Error handling

## 📊 Workflow

```
1. Upload File
   ↓
2. File Validation
   ↓
3. Create Job
   ↓
4. Start Classification (Background Task)
   ↓
5. Process Batch (Concurrent)
   ├─ Check Cache
   ├─ Call LLM API
   └─ Update Cache
   ↓
6. Save Results
   ↓
7. Download File
```

## 🛠️ Development

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Run dev server
npm run dev

# Build for production
npm run build

# Start production server
npm start

# Lint code
npm run lint
```

### Backend Development

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run with auto-reload
uvicorn main:app --reload

# Run with custom host/port
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 🐳 Docker Commands

```bash
# Build images
docker-compose -f docker-compose-fullstack.yml build

# Start services
docker-compose -f docker-compose-fullstack.yml up

# Stop services
docker-compose -f docker-compose-fullstack.yml down

# View logs
docker-compose -f docker-compose-fullstack.yml logs -f

# Restart services
docker-compose -f docker-compose-fullstack.yml restart
```

## 🔐 Environment Variables

```env
# Backend (.env)
OPENAI_API_KEY=your_api_key
OPENAI_BASE_URL=https://api.openai.com/v1
MODEL=gpt-4
MAX_WORKERS=10
MAX_RETRY=3
RETRY_WAIT=0.5
TEMPERATURE=0
MAX_TOKENS=150
```

## 📝 Tech Stack

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **Icons**: Lucide React

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.11
- **Server**: Uvicorn
- **Data Processing**: Pandas
- **LLM**: OpenAI API

### DevOps
- **Containerization**: Docker
- **Orchestration**: Docker Compose

## 🎓 Best Practices

### Frontend
- ✅ TypeScript strict mode
- ✅ Component-based architecture
- ✅ Responsive design
- ✅ Error boundaries
- ✅ Loading states

### Backend
- ✅ RESTful API design
- ✅ Background task processing
- ✅ Proper error handling
- ✅ API documentation
- ✅ CORS configuration

## 🐛 Troubleshooting

### Frontend không kết nối được Backend
```bash
# Kiểm tra backend đang chạy
curl http://localhost:8000/

# Kiểm tra CORS settings trong backend/main.py
```

### Port đã được sử dụng
```bash
# Frontend (3000)
lsof -ti:3000 | xargs kill -9

# Backend (8000)
lsof -ti:8000 | xargs kill -9
```

### Docker build lỗi
```bash
# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker-compose -f docker-compose-fullstack.yml build --no-cache
```

## 📚 Documentation

- **Frontend**: Next.js docs - https://nextjs.org/docs
- **Backend**: FastAPI docs - https://fastapi.tiangolo.com
- **Tailwind**: https://tailwindcss.com/docs

## 🎉 Kết luận

Hệ thống SPX Classification với Next.js frontend cung cấp:
- ✅ Giao diện hiện đại, responsive
- ✅ API RESTful tách biệt
- ✅ Real-time progress tracking
- ✅ Easy deployment với Docker
- ✅ Type-safe với TypeScript

---

**Version**: 2.0.0  
**Stack**: Next.js + FastAPI  
**Last Updated**: November 2025
