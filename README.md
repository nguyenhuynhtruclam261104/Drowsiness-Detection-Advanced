# Drowsiness-Detection-Advanced

**Ứng dụng giám sát buồn ngủ & mất tập trung bằng webcam**, hướng đến người Việt.  
Phù hợp cho học online, làm việc tại nhà hoặc nghiên cứu năng suất.

---

## Tính năng chính
- Nhận diện trạng thái mắt (Tỉnh táo / Buồn ngủ) theo **EAR (Eye Aspect Ratio)**.  
- Hiển thị video webcam trực tiếp trên GUI.  
- Biểu đồ **realtime** về % mất tập trung.  
- **Pop-up + âm thanh cảnh báo** khi buồn ngủ.  
- **Folder logs/** tự động tạo, lưu file CSV **tiếng Việt**.  
- Nút **Bắt đầu / Dừng / Xuất Log** linh hoạt.  
- File CSV chi tiết:
  - Thời gian bắt đầu / kết thúc buồn ngủ  
  - Giá trị EAR  
  - Trạng thái  
- Dữ liệu log dùng để phân tích năng suất học tập / làm việc.

---

## Yêu cầu môi trường
- Python >= 3.10  
- Các thư viện cần cài đặt:

opencv-python>=4.12.0
mediapipe>=1.12.0
scipy>=1.15.0
playsound>=1.2.2
pandas>=2.3.3
plyer>=2.1.0
pillow>=10.0.0
matplotlib>=3.8.0

css
Sao chép mã

Cài đặt nhanh bằng:
```bash
pip install -r requirements.txt
Cấu trúc thư mục
bash
Sao chép mã
Drowsiness-Detection-Advanced/
│
├─ drowsiness.py          # Logic detection, EAR, cảnh báo, log
├─ drowsiness_gui.py      # GUI Tkinter + biểu đồ realtime
├─ alarm.mp3              # File âm thanh cảnh báo
├─ logs/                  # Folder tự động lưu CSV tiếng Việt
├─ requirements.txt       # Thư viện cần cài đặt
└─ README.md
Hướng dẫn sử dụng
Chuẩn bị webcam và đặt alarm.mp3 trong cùng folder.

Chạy GUI:

bash
Sao chép mã
python drowsiness_gui.py
Trên GUI:

Bắt đầu: mở webcam, nhận diện buồn ngủ.

Dừng: tạm dừng webcam, giữ dữ liệu log.

Xuất Log: xuất CSV tiếng Việt vào folder logs/.

Biểu đồ realtime hiển thị % mất tập trung.

Lưu ý
Chỉ chạy trên máy có webcam.

File CSV tiếng Việt có dấu, mở trực tiếp bằng Excel.

Folder logs/ được tạo tự động, file có timestamp → dễ quản lý.
