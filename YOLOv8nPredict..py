from ultralytics import YOLO
import cv2
import torch

model = YOLO("yolov8n.pt")
model.info()

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"모델을 실행할 디바이스 : {device}")

predict_file = input()
results = model.predict(f"{predict_file}", device = device)

for result in results:
    print(result.boxes.xyxy)
    print(result.boxes.conf)
    result_image = result.plot()
    cv2.imshow("YOLOv8n Result", result_image)

cv2.waitKey(0)
cv2.destroyAllWindows()