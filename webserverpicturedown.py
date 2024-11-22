import requests
from PIL import Image
import time

url = "http://192.168.0.30/capture?_cb"
last_modified = None

# 사진 다운로드 함수
def download_picture():
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        new_modified = response.headers.get("Last-Modified")
        if new_modified != last_modified:
            with open("captured_picture.jpg", "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            last_modified = new_modified
            print("새로운 사진이 다운로드되었습니다.")
    except requests.exceptions.RequestException as e:
        print("사진 다운로드 중 오류가 발생했습니다:", e)

# 메인 함수
def main():
    while True:
        download_picture()
        time.sleep(1)  # 1초마다 사진 업데이트 확인

# 실행
if __name__ == "__main__":
    main()
