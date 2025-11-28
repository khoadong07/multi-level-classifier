# 🔄 Workflow - SPX Classification System v2.1

## 📱 Giao diện đơn giản hóa

### 3 Tabs chính:

```
┌─────────────┬─────────────┬─────────────┬─────────────┐
│  Tải lên    │  Cấu hình   │   Xử lý     │   Tasks     │
└─────────────┴─────────────┴─────────────┴─────────────┘
```

## 🎯 Workflow mới (Đơn giản hơn)

### Bước 1: Tải lên
```
Tab "Tải lên"
  ↓
Upload file Excel
  ↓
Task được tạo (status: uploaded)
  ↓
Tự động chuyển sang tab "Xử lý"
```

### Bước 2: Thêm vào Queue
```
Tab "Xử lý"
  ↓
Tùy chọn: ☑️ Xóa cache
  ↓
Click "Thêm vào Queue"
  ↓
Task chuyển sang status: pending
  ↓
Tự động chuyển sang tab "Tasks"
```

### Bước 3: Xem & Download
```
Tab "Tasks"
  ↓
Xem tất cả tasks đang chạy
  ↓
Real-time progress (auto-refresh 3s)
  ↓
Task completed → Click Download
```

## 📊 Tab Details

### 1. Tab "Tải lên"
**Chức năng:**
- Upload file Excel (.xlsx)
- Validation: Phải có 3 cột (Title, Content, Description)
- Hiển thị thông tin file (tên, size, số dòng)

**Actions:**
- Drag & drop hoặc click chọn file
- Upload → Tạo task → Chuyển tab "Xử lý"

---

### 2. Tab "Cấu hình"
**Chức năng:**
- Xem system configuration
- Quản lý cache

**Hiển thị:**
- Model name
- API base URL
- Max workers
- Cache size

**Actions:**
- Xóa cache (button)

---

### 3. Tab "Xử lý"
**Chức năng:**
- Thêm task vào queue
- Tùy chọn xóa cache

**Hiển thị:**
- Thông báo sẵn sàng
- Checkbox: Xóa cache trước khi xử lý
- Button: "Thêm vào Queue"

**Actions:**
- Click button → Task pending → Chuyển tab "Tasks"

---

### 4. Tab "Tasks" (Chính)
**Chức năng:**
- Xem tất cả tasks
- Filter theo status
- Download khi completed
- Delete tasks

**Hiển thị:**
- Danh sách tasks với:
  - Filename
  - Status badge (pending/processing/completed/failed)
  - Progress bar (nếu processing)
  - Statistics (cache hits, API calls)
  - Actions (Download, Delete)

**Filter:**
- Tất cả
- Pending
- Processing
- Completed
- Failed

**Actions:**
- Download (nếu completed)
- Delete (nếu không processing)
- Auto-refresh mỗi 3 giây

## 🔄 Task Status Flow

```
uploaded → pending → processing → completed
                                ↓
                              failed
```

### Status Meanings:
- **uploaded**: File đã upload, chưa bắt đầu
- **pending**: Đang chờ worker xử lý
- **processing**: Đang được xử lý bởi worker
- **completed**: Hoàn thành, có thể download
- **failed**: Xử lý thất bại, xem error message

## 💡 Use Cases

### Case 1: Xử lý 1 file nhanh
```
1. Tab "Tải lên" → Upload file
2. Tab "Xử lý" → Click "Thêm vào Queue"
3. Tab "Tasks" → Đợi completed → Download
```

### Case 2: Xử lý nhiều files
```
1. Upload file 1 → Thêm vào queue
2. Upload file 2 → Thêm vào queue
3. Upload file 3 → Thêm vào queue
4. Tab "Tasks" → Xem tất cả progress
5. Download từng file khi completed
```

### Case 3: Xử lý file lớn
```
1. Upload file 10,000 rows
2. Thêm vào queue
3. Làm việc khác (đóng browser cũng được)
4. Quay lại sau → Tab "Tasks" → Download
```

## 🎨 UI Components

### Task Card:
```
┌─────────────────────────────────────────────────┐
│ 🟢 filename.xlsx                    [completed] │
│                                                  │
│ Số dòng: 1000        Tiến trình: 100%          │
│ Cache hits: 800      API calls: 200            │
│                                                  │
│ [📥 Download]  [🗑️ Delete]                      │
└─────────────────────────────────────────────────┘
```

### Status Icons:
- 🟢 Completed (green)
- 🔵 Processing (blue, spinning)
- 🟡 Pending (yellow)
- 🔴 Failed (red)
- ⚪ Uploaded (gray)

## 🚀 Advantages

### So với workflow cũ:
1. **Đơn giản hơn**: 3 tabs thay vì 5
2. **Tập trung**: Tất cả tasks ở 1 nơi
3. **Non-blocking**: Không cần đợi xử lý xong
4. **Batch-friendly**: Dễ xử lý nhiều files
5. **Persistent**: Tasks lưu trong database

## 📝 Tips

### Tip 1: Batch Upload
```
Upload nhiều files → Tất cả vào queue → Worker xử lý tuần tự
```

### Tip 2: Monitor Progress
```
Tab "Tasks" tự động refresh → Không cần F5
```

### Tip 3: Clean Up
```
Delete tasks đã download → Giữ danh sách sạch
```

### Tip 4: Filter
```
Filter "completed" → Xem tasks có thể download
Filter "processing" → Xem tasks đang chạy
```

## 🎯 Key Features

### Real-time Updates:
- Auto-refresh mỗi 3 giây
- Progress bar cập nhật liên tục
- Status badge thay đổi theo thời gian thực

### Smart Queue:
- Worker tự động nhận task pending
- Xử lý tuần tự, không conflict
- Có thể scale nhiều workers

### Persistent Storage:
- Tasks lưu trong MongoDB
- Không mất dữ liệu khi restart
- Có thể xem lịch sử

## ✅ Workflow Summary

```
Upload → Queue → Process → Download
  ↓        ↓        ↓         ↓
Tab 1   Tab 3    Tab 4     Tab 4
```

**Đơn giản, rõ ràng, hiệu quả!**

---

**Version**: 2.1.0  
**UI**: 3 Tabs (Simplified)  
**Focus**: Task Management  
**Date**: November 2025
