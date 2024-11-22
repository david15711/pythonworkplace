import cv2
import PIL.Image, PIL.ImageTk
from tkinter import *
import numpy as np
from urllib.request import urlopen


class App:
    def __init__(self, window):
        self.width, self.height = 640,480
        self.window = window
        self.window.geometry("640x480")
        self.window.title("Read ESP32-CAM")
        self.buffer = b''
        url = "http://192.168.245.70" #Your url
        self.stream = urlopen(url)

        self.canvas = Canvas(window, width = self.width, height = self.height)
        self.canvas.pack()
        self.delay = 1
        self.update()
        self.window.mainloop()

    def update(self):
        while True:            
            self.buffer += self.stream.read(2560)
            head = self.buffer.find(b'\xff\xd8')
            end = self.buffer.find(b'\xff\xd9')
            try:
                if head > -1 and end > -1:
                    jpg = self.buffer[head:end+2]
                    self.buffer = self.buffer[end+2:]
                    frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
                    self.canvas.create_image(0, 0, image = self.photo, anchor = NW)
                    break
            except:
                pass

        self.window.after(self.delay, self.update)

App(Tk())