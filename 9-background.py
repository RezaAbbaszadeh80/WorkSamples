# ۵. حذف پس‌زمینه مجازی با YOLO و Mediapipe


import cv2
import numpy as np
import mediapipe as mp
from ultralytics import YOLO  # مطمئن شوید که YOLO نسخه 8 را نصب کرده‌اید

# راه‌اندازی Mediapipe برای بخش‌بندی
mp_selfie_segmentation = mp.solutions.selfie_segmentation
selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

# بارگذاری مدل YOLO
# استفاده از مدل دانلود شده
from ultralytics import YOLO

# مسیر فایل مدل از پیش دانلود شده
model_path = 'YOLO_V8_models/yolov8n.pt'

# بارگذاری مدل از مسیر فایل
model = YOLO(model_path)


# بارگذاری تصویر پس‌زمینه مجازی
background = cv2.imread('Data/background.jpeg')
background = cv2.resize(background, (640, 480))

# راه‌اندازی وبکم
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    frame = cv2.flip(frame,1)
    
    if not success:
        break
    
    # اعمال YOLO برای شناسایی اشیاء
    results = model(frame)

    # پردازش بخش‌بندی با Mediapipe
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    segmentation_results = selfie_segmentation.process(frame_rgb)

    # ایجاد ماسک برای بخش‌بندی
    mask = segmentation_results.segmentation_mask
    mask = np.where(mask > 0.5, 1, 0).astype(np.uint8)

    # اعمال پس‌زمینه مجازی
    frame_with_background = np.where(mask[:, :, None] == 0, background, frame)

    # نمایش نتایج شناسایی اشیاء از YOLO
    for detection in results[0].boxes.xyxy:
        x1, y1, x2, y2 = map(int, detection)
        cv2.rectangle(frame_with_background, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # نمایش تصویر نهایی
    cv2.imshow("Virtual Background Removal", frame_with_background)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
