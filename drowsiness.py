import cv2
import mediapipe as mp
from scipy.spatial import distance as dist
from threading import Thread
from playsound import playsound
from datetime import datetime
from plyer import notification
import os
import pandas as pd

EAR_THRESHOLD = 0.25
EAR_CONSEC_FRAMES = 20
ALERT_SOUND = "alarm.mp3"

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True)
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

log_list = []
COUNTER = 0
ALERTED = False

def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

def sound_alarm():
    playsound(ALERT_SOUND)

def process_frame(frame):
    global COUNTER, ALERTED
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(frame_rgb)
    status = "Tỉnh táo"

    if results.multi_face_landmarks:
        mesh_points = results.multi_face_landmarks[0].landmark
        h, w, _ = frame.shape
        left_eye = [(int(mesh_points[i].x*w), int(mesh_points[i].y*h)) for i in LEFT_EYE]
        right_eye = [(int(mesh_points[i].x*w), int(mesh_points[i].y*h)) for i in RIGHT_EYE]
        ear = (eye_aspect_ratio(left_eye) + eye_aspect_ratio(right_eye)) / 2.0

        for (x,y) in left_eye + right_eye:
            cv2.circle(frame, (x,y), 2, (0,255,0), -1)

        if ear < EAR_THRESHOLD:
            COUNTER += 1
            if COUNTER >= EAR_CONSEC_FRAMES and not ALERTED:
                ALERTED = True
                Thread(target=sound_alarm).start()
                notification.notify(title="Cảnh báo Buồn ngủ",
                                    message="Bạn có vẻ mệt mỏi! Hãy nghỉ ngơi một chút.",
                                    timeout=5)
                status = "Buồn ngủ"
                log_list.append({"start_time": datetime.now(), "end_time": None, "ear": ear})
        else:
            if ALERTED:
                ALERTED = False
                log_list[-1]["end_time"] = datetime.now()
            COUNTER = 0

    return frame, status

def export_log(filename=None):
    if not os.path.exists("logs"):
        os.makedirs("logs")

    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"logs/buonnngu_{timestamp}.csv"

    data = []
    for log in log_list:
        data.append({
            "Thời gian bắt đầu": log.get("start_time"),
            "Thời gian kết thúc": log.get("end_time"),
            "Giá trị EAR": log.get("ear"),
            "Trạng thái": "Buồn ngủ" if log.get("ear",0)<EAR_THRESHOLD else "Tỉnh táo"
        })

    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding="utf-8-sig")
    return filename
