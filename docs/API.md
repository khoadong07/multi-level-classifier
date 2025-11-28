# KMLC API Documentation

Base URL: `http://localhost:8000`

## Authentication

All endpoints except `/api/auth/login` require JWT authentication.

**Header Format:**
```
Authorization: Bearer <token>
```

## Endpoints

### Health Check

#### GET /
Check API health status.

**Response:**
```json
{
  "status": "ok",
  "version": "2.1.0",
  "service": "KMLC"
}
```

---

### Authentication

#### POST /api/auth/login
User login.

**Request Body:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "user": {
    "username": "admin",
    "role": "admin",
    "must_change_password": false
  }
}
```

#### POST /api/auth/change-password
Change user password.

**Request Body:**
```json
{
  "old_password": "oldpass",
  "new_password": "newpass"
}
```

**Response:**
```json
{
  "message": "Password changed successfully"
}
```

#### GET /api/auth/me
Get current user information.

**Response:**
```json
{
  "username": "admin",
  "role": "admin",
  "must_change_password": false
}
```

#### POST /api/auth/users
Create new user (Admin only).

**Request Body:**
```json
{
  "username": "newuser",
  "password": "password123",
  "role": "user"
}
```

**Response:**
```json
{
  "message": "User created successfully",
  "user_id": "507f1f77bcf86cd799439011",
  "username": "newuser",
  "default_password": "password123"
}
```

#### GET /api/auth/users
List all users (Admin only).

**Response:**
```json
{
  "users": [
    {
      "username": "admin",
      "role": "admin",
      "must_change_password": false,
      "created_at": "2025-11-28T10:00:00"
    }
  ]
}
```

#### DELETE /api/auth/users/{username}
Delete user (Admin only).

**Response:**
```json
{
  "message": "User deleted successfully"
}
```

---

### Topics

#### POST /api/topics
Create new topic (Admin only).

**Request Body:**
```json
{
  "name": "Customer Feedback",
  "description": "Classify customer feedback",
  "llm_provider": "openai",
  "model": "gpt-3.5-turbo",
  "api_base_url": "https://api.openai.com/v1",
  "api_key": "sk-...",
  "prompt_template": "Classify: {title}\n{content}\n{description}",
  "temperature": 0.0,
  "max_tokens": 150
}
```

**Response:**
```json
{
  "message": "Topic created successfully",
  "topic_id": "507f1f77bcf86cd799439011"
}
```

#### GET /api/topics
List all topics.

**Response:**
```json
{
  "topics": [
    {
      "topic_id": "507f1f77bcf86cd799439011",
      "name": "Customer Feedback",
      "description": "Classify customer feedback",
      "llm_provider": "openai",
      "model": "gpt-3.5-turbo",
      "created_at": "2025-11-28T10:00:00"
    }
  ]
}
```

#### GET /api/topics/{topic_id}
Get topic details.

**Response:**
```json
{
  "topic_id": "507f1f77bcf86cd799439011",
  "name": "Customer Feedback",
  "description": "Classify customer feedback",
  "llm_provider": "openai",
  "model": "gpt-3.5-turbo",
  "api_base_url": "https://api.openai.com/v1",
  "prompt_template": "Classify: {title}\n{content}\n{description}",
  "temperature": 0.0,
  "max_tokens": 150,
  "created_at": "2025-11-28T10:00:00"
}
```

#### PUT /api/topics/{topic_id}
Update topic (Admin only).

**Request Body:** (same as create, all fields optional)

**Response:**
```json
{
  "message": "Topic updated successfully"
}
```

#### DELETE /api/topics/{topic_id}
Delete topic (Admin only).

**Response:**
```json
{
  "message": "Topic deleted successfully"
}
```

---

### Tasks

#### POST /api/upload
Upload Excel file for classification.

**Request:** (multipart/form-data)
- `file`: Excel file (.xlsx)
- `topic_id`: Topic ID

**Response:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "data.xlsx",
  "rows": 100,
  "topic": "Customer Feedback"
}
```

#### POST /api/classify/{job_id}
Start classification task.

**Query Parameters:**
- `clear_cache`: boolean (optional, default: false)

**Response:**
```json
{
  "message": "Task added to queue",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending"
}
```

#### GET /api/status/{job_id}
Get task status and progress.

**Response:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "topic_id": "507f1f77bcf86cd799439011",
  "topic_name": "Customer Feedback",
  "user": "admin",
  "status": "completed",
  "filename": "data.xlsx",
  "rows": 100,
  "progress": 100,
  "stats": {
    "total_tasks": 100,
    "cache_hits": 20,
    "api_calls": 80,
    "failed": 0,
    "success_rate": 100.0
  },
  "error": null,
  "created_at": "2025-11-28T10:00:00",
  "updated_at": "2025-11-28T10:05:00"
}
```

#### GET /api/tasks
List tasks.

**Query Parameters:**
- `status`: string (optional) - Filter by status
- `limit`: int (optional, default: 100)
- `skip`: int (optional, default: 0)

**Response:**
```json
{
  "tasks": [...],
  "count": 10
}
```

#### DELETE /api/tasks/{job_id}
Delete or cancel task.

**Response:**
```json
{
  "message": "Task deleted successfully"
}
```

#### GET /api/download/{job_id}
Download classified result file.

**Response:** Excel file download

---

### Cache

#### DELETE /api/cache
Clear classification cache (Admin only).

**Response:**
```json
{
  "message": "Cache cleared successfully"
}
```

#### GET /api/cache/stats
Get cache statistics.

**Response:**
```json
{
  "size": 150,
  "entries": ["key1", "key2", "..."]
}
```

---

## Status Codes

- `200` - Success
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Unprocessable Entity
- `500` - Internal Server Error
- `503` - Service Unavailable

## Task Status Values

- `uploaded` - File uploaded, waiting to start
- `pending` - In queue, waiting for worker
- `processing` - Currently being processed
- `completed` - Successfully completed
- `failed` - Processing failed
- `cancelled` - Cancelled by user

## Error Response Format

```json
{
  "detail": "Error message here"
}
```
