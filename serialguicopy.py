import sys
import serial
import threading
import queue
from tkinter import*

# Serial COM
class SerialThread(threading.Thread):
    '''
    Control RS-xxx Ports
    '''
    seq = serial.Serial('COM4', 115200, timeout=1)  # MS-Windows
    is_run = True

    def __init__(self, que):
        threading.Thread.__init__(self)
        self.queue = que
        
    def run(self):
        while self.is_run:
            if self.seq.readable():
                text = self.seq.readline()
                self.queue.put(text[:len(text)-1].decode())

# App Main
class App(Tk):
    '''
    Application Main
    '''
    def __init__(self,):
        Tk.__init__(self)

        # Really Full screen (No title bar)
        # self.attributes('-fullscreen', True)

        # Maximize (Exist title bar)
        # self.win_w, self.win_h = self.winfo_screenwidth(), self.winfo_screenheight()
        # self.geometry("%dx%d+0+0" % (self.win_w, self.win_h))

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
        self.thread = SerialThread(self.queue)
        self.thread.start()
        self.process_serial()

    def on_send(self):
        '''
        Send data via serial port
        '''
        data = self.sdata.get()
        # print(data + " Send Clicked")
        SerialThread.seq.write(data.encode())
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
                print("Data received : " + str(received_data))

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

SerialThread.is_run = False