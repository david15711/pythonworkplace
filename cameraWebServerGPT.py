import requests
from bs4 import BeautifulSoup
import os

# HTML을 가져오는 함수
def get_html(url):
    response = requests.get(url)
    return response.text

# 사진을 다운로드하는 함수
def download_image(url, save_path):
    response = requests.get(url)
    with open(save_path, 'wb') as file:
        file.write(response.content)
    print("사진을 다운로드했습니다.")

# 주소 설정
url = "http://192.168.245.70"
image_url = "http://192.168.245.70/01"

# 마지막으로 읽은 값 초기화
last_value = None
while(1):
    # HTML 가져오기
    html = get_html(url)

    # BeautifulSoup을 사용하여 HTML 파싱
    soup = BeautifulSoup(html, 'html.parser')

    # 두 번째 <h3></h3> 태그 내부의 숫자값 가져오기
    h3_tags = soup.find_all('h3')
    if len(h3_tags) >= 2:
        second_h3_value = h3_tags[1].text
        print("두 번째 <h3> 태그의 값:", second_h3_value)

        # 0이 아니면서 마지막으로 읽은 값과 다른 경우 사진 다운로드
        if second_h3_value != "0" and second_h3_value != last_value:
            # 바탕화면 경로 설정 (윈도우 환경 기준)
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            save_path = os.path.join(desktop_path, "image.jpg")
            download_image(image_url, save_path)
            print("작업이 완료되었습니다.")

        # 마지막으로 읽은 값 업데이트
        last_value = second_h3_value

