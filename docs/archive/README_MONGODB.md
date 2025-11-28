# 🗄️ SPX Classification với MongoDB Queue System

## 🎯 Kiến trúc mới

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Next.js   │ ───► │   FastAPI   │ ───► │   MongoDB   │
│  Frontend   │      │   Backend   │      │   Database  │
└─────────────┘      └─────────────┘      └─────────────┘
                            │
                            ▼
                     ┌─────────────┐
                     │Queue Worker │
                     │  (Python)   │
                     └─────────────┘
```

## ✨ Tính năng mới

### 1. Queue System
- ✅ Upload file → Tạo task trong MongoDB
- ✅ Task được xử lý bởi worker riêng biệt
- ✅ Không cần đợi xử lý xong mới làm việc khác
- ✅ Có thể upload nhiều file cùng lúc

### 2. Task Management
- ✅ Xem danh sách tất cả tasks
- ✅ Filter theo status: pending, processing, completed, failed
- ✅ Real-time progress tracking
- ✅ Download khi task hoàn thành
- ✅ Xóa tasks không cần thiết

### 3. MongoDB Collections

#### Tasks Collection:
```json
{
  "_id": "ObjectId",
  "job_id": "uuid",
  "status": "pending|processing|completed|failed",
  "filename": "data.xlsx",
  "rows": 1000,
  "progress": 75,
  "stats": {
    "total_tasks": 1000,
    "cache_hits": 800,
    "api_calls": 200,
    "failed": 0,
    "success_rate": 100
  },
  "error": null,
  "created_at": "2025-11-28T...",
  "updated_at": "2025-11-28T..."
}
```

## 🚀 Chạy hệ thống

### Docker (Khuyến nghị):
```bash
# Start tất cả services (MongoDB + Backend + Worker + Frontend)
docker-compose -f docker-compose-fullstack.yml up -d

# Xem logs
docker-compose -f docker-compose-fullstack.yml logs -f

# Xem logs từng service
docker logs spx_mongodb -f
docker logs spx_backend -f
docker logs spx_worker -f
docker logs spx_frontend -f
```

### Development Mode:
```bash
# Terminal 1 - MongoDB
docker run -d -p 27017:27017 --name mongodb mongo:7.0

# Terminal 2 - Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Terminal 3 - Worker
cd backend
python3 queue_worker.py

# Terminal 4 - Frontend
cd frontend
npm install
npm run dev
```

## 📱 Sử dụng

### 1. Upload File
- Tab "Tải lên"
- Upload file Excel
- Task được tạo với status "uploaded"

### 2. Bắt đầu xử lý
- Tab "Xử lý"
- Click "Bắt đầu phân loại"
- Task chuyển sang status "pending"
- Worker tự động nhận và xử lý

### 3. Xem Tasks
- Tab "Tasks" (MỚI!)
- Xem tất cả tasks đang chạy
- Filter theo status
- Real-time progress
- Download khi hoàn thành

### 4. Kết quả
- Tab "Kết quả"
- Xem chi tiết task đã hoàn thành
- Download file

## 🔄 Workflow

```
1. Upload File
   ↓
2. Create Task (status: uploaded)
   ↓
3. Start Classification (status: pending)
   ↓
4. Worker picks up task (status: processing)
   ↓
5. Process with progress updates
   ↓
6. Complete (status: completed)
   ↓
7. Download result
```

## 🛠️ API Endpoints

### Tasks Management:
```bash
# List all tasks
GET /api/tasks

# List tasks by status
GET /api/tasks?status=pending

# Get task detail
GET /api/status/{job_id}

# Delete task
DELETE /api/tasks/{job_id}

# Upload file (creates task)
POST /api/upload

# Start classification (add to queue)
POST /api/classify/{job_id}

# Download result
GET /api/download/{job_id}
```

## 📊 Task Status Flow

```
uploaded → pending → processing → completed
                                ↓
                              failed
```

- **uploaded**: File đã upload, chưa bắt đầu xử lý
- **pending**: Đang chờ worker xử lý
- **processing**: Đang được xử lý
- **completed**: Hoàn thành thành công
- **failed**: Xử lý thất bại

## 🔍 Monitoring

### Check MongoDB:
```bash
# Connect to MongoDB
docker exec -it spx_mongodb mongosh

# Use database
use spx_classification

# List tasks
db.tasks.find().pretty()

# Count by status
db.tasks.countDocuments({status: "pending"})
db.tasks.countDocuments({status: "processing"})
db.tasks.countDocuments({status: "completed"})
```

### Check Worker:
```bash
# View worker logs
docker logs spx_worker -f

# Worker should show:
# 🔄 Queue worker started
# ✅ Connected to MongoDB
# 📋 Processing task: xxx
# ✅ Task xxx completed successfully
```

## 💡 Advantages

### So với hệ thống cũ:
1. **Non-blocking**: Không cần đợi xử lý xong
2. **Scalable**: Có thể chạy nhiều workers
3. **Persistent**: Tasks được lưu trong database
4. **Monitoring**: Xem tất cả tasks đang chạy
5. **Retry**: Có thể retry tasks failed
6. **History**: Lưu lịch sử tất cả tasks

## 🎯 Use Cases

### 1. Xử lý nhiều files:
```
Upload file 1 → pending
Upload file 2 → pending
Upload file 3 → pending
↓
Worker xử lý tuần tự
```

### 2. Xử lý file lớn:
```
Upload file 10,000 rows → pending
Làm việc khác
↓
Check tab "Tasks" để xem progress
↓
Download khi completed
```

### 3. Batch processing:
```
Upload 10 files cùng lúc
↓
Tất cả vào queue
↓
Worker xử lý từng file
↓
Download tất cả khi xong
```

## 🔧 Configuration

### Environment Variables:
```env
# MongoDB
MONGODB_URL=mongodb://mongodb:27017
DATABASE_NAME=spx_classification

# Worker
MAX_WORKERS=10  # Số workers xử lý đồng thời
```

### Scale Workers:
```bash
# Chạy nhiều workers (trong docker-compose)
docker-compose -f docker-compose-fullstack.yml up -d --scale worker=3
```

## 📚 Database Schema

### Tasks Collection:
```javascript
{
  _id: ObjectId,
  job_id: String (UUID),
  status: String (enum),
  filename: String,
  rows: Number,
  progress: Number (0-100),
  stats: {
    total_tasks: Number,
    cache_hits: Number,
    api_calls: Number,
    failed: Number,
    success_rate: Number
  },
  error: String (nullable),
  created_at: Date,
  updated_at: Date
}
```

### Indexes:
```javascript
db.tasks.createIndex({ job_id: 1 })
db.tasks.createIndex({ status: 1 })
db.tasks.createIndex({ created_at: -1 })
```

## ✅ Checklist

- [x] MongoDB container
- [x] Backend API với MongoDB
- [x] Queue worker
- [x] Task management endpoints
- [x] Frontend TaskList component
- [x] Real-time progress tracking
- [x] Download completed tasks
- [x] Delete tasks
- [x] Filter by status

---

**Version**: 2.1.0  
**New Features**: MongoDB Queue System  
**Stack**: Next.js + FastAPI + MongoDB + Worker  
**Last Updated**: November 2025
