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
from win32api import GetSystemMetrics

monitor_width= GetSystemMetrics(0)*2
monitor_height= GetSystemMetrics(1)*2
left_LED_NUM = 17
top_LED_NUM = 21
right_LED_NUM = 16
default_port = 'COM8'
serial_state = False
thread_state = False
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
        self.queue.put(76)
        self.queue.put(159)
        self.queue.put(132)
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
            while "Screen capturing":
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


# Serial COM
class SerialThread(threading.Thread):

    def __init__(self, que, que2, port):
        global thread_state
        self.queue = que
        self.queue2 = que2
        self.port = port
        if thread_state == True:
            return
        else: 
            threading.Thread.__init__(self)
            thread_state = True

    def run(self):
        global serial_state
        global send_state
        serial_state = True
        send_state = True
        try:
            self.seq = serial.Serial(self.port, baudrate= 115200, parity=serial.PARITY_NONE,
                                        stopbits=serial.STOPBITS_ONE,
                                        bytesize=serial.EIGHTBITS)
        except: 
            serial.SerialException
        self.serial_process()
            
    def serial_process(self):
        while serial_state == True:
            if send_state == True:
                for i in range(0, 55):
                    self.seq.write([self.queue2.get(), self.queue2.get(), self.queue2.get()])
                    if self.seq.inWaiting:
                        self.text = self.seq.readline()
                        self.queue.put(bytes(self.text))
            elif send_state == False: 
                try:
                    for i in range(0, 55):
                        self.seq.write(0, 0, 0,)
                except:
                    pass

    def serial_close(self):
        global serial_state
        try:
            self.seq.close()
            serial_state = False
        except:
            pass

    # def serial_open(self):
    #     global serial_state
    #     try:
    #         self.seq = serial.Serial(self.port, baudrate= 115200, parity=serial.PARITY_NONE,
    #                                     stopbits=serial.STOPBITS_ONE,
    #                                     bytesize=serial.EIGHTBITS)
    #     except: 
    #         serial.SerialException

        
# App Main
class App(Tk):
    global serial_state
    global send_state
    def __init__(self):
        Tk.__init__(self)
        
        #사용 가능 포트 찾기
        # self.find_port = Button(self, text= 'start serial', bg= 'white', fg= 'black', width= 8, height=1, font= "맑은고딕 20", command=self.serial_ports())
        # self.selct_port = OptionMenu(self, )

        # self.searchbluetooth = Button(self, text= 'search bluetooth', bg= '#36393f', fg= 'white', width= 8, height= 1, font= "맑은고딕 20")
        # # # self.searchbluetooth.config(command=)
        # self.searchbluetooth.place(anchor='nw', relx= 0.21, rely=0.62, relwidth=0.18, relheight=0.05)

        # self.check = Checkbutton(self, onvalue=1, offvalue=0)
        # self.check.config(font= "맑은고딕 20", text= 'power on', variable=send_state)
        # self.check.place(anchor='nw', relx=0.41, rely= 0.02)
        # self.tk.call('tk', 'scaling', 2.0)
        #큐 및 쓰레드 시작 구간
        self.queue = queue.Queue()
        self.queue2 = queue.Queue()
        self.thread2 = colorcapture(self.queue2)
        self.thread2.start()
        #창 정의
        self.title('UART serial GUI')
        self.geometry("1000x800+100+100")
        self.option_add("font", "맑은고딕 50")
        self.config(bg= '#101215')
        #포트 입력 구간
        self.lab_port = Label(self, text='port', bg= '#36393f', fg= 'white', width= 8, height= 1, font= "맑은고딕 20")
        self.lab_port.place(anchor='nw', relx=0.01, rely=0.02, relwidth=0.18, relheight=0.05)
        self.ent_port = Entry(self, width=12, bg= 'white', fg= 'black', font= "맑은고딕 20")
        self.ent_port.insert(0, default_port)
        self.ent_port.config(width=12)
        self.ent_port.place(anchor='nw', relx=0.21, rely=0.02, relwidth=0.18, relheight=0.05)

        def connect_serial():
            global serial_state
            global thread_state
            if serial_state == 0:
                if self.thread.is_alive() == 0:
                    self.thread.start()
                # else:
                #     self.thread.serial_open()
                # if self.queue.get() == 'connect failed':
                #     self.answer_label.config(text= 'connect failed')
                #     return()
                # elif :
                self.process_serial()
                self.init_btn.config(text= 'close serial')
                serial_state = 1
            elif serial_state == 1:
                self.thread.serial_close()
                self.init_btn.config(text= 'start serial')
                serial_state = 0

        #시리얼 통신 시작
        self.init_btn = Button(self, text= 'start serial', bg= 'white', fg= 'black', width= 8, height=1, font= "맑은고딕 20")
        self.init_btn.place(anchor='nw', relx=0.81, rely=0.02, relwidth=0.18, relheight=0.05)
        self.init_btn.config(command=connect_serial)
        # 밝기
        self.bright_lab = Label(self, text= 'Brightness', bg= '#36393f', fg= 'white', width= 8, height= 1, font= "맑은고딕 20")
        self.bright_lab.place(anchor='nw', relx=0.01, rely= 0.22, relwidth=0.18, relheight=0.05)
        self.bright_stringvar = StringVar(self)
        self.bright_ent = Entry(self, textvariable= self.bright_stringvar, text='100', width=12, bg= 'white', fg= 'black', font= "맑은고딕 20")
        self.bright_ent.insert(0, '100')
        self.bright_ent.place(anchor='nw', relx=0.21, rely= 0.22, relwidth=0.18, relheight=0.05)
        # 응답 구간
        self.answer_label = Label(self, bg= 'white', fg= 'black', width= 8, height=1, font= "맑은고딕 20")
        self.answer_label.place(relx=0.4, rely=0.5, relwidth= 0.2, relheight= 0.1)
        
        self.thread = SerialThread(self.queue, self.queue2, self.ent_port.get())

    def serial_ports():
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
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

#폴링 구간
    def process_serial(self):
        while self.queue.qsize():
            try:
                received_data = self.queue.get()
                print("Data received : " + str(received_data))
                self.answer_label.config(text= received_data)
            except queue.Empty:
                pass
        time.sleep(1)

app_main = App()
app_main.mainloop()

serial_state = False