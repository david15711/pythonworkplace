import os
import csv
import json
import sseclient
import requests
from ultralytics import YOLO
from PIL import Image
from io import BytesIO
import time
import shutil

url = "http://192.168.9.70"
result_path = r".\result"
csv_file = os.path.join(result_path, "result.csv")

model = YOLO("./best.pt")
model.info()

def append_to_csv(data):
    csv_file = os.path.join(result_path, "result.csv")
    file_exists = os.path.isfile(csv_file)
    header = ["x", "y", "z", "facing", "count"]
    with open(csv_file, mode="a", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=header)
        if not file_exists:
            writer.writeheader(header)
        writer.writerow(data)

def download_image():
    response = requests.get(url + "/image", stream=True)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        print("Failed to download image.")
        return None
        
def process_image(image, data):
    results = model.predict(image, conf=0.65)
    data['x'] = round(data['x'])
    data['y'] = round(data['y'])
    data['z'] = round(data['z'])
    results[0].plot(show=True, save=True, labels=True, filename= f"{data['x']}-{data['y']}-{data['z']}-{data['facing']}.jpg")
    class1_count = sum(1 for obj in results[0].boxes.cls if obj == 0)
    print("Boxes count: ", class1_count)

    shutil.move(f"{data['x']}-{data['y']}-{data['z']}-{data['facing']}.jpg", os.path.join(result_path, f"{data['x']}-{data['y']}-{data['z']}-{data['facing']}.jpg") )
    csv_data = {
        "x": data["x"],
        "y": data["y"],
        "z": data["z"],
        "facing": data["facing"],
        "count": class1_count,
    }
    append_to_csv(csv_data)

def check_connection():
    response = requests.get(url + "/check")
    if response.status_code == 200:
        print("Response from server: ", response.text)
        return True
    else: 
        return False


def listen_for_sse():
    print("Listening for SSE events...")
    try:        
        client = sseclient.SSEClient(url + "/events")
        for event in client:
            if event.data:
                try:
                    data = json.loads(event.data)  # SSE 데이터를 JSON으로 파싱
                    print(f"Image ready with data: {data}")
                    time.sleep(1)
                    image = download_image()
                    if image:
                        process_image(image, data)
                except json.JSONDecodeError:
                    print("Failed to decode SSE data.")
            
    except requests.exceptions.RequestException as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    if not os.path.exists(result_path):
        os.makedirs(result_path, exist_ok=True)

    print(csv_file)
    while not check_connection():
        time.sleep(1)
    while True:
        listen_for_sse()
        time.sleep(1)

