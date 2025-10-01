import cv2
from tkinter import Tk, Label, Button
from PIL import Image, ImageTk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime
from drowsiness import process_frame, export_log

cap = None
time_list = []
status_list = []
running = False

root = Tk()
root.title("Giám sát buồn ngủ - Việt")
root.geometry("1000x700")

video_frame = Label(root)
video_frame.pack(side="left", padx=10, pady=10)

status_label = Label(root, text="Trạng thái: Tỉnh táo", font=("Arial", 16))
status_label.pack(pady=5)

fig = Figure(figsize=(5,4))
ax = fig.add_subplot(111)
ax.set_title("Thời gian mất tập trung (Buồn ngủ)")
ax.set_xlabel("Thời gian")
ax.set_ylabel("Trạng thái")
ax.set_ylim(0,1)
line, = ax.plot([], [], 'r-')

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side="right", padx=10, pady=10)

def update_plot():
    if time_list:
        ax.clear()
        ax.set_title("Thời gian mất tập trung (Buồn ngủ)")
        ax.set_xlabel("Thời gian")
        ax.set_ylabel("Trạng thái")
        ax.set_ylim(0,1)
        ax.plot(time_list, status_list, 'r-')
        canvas.draw()
    if running:
        root.after(1000, update_plot)

def start_detection():
    global cap, running
    cap = cv2.VideoCapture(0)
    running = True

    def video_loop():
        if running:
            ret, frame = cap.read()
            if ret:
                frame, status = process_frame(frame)
                status_label.config(text=f"Trạng thái: {status}", fg="red" if status=="Buồn ngủ" else "green")

                time_list.append(datetime.now())
                status_list.append(1 if status=="Buồn ngủ" else 0)
                if len(time_list) > 100:
                    time_list.pop(0)
                    status_list.pop(0)

                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img)
                imgtk = ImageTk.PhotoImage(image=img)
                video_frame.imgtk = imgtk
                video_frame.configure(image=imgtk)

            video_frame.after(10, video_loop)

    video_loop()
    update_plot()

def stop_detection():
    global running
    running = False
    if cap:
        cap.release()
        cv2.destroyAllWindows()
    status_label.config(text="Webcam đã dừng", fg="blue")

def export_log_file():
    filename = export_log()
    status_label.config(text=f"Log đã xuất ra {filename}", fg="purple")

Button(root, text="Bắt đầu", command=start_detection, font=("Arial",14), bg="green", fg="white").pack(pady=5)
Button(root, text="Dừng", command=stop_detection, font=("Arial",14), bg="red", fg="white").pack(pady=5)
Button(root, text="Xuất Log", command=export_log_file, font=("Arial",14), bg="blue", fg="white").pack(pady=5)

root.mainloop()
