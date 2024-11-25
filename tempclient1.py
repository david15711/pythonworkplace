import sseclient
import requests
import base64
import cv2
import numpy as np
import csv
from ultralytics import YOLO  # YOLOv8 라이브러리

# ESP32 서버 URL
ESP32_URL = "http://<ESP32_IP_ADDRESS>/events"

# YOLOv8 모델 로드
model = YOLO("yolov8n.pt")  # YOLOv8 모델

# CSV 파일 초기화
csv_file = open("data_log.csv", "w", newline="")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["x", "y", "z", "facing", "class", "count"])

# SSE 이벤트 수신
response = requests.get(ESP32_URL, stream=True)
client = sseclient.SSEClient(response)

for event in client.events():
    data = json.loads(event.data)
    x, y, z, facing = data["x"], data["y"], data["z"], data["facing"]
    image_data = base64.b64decode(data["image"].split(",")[1])
    
    # 이미지를 디코딩
    nparr = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # YOLO 추론
    results = model(image)
    class_counts = {}
    for r in results[0].boxes:
        cls = int(r.cls)
        class_counts[cls] = class_counts.get(cls, 0) + 1
    
    # CSV 저장
    for cls, count in class_counts.items():
        csv_writer.writerow([x, y, z, facing, cls, count])
    
    # 결과 출력
    print(f"x: {x}, y: {y}, z: {z}, facing: {facing}, classes: {class_counts}")
csv_file.close()
