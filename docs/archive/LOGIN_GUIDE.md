# Hướng Dẫn Đăng Nhập

## ✅ Hệ thống đã sẵn sàng!

### Thông tin đăng nhập mặc định:

```
Username: admin
Password: admin123
```

### Truy cập hệ thống:

1. **Frontend (Giao diện người dùng):**
   - URL: http://localhost:3000
   - Trang login sẽ tự động hiển thị

2. **Backend API:**
   - URL: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Các bước đăng nhập:

1. Mở trình duyệt và truy cập: http://localhost:3000
2. Nhập username: `admin`
3. Nhập password: `admin123`
4. Click "Đăng nhập"
5. Bạn sẽ được chuyển đến trang Admin Dashboard

### Tính năng Admin:

- **Quản lý người dùng**: Tạo, xóa user
- **Quản lý chủ đề**: Tạo topics với cấu hình LLM riêng
- **Xem tất cả tasks**: Theo dõi tiến trình xử lý của tất cả users
- **Quản lý hệ thống**: Xem cache, cấu hình

### Kiểm tra trạng thái hệ thống:

```bash
# Xem tất cả containers
docker ps

# Xem logs backend
docker logs spx_backend

# Xem logs worker
docker logs spx_worker

# Xem logs frontend
docker logs spx_frontend
```

### Khởi động lại hệ thống:

```bash
# Khởi động tất cả services
docker-compose -f docker-compose-fullstack.yml up -d

# Dừng tất cả services
docker-compose -f docker-compose-fullstack.yml down
```

### Lưu ý:

- Mật khẩu mặc định `admin123` nên được thay đổi trong môi trường production
- Admin có thể tạo user mới từ dashboard
- Mỗi user chỉ thấy tasks của mình, admin thấy tất cả
