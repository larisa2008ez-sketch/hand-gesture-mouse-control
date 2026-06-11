import cv2
import mediapipe as mp
import pyautogui
import math
import numpy as np

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0

# new stable API MediaPipe
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

import urllib.request
import os
import ssl

model_path = 'hand_landmarker.task'
if not os.path.exists(model_path):
    print("Загрузка модели распознавания рук...")
    url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task"
    
    # ignore SSL verification errors on macOS
    context = ssl._create_unverified_context()
    with urllib.request.urlopen(url, context=context) as response, open(model_path, 'wb') as out_file:
        out_file.write(response.read())
# detection settings
options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=1
)

screen_width, screen_height = pyautogui.size()
is_dragging = False
frame_count = 0
cap = cv2.VideoCapture(0)

print("Программа запускается. Нажмите 'q' для выхода.")

with HandLandmarker.create_from_options(options) as landmarker:
    while cap.isOpened():
        success, frame = cap.read()
        if not success: break

        frame = cv2.flip(frame, 1)
        h, w, c = frame.shape
        
        # convert the frame to MediaPipe Image format
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        
        timestamp = frame_count * 33  # approx 30 frames per second (33 ms per frame)
        frame_count += 1
        
        # detect hand landmarks
        detection_result = landmarker.detect_for_video(mp_image, timestamp)

        if detection_result.hand_landmarks:
            hand_landmarks = detection_result.hand_landmarks[0]
           
            thumb = hand_landmarks[4]
            index = hand_landmarks[8]

            margin = 50
            x_mouse = int(np.interp(index.x * w, (margin, w - margin), (0, screen_width)))
            y_mouse = int(np.interp(index.y * h, (margin, h - margin), (0, screen_height)))

            #calculate the distance between fingers
            thumb_x, thumb_y = int(thumb.x * w), int(thumb.y * h)
            index_x, index_y = int(index.x * w), int(index.y * h)
            distance = math.hypot(index_x - thumb_x, index_y - thumb_y)

        
            cv2.circle(frame, (thumb_x, thumb_y), 8, (0, 255, 0), -1)
            cv2.circle(frame, (index_x, index_y), 8, (0, 255, 0), -1)
            
            if not is_dragging:
                pyautogui.moveTo(x_mouse, y_mouse)

            if distance < 30:
                if not is_dragging:
                    pyautogui.mouseDown()
                    is_dragging = True
                    print("Зажали")
                pyautogui.moveTo(x_mouse, y_mouse)
            else:
                if is_dragging:
                    pyautogui.mouseUp()
                    is_dragging = False
                    print("Отпустили")

        cv2.imshow('Hand Control', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()