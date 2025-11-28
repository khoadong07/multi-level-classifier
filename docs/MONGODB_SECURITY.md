# Security Configuration

## Tổng quan

Dự án đã được cấu hình với xác thực cho cả MongoDB và Application để tăng cường bảo mật.

## 1. Tài khoản Application (Đăng nhập hệ thống)

### Thông tin đăng nhập mặc định:
- **Username**: `admin`
- **Password**: `admin123`
- **Role**: `admin`

Tài khoản này được tạo tự động khi khởi động backend lần đầu và được sử dụng để đăng nhập vào giao diện web.

### Thay đổi tài khoản admin mặc định:

Cập nhật trong file `.env`:
```bash
ADMIN_USERNAME=your_admin_username
ADMIN_PASSWORD=your_secure_password
```

**Lưu ý**: Sau khi thay đổi, cần xóa user cũ trong database hoặc reset database:
```bash
docker-compose -f docker-compose-fullstack.yml down -v
docker-compose -f docker-compose-fullstack.yml up -d
```

## 2. MongoDB Database

### Thông tin đăng nhập mặc định:
- **Username**: `admin`
- **Password**: `spx_secure_password_2024`
- **Database**: `spx_classification`

### Connection String:
```
mongodb://admin:spx_secure_password_2024@mongodb:27017
```

## Thay đổi mật khẩu

### 1. Cập nhật file `.env`:
```bash
MONGODB_USERNAME=admin
MONGODB_PASSWORD=your_new_secure_password
MONGODB_URL=mongodb://admin:your_new_secure_password@mongodb:27017
DATABASE_NAME=spx_classification
```

### 2. Cập nhật file `.env.docker` (nếu sử dụng):
```bash
MONGODB_USERNAME=admin
MONGODB_PASSWORD=your_new_secure_password
MONGODB_URL=mongodb://admin:your_new_secure_password@mongodb:27017
DATABASE_NAME=spx_classification
```

### 3. Khởi động lại containers:
```bash
docker-compose -f docker-compose-fullstack.yml down -v
docker-compose -f docker-compose-fullstack.yml up -d
```

**Lưu ý**: Flag `-v` sẽ xóa volumes cũ. Chỉ sử dụng khi muốn reset hoàn toàn database.

## Biến môi trường

Các biến môi trường MongoDB trong `docker-compose-fullstack.yml`:

| Biến | Mô tả | Giá trị mặc định |
|------|-------|------------------|
| `MONGODB_USERNAME` | Username MongoDB | `admin` |
| `MONGODB_PASSWORD` | Password MongoDB | `spx_secure_password_2024` |
| `MONGODB_URL` | Connection string đầy đủ | `mongodb://admin:spx_secure_password_2024@mongodb:27017` |
| `DATABASE_NAME` | Tên database | `spx_classification` |

## Kết nối từ bên ngoài Docker

Nếu muốn kết nối MongoDB từ máy local (không qua Docker):

```bash
mongosh "mongodb://admin:spx_secure_password_2024@localhost:27017"
```

Hoặc sử dụng MongoDB Compass với connection string:
```
mongodb://admin:spx_secure_password_2024@localhost:27017
```

## Best Practices

1. **Đổi mật khẩu mặc định** ngay khi triển khai production
2. **Không commit** file `.env` vào Git (đã có trong `.gitignore`)
3. **Sử dụng mật khẩu mạnh**: ít nhất 16 ký tự, bao gồm chữ hoa, chữ thường, số và ký tự đặc biệt
4. **Backup định kỳ**: Sử dụng `mongodump` để backup database
5. **Giới hạn truy cập**: Trong production, không expose port 27017 ra ngoài

## Troubleshooting

### Lỗi xác thực
```
Authentication failed
```
**Giải pháp**: Kiểm tra username/password trong file `.env` và đảm bảo khớp với cấu hình MongoDB.

### Không thể kết nối
```
MongoServerError: connection refused
```
**Giải pháp**: 
1. Kiểm tra MongoDB container đang chạy: `docker ps`
2. Xem logs: `docker logs spx_mongodb`
3. Restart container: `docker-compose -f docker-compose-fullstack.yml restart mongodb`

### Reset mật khẩu
Nếu quên mật khẩu, cần xóa volume và tạo lại:
```bash
docker-compose -f docker-compose-fullstack.yml down -v
# Cập nhật mật khẩu mới trong .env
docker-compose -f docker-compose-fullstack.yml up -d
```

## Migration từ MongoDB không có password

Nếu đang có data trong MongoDB cũ (không có password):

1. **Backup data hiện tại**:
```bash
docker exec spx_mongodb mongodump --out=/data/backup
docker cp spx_mongodb:/data/backup ./mongodb_backup
```

2. **Cập nhật cấu hình** như hướng dẫn ở trên

3. **Khởi động lại với authentication**:
```bash
docker-compose -f docker-compose-fullstack.yml down -v
docker-compose -f docker-compose-fullstack.yml up -d
```

4. **Restore data**:
```bash
docker cp ./mongodb_backup spx_mongodb:/data/backup
docker exec spx_mongodb mongorestore --username admin --password spx_secure_password_2024 --authenticationDatabase admin /data/backup
```
