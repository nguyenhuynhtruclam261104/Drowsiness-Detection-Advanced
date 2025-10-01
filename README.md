# Drowsiness-Detection-Advanced
Cảnh báo ngủ gật 
# Drowsiness Detection Advanced (Mediapipe)

## 1. Mục đích
Dự án phát hiện **buồn ngủ khi lái xe hoặc khi sử dụng máy tính** thông qua webcam.  
- Nếu người dùng **nhắm mắt liên tục** quá ngưỡng, hệ thống sẽ **phát cảnh báo âm thanh**.  
- Có thể dùng để **demo trực tiếp trong lớp học** hoặc nghiên cứu.

---

## 2. Nguyên lý hoạt động

1. **Webcam** lấy hình ảnh trực tiếp của người dùng.
2. **Mediapipe Face Mesh** phát hiện khuôn mặt và các điểm landmark trên mắt.
3. **Tính toán Eye Aspect Ratio (EAR)**:
   - EAR là tỉ lệ giữa chiều cao và chiều rộng mắt.
   - Nếu EAR < ngưỡng (`EAR_THRESH`) trong một số frame liên tiếp (`EAR_CONSEC_FRAMES`) → xác định mắt đang nhắm → cảnh báo.
4. **Phát âm thanh cảnh báo** bằng file `alarm.mp3`.
5. (Tuỳ chọn) Có thể lưu log thời điểm buồn ngủ, hiển thị trạng thái Awake/Drowsy trực quan.

---

## 3. Cấu trúc thư mục

Drowsiness-Detection-Advanced/
│
├── drowsiness.py # Code chính
├── requirements.txt # Thư viện cần cài
└── alarm.mp3 # File âm thanh cảnh báo

yaml
Sao chép mã

---

## 4. Cài đặt thư viện

Chạy lệnh sau để cài các thư viện cần thiết:

```bash
pip install -r requirements.txt
Lưu ý: playsound cần dùng phiên bản 1.2.2 để chạy ổn định trên Windows.

---

## 5. Cách chạy dự án

Đặt file alarm.mp3 vào cùng thư mục với drowsiness.py.

Mở terminal, di chuyển đến thư mục dự án:

bash
Sao chép mã
cd D:\Drowsiness-Detection-Advanced
Chạy chương trình:

bash
Sao chép mã
python drowsiness.py
Webcam sẽ bật. Khi phát hiện buồn ngủ, sẽ hiển thị cảnh báo trên màn hình và phát âm thanh cảnh báo.

Nhấn q để thoát chương trình.

## 6. Tham số có thể chỉnh sửa

EAR_THRESH: ngưỡng tỉ lệ mắt nhắm (mặc định 0.25).

EAR_CONSEC_FRAMES: số frame liên tiếp mắt nhắm để cảnh báo (mặc định 20).

---

## 7. Demo lớp học

Mở webcam → để sinh viên thử nhắm mắt → hệ thống phát cảnh báo.

Có thể kết hợp ghi log hoặc hiển thị trạng thái trên GUI sau này.

---

## 8. Ghi chú

Dự án này dùng Mediapipe, không cần dlib.

Chạy tốt trên Windows, CPU bình thường, không cần GPU.

Có thể phát triển thêm:

Giao diện đồ họa (Tkinter/PyQt).

Lưu log CSV.

Hỗ trợ nhiều người cùng lúc.
