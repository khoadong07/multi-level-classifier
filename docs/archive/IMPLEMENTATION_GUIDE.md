# 🚀 Implementation Guide - Full Auth System

## ✅ Đã hoàn thành

### Backend:
- ✅ Authentication system (JWT + Bcrypt)
- ✅ User management endpoints
- ✅ Topic management endpoints  
- ✅ Protected task endpoints
- ✅ Database models (Users, Topics, Tasks)
- ✅ Default admin account

### Frontend:
- ✅ Login page
- ✅ Change password page
- ✅ Protected routes
- ✅ Auth utilities (lib/auth.ts, lib/api.ts)
- ✅ Navbar component
- ✅ Admin dashboard layout
- ✅ User dashboard layout
- ✅ User Management component

## 📝 Cần tạo thêm (Frontend Components)

### 1. Admin Components:

#### `frontend/src/components/admin/TopicManagement.tsx`
```typescript
- List all topics
- Create new topic (form with LLM config)
- Edit topic
- Delete topic
- Show: name, model, created_by, created_at
```

#### `frontend/src/components/admin/AllTasks.tsx`
```typescript
- List all tasks from all users
- Filter by status, user, topic
- Cancel/Delete any task
- Download any result
- Show: user, topic, filename, status, progress
```

### 2. User Components:

#### `frontend/src/components/user/UserUpload.tsx`
```typescript
- Select topic (dropdown)
- Upload Excel file
- Validate file
- Show upload success
- Redirect to tasks
```

#### `frontend/src/components/user/UserTasks.tsx`
```typescript
- List user's own tasks only
- Filter by status
- Real-time progress
- Cancel own task
- Download completed task
- Show: topic, filename, status, progress, stats
```

## 🔧 Implementation Steps

### Step 1: Complete Admin Components

```bash
# Create TopicManagement.tsx
- Form: name, description, llm_provider, model, api_base_url, api_key, prompt_template, temperature, max_tokens
- API: POST /api/topics, GET /api/topics, PUT /api/topics/{id}, DELETE /api/topics/{id}
- Table: Show all topics with edit/delete buttons

# Create AllTasks.tsx  
- API: GET /api/tasks (admin sees all)
- Table: user, topic_name, filename, status, progress, created_at
- Actions: Cancel, Delete, Download
```

### Step 2: Complete User Components

```bash
# Create UserUpload.tsx
- API: GET /api/topics (get list)
- Select topic dropdown
- File upload with topic_id
- API: POST /api/upload?topic_id={id}

# Create UserTasks.tsx
- API: GET /api/tasks (user sees own only)
- Real-time refresh every 3s
- Filter by status
- Actions: Cancel, Download
```

### Step 3: Update Worker

```typescript
// backend/queue_worker.py
- Load topic config for each task
- Use topic's LLM settings
- Use topic's prompt template
- Process with topic-specific config
```

### Step 4: Test Flow

```bash
# Admin Flow:
1. Login as admin
2. Create topic "SPX Feedback"
3. Create user "user1" / "pass123"
4. View all tasks

# User Flow:
1. Login as user1
2. Change password
3. Select topic "SPX Feedback"
4. Upload file
5. View my tasks
6. Download result
```

## 📦 Required npm packages

```bash
cd frontend
npm install axios
# Already installed: next, react, lucide-react, tailwindcss
```

## 🔑 Environment Variables

### Backend (.env):
```env
SECRET_KEY=your-secret-key-change-in-production-min-32-chars
MONGODB_URL=mongodb://mongodb:27017
DATABASE_NAME=spx_classification
```

### Frontend (.env.local):
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🐳 Docker Updates

### docker-compose-fullstack.yml:
```yaml
backend:
  environment:
    - SECRET_KEY=${SECRET_KEY}
    
worker:
  environment:
    - SECRET_KEY=${SECRET_KEY}
```

## 🧪 Testing

### 1. Test Authentication:
```bash
# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Get token, then:
curl -H "Authorization: Bearer {token}" \
  http://localhost:8000/api/auth/me
```

### 2. Test User Management:
```bash
# Create user
curl -X POST http://localhost:8000/api/auth/users \
  -H "Authorization: Bearer {admin_token}" \
  -H "Content-Type: application/json" \
  -d '{"username":"user1","password":"pass123","role":"user"}'
```

### 3. Test Topic Management:
```bash
# Create topic
curl -X POST http://localhost:8000/api/topics \
  -H "Authorization: Bearer {admin_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "SPX Feedback",
    "llm_provider": "openai",
    "model": "gpt-4",
    "api_base_url": "http://103.232.122.80:8000/v1/",
    "api_key": "DUMMY_KEY",
    "prompt_template": "...",
    "temperature": 0.0,
    "max_tokens": 150
  }'
```

## 📊 Component Structure

```
frontend/src/
├── app/
│   ├── page.tsx (redirect to login)
│   ├── login/page.tsx ✅
│   ├── change-password/page.tsx ✅
│   ├── admin/page.tsx ✅
│   └── dashboard/page.tsx ✅
├── components/
│   ├── Navbar.tsx ✅
│   ├── ProtectedRoute.tsx ✅
│   ├── admin/
│   │   ├── UserManagement.tsx ✅
│   │   ├── TopicManagement.tsx ⏳
│   │   └── AllTasks.tsx ⏳
│   └── user/
│       ├── UserUpload.tsx ⏳
│       └── UserTasks.tsx ⏳
└── lib/
    ├── auth.ts ✅
    └── api.ts ✅
```

## 🎯 Next Actions

1. **Create remaining components** (4 files)
2. **Update worker** to use topic config
3. **Add SECRET_KEY** to .env
4. **Test full flow**
5. **Deploy**

## 📝 Code Templates

### Topic Management Component Template:
```typescript
// Similar to UserManagement but for topics
- useState for topics list
- fetchTopics() function
- Create/Edit modal with form
- Delete confirmation
- Table display
```

### User Upload Component Template:
```typescript
- useState for topics, selectedTopic, file
- fetchTopics() on mount
- handleFileUpload() with topic_id
- Drag & drop support
- Progress indicator
```

### User Tasks Component Template:
```typescript
// Similar to existing TaskList but filtered
- Only show current user's tasks
- Real-time refresh
- Cancel button
- Download button when completed
```

---

**Status**: 70% Complete  
**Remaining**: 4 components + worker update  
**ETA**: 30 minutes
