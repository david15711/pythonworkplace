import sys
import serial
import threading
import queue
from tkinter import*
import time
import cv2
import numpy as np
import mss

NUM_LEDS = 32
default_port = 'COM7'
default_baud = 115200
serial_state = False
# red = random.randrange(0, 255)
# green = random.randrange(0, 255)
# blue = random.randrange(0, 255)
# Serial COM
class SerialThread(threading.Thread):
    # seq = serial.Serial('COM7', 115200, timeout=1)  # MS-Windows
    # is_run = True

    def __init__(self, que, que2):
        threading.Thread.__init__(self)
        self.queue = que
        self.queue2 = que2
        # self.port = port
        # self.baud = baud
        
    def run(self):
        seq = serial.Serial('COM3', 115200, parity=serial.PARITY_NONE,
                                        stopbits=serial.STOPBITS_ONE,
                                        bytesize=serial.EIGHTBITS)
        serial_state = True
        while serial_state == True:
            for i in range(0, NUM_LEDS):
                seq.write([self.queue2.get(), self.queue2.get(), self.queue2.get(), 0x00])
                seq.write([0x0b, 0x0a])
                time.sleep(0.5)
                if seq.readable():
                    text = seq.readline()
                    self.queue.put(bytes(text))
                    # print(bytes([red]))
                    # print(bytes([green]))
                    # print(bytes([blue]))




class colorcapture(threading.Thread):

    def __init__(self, que):
        threading.Thread.__init__(self)
        self.queue = que

    def run(self):
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
                    # print(RGB)
                    R = RGB[0]
                    G = RGB[1]
                    B = RGB[2]
                    self.queue.put(R)
                    self.queue.put(G)
                    self.queue.put(B)
                    # print(R)
                    # print(G)
                    # print(B)
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
                    # print(RGB)
                    R = RGB[0]
                    G = RGB[1]
                    B = RGB[2]
                    self.queue.put(R)
                    self.queue.put(G)
                    self.queue.put(B)
                    # print(R)
                    # print(G)
                    # print(B)
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
                    # print(RGB)
                    R = RGB[0]
                    G = RGB[1]
                    B = RGB[2]
                    self.queue.put(R)
                    self.queue.put(G)
                    self.queue.put(B)
                    # print(R)
                    # print(G)
                    # print(B)
                    # 켭쳐 보기
                    #cv2.imshow("OpenCV/Nump", img)
                    #cv2.waitKey(1)
                    #cv2.destroyAllWindows()
                    #print(f"fps: {1 / (time.time() - last_time)}")

# App Main
class App(Tk):
    '''
    Application Main
    '''
    def __init__(self):
        Tk.__init__(self)

        # Move center
        self.win_w = self.winfo_reqwidth()
        self.win_h = self.winfo_reqheight()
        self.screen_w = self.winfo_screenwidth()
        self.screen_h = self.winfo_screenheight()
        self.loc_x = (self.screen_w/2) - (self.win_w/2)
        self.loc_y = (self.screen_h/2) - (self.win_h/2)
        self.geometry('+%d+%d' % (self.loc_x, self.loc_y))

        self.svar = ""

        self.rlabel = Label(self, text="Received:")
        self.rlabel.grid(row=0, column=0)

        # self.rdata = tk.Entry(self, textvariable=self.svar)   # Text input field
        self.rdata = Label(self, text=self.svar) # Label
        self.rdata.grid(row=0, column=1)

        self.slabel = Label(self, text="Send:")
        self.slabel.grid(row=1, column=0)

        self.sdata = Entry(self)
        self.sdata.grid(row=1, column=1)

        self.btn_send = Button(self, text="Send", width=15, command=self.on_send)
        self.btn_send.grid(row=2, column=1)

        self.queue = queue.Queue()
        self.queue2 = queue.Queue()
        self.thread2 = colorcapture(self.queue2)
        self.thread2.start()
        self.thread = SerialThread(self.queue, self.queue2)
        self.thread.start()
        self.process_serial()

    def on_send(self):
        '''
        Send data via serial port
        '''
        data = self.sdata.get()
        # print(data + " Send Clicked")
        SerialThread.seq.write(data)
        # self.ser.close()
        self.sdata.delete(0, len(self.sdata.get()))
#폴링 구간
    def process_serial(self):
        '''
        Receive data via serial port
        '''
        while self.queue.qsize():
            try:
                received_data = self.queue.get()
                print("Data received : ")
                print(received_data)

                # In case, Text input field
                # self.rdata.delete(0, 'end')
                # self.rdata.insert('end', self.queue.get())

                # In case, Label
                self.rdata.config(text=received_data)
            except queue.Empty:
                pass
        self.after(10, self.process_serial)

app_main = App()
app_main.mainloop()

serial_state = False