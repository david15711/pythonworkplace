import cv2
import numpy as np
import mss
import time

with mss.mss() as Sct:
    #반복
    while "Screen capturing":
        #last_time = time.time()
        for i in range(1,10,1):
            monitor = {"top": 680-70*(i-1), "left": 0, "width": 10, "height": 7}
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
            print(RGB)
            R = RGB[0]
            G = RGB[1]
            B = RGB[2]
            print(R)
            print(G)
            print(B)
            # 켭쳐 보기
            #cv2.imshow("OpenCV/Nump", img)
            #cv2.waitKey(1)
            #cv2.destroyAllWindows()
        for j in range(10,24,1):
            monitor = {"top": 0, "left": 80+80*(j-10), "width": 8, "height": 10}
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
            print(RGB)
            R = RGB[0]
            G = RGB[1]
            B = RGB[2]
            print(R)
            print(G)
            print(B)
            # 켭쳐 보기
            #cv2.imshow("OpenCV/Nump", img)
            #cv2.waitKey(1)
            #cv2.destroyAllWindows()
        for k in range(24,33,1):
            monitor = {"top": 40+70*(k-24), "left": 1200, "width": 10, "height": 7}
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
            print(RGB)
            R = RGB[0]
            G = RGB[1]
            B = RGB[2]
            print(R)
            print(G)
            print(B)
            # 켭쳐 보기
            #cv2.imshow("OpenCV/Nump", img)
            #cv2.waitKey(1)
            #cv2.destroyAllWindows()
        #print(f"fps: {1 / (time.time() - last_time)}")