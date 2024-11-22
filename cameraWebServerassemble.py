import requests
import numpy as np
import datetime
import re
import os

url = 'http://192.168.43.231'  # 대상 웹 페이지의 URL을 입력하세요.
folder_path = r"C:\\Users\\MS\Desktop\doorlock_picture"

def download_image(url):
    response = requests.get(url)
    image_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")+'.jpg'
    image_name = re.sub(r'[\\/:*?"<>|]', '_', image_name)
    file_path = os.path.join(folder_path, image_name)
    with open(file_path, 'wb') as file:
        file.write(response.content)
    print("이미지를 다운로드했습니다.")

def get_html(url):
    try:
        response = requests.get(url)
        return response.text
    except requests.exceptions.RequestException as e:
        return None
    
last_state = 0

while(1):
    response = requests.get(url)
    html = get_html(url)
    # print(html)
    start_index = html.find('<h3>') + len('<h3>')  # 시작 태그 다음 문자부터 추출합니다.
    end_index = html.find('</h3>', start_index)  # 종료 태그 이전까지 추출합니다.
    capture_bites = html[start_index:end_index]  # "변하는 문자열"을 추출합니다.
    if  (capture_bites != '0') and (last_state != capture_bites):
        last_state = capture_bites
        print(capture_bites)
        download_image('http://192.168.43.231/01')