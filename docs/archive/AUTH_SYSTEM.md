# 🔐 Authentication & Authorization System

## 📋 Tổng quan

Hệ thống SPX Classification v2.1 với authentication và authorization hoàn chỉnh:

### Roles:
- **Admin**: Quản lý toàn bộ hệ thống
- **User**: Sử dụng hệ thống để xử lý data

## 🎯 Tính năng

### 1. Authentication
- ✅ Login với username/password
- ✅ JWT token-based authentication
- ✅ Force password change on first login
- ✅ Secure password hashing (bcrypt)

### 2. Authorization
- ✅ Role-based access control (RBAC)
- ✅ Admin và User roles
- ✅ Permission checks trên mọi endpoints

### 3. User Management (Admin only)
- ✅ Tạo user mới
- ✅ Set password mặc định
- ✅ Xem danh sách users
- ✅ Xóa users
- ✅ Force password change

### 4. Topic Management (Admin only)
- ✅ Tạo topics xử lý
- ✅ Cấu hình LLM cho mỗi topic
- ✅ Quản lý prompt templates
- ✅ Update/Delete topics

### 5. Task Management
- ✅ User chỉ thấy tasks của mình
- ✅ Admin thấy tất cả tasks
- ✅ Cancel task bất kỳ lúc nào
- ✅ Download khi completed

## 🏗️ Database Schema

### Users Collection:
```javascript
{
  _id: ObjectId,
  username: String (unique),
  password: String (hashed),
  role: String (admin|user),
  must_change_password: Boolean,
  created_at: Date
}
```

### Topics Collection:
```javascript
{
  _id: ObjectId,
  name: String (unique),
  description: String,
  llm_provider: String,
  model: String,
  api_base_url: String,
  api_key: String (encrypted),
  prompt_template: String,
  temperature: Number,
  max_tokens: Number,
  created_by: String,
  created_at: Date
}
```

### Tasks Collection:
```javascript
{
  _id: ObjectId,
  job_id: String (unique),
  topic_id: String,
  topic_name: String,
  user: String,
  status: String,
  filename: String,
  rows: Number,
  progress: Number,
  stats: Object,
  error: String,
  created_at: Date,
  updated_at: Date
}
```

## 🔑 API Endpoints

### Authentication:
```bash
POST /api/auth/login
POST /api/auth/change-password
GET  /api/auth/me
```

### User Management (Admin):
```bash
POST   /api/auth/users
GET    /api/auth/users
DELETE /api/auth/users/{username}
```

### Topic Management (Admin):
```bash
POST   /api/topics
GET    /api/topics
GET    /api/topics/{topic_id}
PUT    /api/topics/{topic_id}
DELETE /api/topics/{topic_id}
```

### Task Management:
```bash
POST   /api/upload?topic_id={id}
POST   /api/classify/{job_id}
GET    /api/tasks
GET    /api/status/{job_id}
DELETE /api/tasks/{job_id}
GET    /api/download/{job_id}
```

## 🚀 Workflow

### Admin Workflow:
```
1. Login (admin/admin123)
   ↓
2. Create Topics
   - Tên topic
   - LLM config (provider, model, API key)
   - Prompt template
   ↓
3. Create Users
   - Username
   - Default password
   - Role (user/admin)
   ↓
4. Monitor all tasks
   - View all users' tasks
   - Cancel/Delete any task
```

### User Workflow:
```
1. Login (username/password)
   ↓
2. Change Password (first time)
   ↓
3. Select Topic
   ↓
4. Upload File
   ↓
5. Start Processing
   ↓
6. Monitor Tasks
   - View own tasks only
   - Cancel own tasks
   - Download completed tasks
```

## 🔐 Security Features

### 1. Password Security
- Bcrypt hashing
- Salt rounds: 12
- Force change on first login

### 2. JWT Tokens
- HS256 algorithm
- 24 hours expiration
- Secure secret key

### 3. Authorization
- Role-based access control
- Permission checks on all endpoints
- User can only access own resources

### 4. API Key Protection
- API keys encrypted in database
- Hidden from non-admin users
- Secure transmission

## 📱 Frontend Changes

### New Pages:
1. **Login Page** - Authentication
2. **Change Password** - First login
3. **Admin Dashboard**:
   - User Management
   - Topic Management
   - All Tasks View
4. **User Dashboard**:
   - Topic Selection
   - Upload File
   - My Tasks

### Navigation:
```
Login → Dashboard
         ├─ Admin:
         │   ├─ Users
         │   ├─ Topics
         │   └─ All Tasks
         └─ User:
             ├─ Upload (with topic selection)
             └─ My Tasks
```

## 🛠️ Setup

### 1. Environment Variables:
```env
# Add to .env
SECRET_KEY=your-secret-key-here-change-in-production
```

### 2. Default Admin:
```
Username: admin
Password: admin123
```

### 3. Create First User:
```bash
# Login as admin
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Create user
curl -X POST http://localhost:8000/api/auth/users \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"username":"user1","password":"user123","role":"user"}'
```

### 4. Create First Topic:
```bash
curl -X POST http://localhost:8000/api/topics \
  -H "Authorization: Bearer {admin_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "SPX Feedback Classification",
    "description": "Phân loại feedback khách hàng SPX",
    "llm_provider": "openai",
    "model": "gpt-4",
    "api_base_url": "https://api.openai.com/v1",
    "api_key": "sk-xxx",
    "prompt_template": "...",
    "temperature": 0.0,
    "max_tokens": 150
  }'
```

## 🔍 Permission Matrix

| Action | Admin | User |
|--------|-------|------|
| Login | ✅ | ✅ |
| Change Password | ✅ | ✅ |
| Create Users | ✅ | ❌ |
| View All Users | ✅ | ❌ |
| Delete Users | ✅ | ❌ |
| Create Topics | ✅ | ❌ |
| View Topics | ✅ | ✅ (without API key) |
| Update Topics | ✅ | ❌ |
| Delete Topics | ✅ | ❌ |
| Upload File | ✅ | ✅ |
| View All Tasks | ✅ | ❌ |
| View Own Tasks | ✅ | ✅ |
| Cancel Own Task | ✅ | ✅ |
| Cancel Any Task | ✅ | ❌ |
| Download Own Result | ✅ | ✅ |
| Download Any Result | ✅ | ❌ |

## 💡 Best Practices

### For Admins:
1. Change default admin password immediately
2. Use strong passwords for all users
3. Regularly review user access
4. Monitor task usage
5. Backup topic configurations

### For Users:
1. Change password on first login
2. Use strong passwords
3. Select correct topic before upload
4. Monitor task progress
5. Download results promptly

## 🔄 Migration from v2.0

### Database Changes:
```javascript
// Add to existing tasks
db.tasks.updateMany({}, {
  $set: {
    user: "admin",  // Set default user
    topic_id: "default_topic_id"
  }
})
```

### API Changes:
- All endpoints now require authentication
- Upload endpoint requires topic_id parameter
- Tasks filtered by user (except admin)

---

**Version**: 2.1.0  
**Features**: Authentication + Authorization + Multi-tenant  
**Security**: JWT + Bcrypt + RBAC  
**Status**: ✅ Ready for Production
