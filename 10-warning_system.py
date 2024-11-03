import cv2
import numpy as np
from ultralytics import YOLO

# بارگذاری مدل YOLO
model_path = 'YOLO_V8_models/yolov8n.pt'  # مسیر فایل مدل YOLO
model = YOLO(model_path)

# تنظیمات دوربین
focal_length = 800  # طول کانونی دوربین (بسته به دوربین و تنظیمات)
real_object_width = 0.5  # عرض واقعی شیء (متر)

# تنظیمات هشدار
warning_distance = 1.0  # فاصله هشدار (متر)

# راه‌اندازی وبکم
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # اعمال YOLO برای شناسایی اشیاء
    results = model(frame)

    # پردازش نتایج شناسایی
    for result in results:
        for detection in result.boxes:
            x1, y1, x2, y2 = map(int, detection.xyxy[0])
            conf = detection.conf[0]

            obj_width = x2 - x1
            obj_height = y2 - y1

            # محاسبه فاصله تخمینی
            if obj_width > 0:  # اطمینان از اینکه عرض شیء بیشتر از صفر است
                distance = (real_object_width * focal_length) / obj_width

                # رسم مستطیل دور شیء
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # نمایش فاصله
                cv2.putText(frame, f'Distance: {distance:.2f}m', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # فعال‌سازی هشدار اگر فاصله کمتر از حد هشدار باشد
                if distance < warning_distance:
                    cv2.putText(frame, 'WARNING: Too close!', (x1, y2 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # نمایش تصویر
    cv2.imshow('Distance Measurement and Warning System', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
