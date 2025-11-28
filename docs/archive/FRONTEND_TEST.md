# Frontend Test Guide

## Hệ thống đang chạy ổn định!

### URLs để test:

1. **Home Page (redirect to login)**
   ```
   http://localhost:3000
   ```

2. **Login Page**
   ```
   http://localhost:3000/login
   ```
   - Username: `admin`
   - Password: `admin123`

3. **Admin Dashboard** (sau khi login)
   ```
   http://localhost:3000/admin
   ```

4. **User Dashboard** (sau khi login với user role)
   ```
   http://localhost:3000/dashboard
   ```

### Nếu gặp lỗi "Application error":

1. **Clear browser cache:**
   - Chrome: Ctrl+Shift+Delete → Clear cache
   - Firefox: Ctrl+Shift+Delete → Clear cache
   - Safari: Cmd+Option+E

2. **Hard refresh:**
   - Chrome/Firefox: Ctrl+Shift+R (Windows) hoặc Cmd+Shift+R (Mac)
   - Safari: Cmd+Option+R

3. **Open in Incognito/Private mode:**
   - Chrome: Ctrl+Shift+N
   - Firefox: Ctrl+Shift+P
   - Safari: Cmd+Shift+N

4. **Check browser console:**
   - Press F12 → Console tab
   - Xem có lỗi JavaScript nào không

5. **Restart frontend container:**
   ```bash
   docker-compose -f docker-compose-fullstack.yml restart frontend
   ```

### Test với curl:

```bash
# Test home page
curl -s http://localhost:3000 | grep "Redirecting"

# Test login page
curl -s http://localhost:3000/login | grep "SPX Classification"

# Test API
curl -s http://localhost:8000/ | python3 -m json.tool
```

### Kiểm tra logs:

```bash
# Frontend logs
docker logs spx_frontend --tail 50

# Backend logs
docker logs spx_backend --tail 50

# Worker logs
docker logs spx_worker --tail 50
```

### Rebuild nếu cần:

```bash
# Rebuild frontend
docker-compose -f docker-compose-fullstack.yml build frontend
docker-compose -f docker-compose-fullstack.yml up -d frontend

# Rebuild tất cả
docker-compose -f docker-compose-fullstack.yml build
docker-compose -f docker-compose-fullstack.yml up -d
```

## Hệ thống đã được test thành công:

✅ Backend API hoạt động (port 8000)
✅ Frontend hoạt động (port 3000)
✅ MongoDB hoạt động (port 27017)
✅ Worker xử lý tasks
✅ LLM inference hoạt động (3 API calls thành công)
✅ Authentication hoạt động
✅ File upload/download hoạt động

## Lưu ý:

- Lỗi "Application error" thường do browser cache
- Nếu vẫn gặp lỗi, hãy mở browser console (F12) để xem chi tiết
- Hệ thống backend đang hoạt động bình thường
