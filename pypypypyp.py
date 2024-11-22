import cv2
import mss
import numpy as np
from win32api import GetSystemMetrics
import time

monitor_width= GetSystemMetrics(0)*2
monitor_height= GetSystemMetrics(1)*2
R = [0 for i in range(33)]
G = [0 for i in range(33)]
B = [0 for i in range(33)]
R[0] = 0
G[0] = 0
B[0] = 0
left_LED_NUM = 17
top_LED_NUM = 21
right_LED_NUM = 16


with mss.mss() as Sct:
    #반복
    while "Screen capturing":
        #last_time = time.time()
        for i in range(1,10,1):
            monitor = {"top": int(monitor_height-monitor_height*0.11111*(i-1)), "left": 0, "width": int(monitor_width*0.1), "height": int(monitor_height/9)}
            # 스크린 캡쳐 후 numpy.array에 저장
            img = np.array(Sct.grab(monitor))
            #BRG를 RGB로 변경
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            #크기 조정
            height, width, _ = np.shape(img)
            data = np.reshape(img, (-1, 3))
            data = np.float32(data)
            #K-means클러스터링 실행
            number_clusters = 3
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
            flags = cv2.KMEANS_RANDOM_CENTERS
            compactness, labels, centers = cv2.kmeans(data, number_clusters, None, criteria, 10, flags)
            #RGB값 추출
            RGB = centers[0].astype(np.int32)
            # print(RGB)
            R[i] = RGB[0]
            G[i] = RGB[1]
            B[i] = RGB[2]
            # print(R)
            # print(G)
            # print(B)
            # 켭쳐 보기
            #cv2.imshow("OpenCV/Nump", img)
            #cv2.waitKey(1)
            #cv2.destroyAllWindows()
        for j in range(10,24,1):
            monitor = {"top": 0, "left": int(monitor_width*0.07142*(j-10)), "width": int(monitor_width/14), "height": int(monitor_height*0.1)}
            # 스크린 캡쳐 후 numpy.array에 저장
            img = np.array(Sct.grab(monitor))
            #BRG를 RGB로 변경
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            #크기 조정
            height, width, _ = np.shape(img)
            data = np.reshape(img, (-1, 3))
            data = np.float32(data)
            #K-means클러스터링 실행
            number_clusters = 3
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
            flags = cv2.KMEANS_RANDOM_CENTERS
            compactness, labels, centers = cv2.kmeans(data, number_clusters, None, criteria, 10, flags)
            #RGB값 추출
            RGB = centers[0].astype(np.int32)
            # print(RGB)
            R[j] = RGB[0]
            G[j] = RGB[1]
            B[j] = RGB[2]
            # print(R)
            # print(G)
            # print(B)
            # 켭쳐 보기
            #cv2.imshow("OpenCV/Nump", img)
            #cv2.waitKey(1)
            #cv2.destroyAllWindows()
        for k in range(24,33,1):
            monitor = {"top": int(monitor_height*0.11111*(k-24)), "left": int(monitor_width-10), "width": int(monitor_width*0.1), "height": int(monitor_height/9)}
            # 스크린 캡쳐 후 numpy.array에 저장
            img = np.array(Sct.grab(monitor))
            #BRG를 RGB로 변경
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            #크기 조정
            height, width, _ = np.shape(img)
            data = np.reshape(img, (-1, 3))
            data = np.float32(data)
            #K-means클러스터링 실행
            number_clusters = 3
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
            flags = cv2.KMEANS_RANDOM_CENTERS
            compactness, labels, centers = cv2.kmeans(data, number_clusters, None, criteria, 10, flags)
            #RGB값 추출
            RGB = centers[0].astype(np.int32)
            # print(RGB)
            R[k] = RGB[0]
            G[k] = RGB[1]
            B[k] = RGB[2]
            # print(R)
            # print(G)
            # print(B)
            # 켭쳐 보기
            #cv2.imshow("OpenCV/Nump", img)
            #cv2.waitKey(1)
            #cv2.destroyAllWindows()
            #print(f"fps: {1 / (time.time() - last_time)}")
            
            
        for i in range(0, 17, 1):
            left = int(round(9/left_LED_NUM * (i-1), 0))
            print('왼쪽 원본 배열 {0}, LED 왼쪽에서 {1}, LED 전체 {2}'.format(left, i, i+0))
            print(R[left])
            print(G[left])
            print(B[left])
            time.sleep(0.3)
        for i in range(0, 21, 1):
            top_ = 9 + int(round(14/top_LED_NUM * i, 0))
            print('위쪽 원본 배열 {0}, LED 위에서 {1}, LED 전체 {2}'.format(top_, i, i+17))
            print(R[top_])
            print(G[top_])
            print(B[top_])
            time.sleep(0.3)
        for i in range(0, 16, 1):
            right = 24 + int(round(9/right_LED_NUM * i, 0))
            print('오른쪽 원본 배열 {0}, LED 오른쪽에서 {1}, LED 전체 {2}'.format(right, i, i+38))
            print(R[right])
            print(G[right])
            print(B[right])
            time.sleep(0.3)
