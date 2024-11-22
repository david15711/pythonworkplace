import queue
import sys
import glob
import threading
import time
from tkinter import *
import bleak
import asyncio
import cv2
import mss
import numpy as np
import serial
import pywinauto
from win32api import GetSystemMetrics

monitor_width= GetSystemMetrics(0)*2
monitor_height= GetSystemMetrics(1)*2
left_LED_NUM = 17
top_LED_NUM = 21
right_LED_NUM = 16
serial_state = False
send_state = False
R = [0 for i in range(33)]
G = [0 for i in range(33)]
B = [0 for i in range(33)]
R[0] = 0
G[0] = 0
B[0] = 0

class colorcapture(threading.Thread):
    def __init__(self, que):
        threading.Thread.__init__(self, daemon= False)
        self.queue = que

    def send_queue(self):
        # 76 = 159 ^ 132 ^ 0x55 (chk = hi ^ lo ^ 0x55)
        self.queue.put(159)
        self.queue.put(132)
        self.queue.put(76)
        for i in range(0, 17, 1):
            left = int(round(9/left_LED_NUM * (i-1), 0))
            self.queue.put(R[left])
            self.queue.put(G[left])
            self.queue.put(B[left])
        for i in range(0, 21, 1):
            top_ = 9 + int(round(14/top_LED_NUM * i, 0))
            self.queue.put(R[top_])
            self.queue.put(G[top_])
            self.queue.put(B[top_])
        for i in range(0, 16, 1):
            right = 24 + int(round(9/right_LED_NUM * i, 0))
            self.queue.put(R[right])
            self.queue.put(G[right])
            self.queue.put(B[right])
    
    def run(self):
        with mss.mss() as Sct:
            while True:
                while send_state == True:
                    #last_time = time.time()
                    for i in range(1,10,1):
                        monitor = {"top": int(monitor_height-monitor_height*0.11111*(i-1)), "left": 0, "width": 10, "height": int(monitor_height/9)}
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
                        monitor = {"top": 0, "left": int(monitor_width*0.07142*(j-10)), "width": int(monitor_width/14), "height": 10}
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
                        monitor = {"top": int(monitor_height*0.11111*(k-24)), "left": monitor_width-10, "width": 10, "height": int(monitor_height/9)}
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
                    self.send_queue()


class SerialThread(threading.Thread):
    def __init__(self, que, que2):
        self.queue = que
        self.queue2 = que2
        self.serial_open = False
        threading.Thread.__init__(self)

    def run(self):
        while True:
            if serial_state == True:
                port = self.queue2.get()
                self.serial_start(port)
            self.serial_process()

    def serial_start(self, port):
        try:
            self.port = port
            self.ser = serial.Serial(self.port, baudrate= 115200, parity=serial.PARITY_NONE,
                                        stopbits=serial.STOPBITS_ONE,
                                        bytesize=serial.EIGHTBITS)
            while not self.ser.inWaiting:
                print('waiting')
                continue
            while self.serial_open == False:
                for i in range(3):
                    text= self.ser.read()
                    print(text)
                    self.ser.write(text)
                self.serial_open = True
            return
        except (OSError, serial.SerialException):
            self.queue2.put('connect failed')
            pass
            
    def serial_process(self):
        while self.serial_open == True:
            print("waiting serial_process")
            time.sleep(1)
            if send_state == True:
                for i in range(0, 55):
                    self.ser.write([self.queue.get(), self.queue.get(), self.queue.get()])
            elif send_state == False:
                self.ser.write(159)
                self.ser.write(132)
                self.ser.write(76)
                for i in range(1, 55):
                    self.ser.write(0)
                    self.ser.write(0)
                    self.ser.write(0)


    def serial_close(self):
        self.serial_open = False
        self.ser.close()
        
        
# App Main
class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.app = pywinauto.application.Application().connect(process= 3360)
        self.dialog = self.app.window()
        #창 정의
        self.title('Ambilight start GUI')
        self.resizable(False, False)
        self.geometry("600x120")
        self.option_add("font", "맑은고딕 18")
        self.config(bg= '#101215')
        #사용 가능 포트 찾기
        self.port_list = self.serial_ports()
        self.port_var = StringVar(self)
        self.port_var.set("Select serial port") 
        self.find_port = Button(self, text= 'find serial', bg= 'white',
                            fg= 'black', width= 8, height=1, font= "맑은고딕 12", command= self.refresh)
        self.find_port.place(anchor='nw', relx=0, rely=0.2, width=300, height=50)
        self.select_port = OptionMenu(self, self.port_var, self.port_list)
        # self.select_port.place(anchor='nw', relx=0.4, rely=0.1, relwidth=0.18, relheight=0.05)
        #시리얼 통신 시작
        self.init_btn = Button(self, text= 'start serial', bg= 'white', fg= 'black', width= 8, height=1, font= "맑은고딕 12")
        self.init_btn.place(anchor='nw', relx=0.5, rely=0.2, width=300, height=50)
        self.init_btn.config(command=self.connect_serial)

        def send_state_change():
            global send_state
            if serial_state == False:
                print("start serial first")
                return
            if send_state == False:
                send_state = True
                self.send_btn.config(text= 'stop send')
            else: 
                send_state = False
                self.send_btn.config(text= 'start')
            
        self.send_btn = Button(self, text= 'start', bg= 'white', fg= 'black', width= 8, height=1, font= "맑은고딕 20")
        # self.send_btn.place(anchor='nw', relx=0.2, rely=0.3, relwidth=0.18, relheight=0.05)
        self.send_btn.config(command= send_state_change)
        # 응답 구간
        self.answer_label = Label(self, bg= 'white', fg= 'black', width= 8, height=1, font= "맑은고딕 20")
        # self.answer_label.place(anchor='nw', relx=0.2, rely=0.2, relwidth=0.18, relheight=0.05)
        
        self.queue = queue.Queue()
        self.queue2 = queue.Queue()
        self.thread = SerialThread(self.queue, self.queue2)
        self.thread.start()
        self.thread2 = colorcapture(self.queue)
        self.thread2.start()
        self.process_serial()

    def connect_serial(self):
        global serial_state
        if serial_state == False:
            port = self.port_var.get()[2:-3]
            print('serial_start')
            serial_state = True
            self.queue2.put(port)
            self.init_btn.config(text= 'close serial')
        elif serial_state == True:
            self.queue2.put('')
            self.init_btn.config(text= 'start serial')
            serial_state = False

    # 포트 찾기
    def serial_ports(self):
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')
        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    def refresh(self):
        self.select_port['menu'].delete(0, 'end')
        self.port_list = []
        self.port_list = self.serial_ports()
        self.port_var.set(self.port_list)

    def process_serial(self):
        while self.queue2.qsize():
            try:
                received_data = self.queue2.get()
                print("Data received : " + str(received_data))
                self.answer_label.config(text= received_data)
            except queue.Empty:
                pass
            self.after(10, self.process_serial)



app_main = App()
app_main.mainloop()

serial_state = False