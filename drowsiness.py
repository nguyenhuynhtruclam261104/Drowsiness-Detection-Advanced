import cv2
import mediapipe as mp
import numpy as np
from playsound import playsound
import threading
import time

# Mediapipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False,
                                  max_num_faces=1,
                                  refine_landmarks=True,
                                  min_detection_confidence=0.5,
                                  min_tracking_confidence=0.5)

# Landmark index cho mắt (Mediapipe 468 điểm)
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [263, 387, 385, 362, 380, 373]

# Hàm tính EAR (Eye Aspect Ratio)
def eye_aspect_ratio(landmarks, eye_idx, img_w, img_h):
    points = [(int(landmarks[idx].x * img_w), int(landmarks[idx].y * img_h)) for idx in eye_idx]

    # EAR công thức
    A = np.linalg.norm(np.array(points[1]) - np.array(points[5]))
    B = np.linalg.norm(np.array(points[2]) - np.array(points[4]))
    C = np.linalg.norm(np.array(points[0]) - np.array(points[3]))
    ear = (A + B) / (2.0 * C)
    return ear

# Cảnh báo bằng âm thanh
def sound_alarm(path):
    playsound(path)

# Biến cờ cho cảnh báo
alarm_on = False

# Bắt đầu webcam
cap = cv2.VideoCapture(0)

EAR_THRESH = 0.25   # Ngưỡng mắt nhắm
EAR_CONSEC_FRAMES = 20  # Số frame liên tiếp

counter = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            leftEAR = eye_aspect_ratio(face_landmarks.landmark, LEFT_EYE, w, h)
            rightEAR = eye_aspect_ratio(face_landmarks.landmark, RIGHT_EYE, w, h)
            ear = (leftEAR + rightEAR) / 2.0

            cv2.putText(frame, f"EAR: {ear:.2f}", (30, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            if ear < EAR_THRESH:
                counter += 1
                if counter >= EAR_CONSEC_FRAMES:
                    if not alarm_on:
                        alarm_on = True
                        t = threading.Thread(target=sound_alarm, args=("alarm.mp3",))
                        t.daemon = True
                        t.start()
                    cv2.putText(frame, "DROWSINESS ALERT!", (100, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
            else:
                counter = 0
                alarm_on = False

    cv2.imshow("Drowsiness Detection (Mediapipe)", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
