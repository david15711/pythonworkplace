import serial
import tkinter
import threading
import time
import queue

class Serialthread(threading.Thread):
    def __init__(self, queue, serial):
        threading.Thread.__init__()
        self.ser = serial
        self.queue = queue

    def run(self):
        while App.connect_state:
            if self.ser.readable():
                text = self.ser.readline()
                self.queue.put(text[:len(text)-1].decode())


class App(tkinter.Tk):
    
    rel_entrywidth_y= 0.02
    baud_rate_list = [1200, 1800, 2400, 4800, 7200, 9600, 14400, 19200]
    HEIGHT = 650
    WIDTH = 750
    default_port = 'COM5'
    connect_state = 'NOPE'

    def __init__(self):
        self.thread = Serialthread()
        
        tkinter.Tk.__init__(self)
        self.canvas = tkinter.Canvas(self, width=self.WIDTH, height=self.HEIGHT, bg='#adadad')
        self.canvas.pack()
        
        self.port_label = tkinter.Label(self.canvas, text="Select Port:", font="Courier 12", bg = '#adadad')
        self.port_label.place(anchor='nw', relx=0.01, rely=self.rel_entrywidth_y, relwidth=0.18, relheight=0.05)

        self.port_entry = tkinter.Entry(self.canvas, text='COM1', font="Courier 12", bg='#A6CCF0', justify='center')
        self.port_entry.insert(0, self.default_port)
        self.port_entry.place(anchor='nw', relx=0.21, rely=self.rel_entrywidth_y, relwidth=0.18, relheight=0.05)

        self.baud_rate_var = tkinter.StringVar(self.canvas)
        self.baud_rate_var.set(self.baud_rate_list[5])           # set default baud rate

        self.baud_label = tkinter.Label(self.canvas, text="  Baud Rate:", font="Courier 12", bg = '#adadad')
        self.baud_label.place(anchor='nw', relx=0.4, rely=self.rel_entrywidth_y, relwidth=0.18, relheight=0.05)

        self.baud_menu = tkinter.OptionMenu(self, self.baud_rate_var, *self.baud_rate_list)
        self.baud_menu.config(font='Courier 12', bg='#A6CCF0')
        self.baud_menu.place(anchor='nw', relx=0.6, rely=self.rel_entrywidth_y, relwidth=0.18, relheight=0.05)

        self.connect_button = tkinter.Button(self.canvas, text='Connect', font='Courier 12 bold', command=self.connect_func)
        self.connect_button.place(anchor='nw', relx=0.815, rely=self.rel_entrywidth_y, relwidth=0.15, relheight=0.05)

        self.canvas.create_line(0, 60, self.WIDTH, 60, width=1)

        #self.separator1 = ttk.Separator(self.canvas, orient='horizontal', bg='#adadad')
        #self.separator1.place(relx=0, rely=0.5, relwidth=1, relheight=0.5)


        self.comm_text = tkinter.Text(self, width=40, height=10, font='Courier 12', state='disabled')
        self.comm_text.place(anchor='n', relx=0.63, rely=0.1, relwidth=0.7, relheight=0.75)
        self.comm_vsb = tkinter.Scrollbar(self, orient='vertical', command=self.comm_text.yview)
        self.comm_vsb.place(anchor='n', relx=0.985, rely=0.101, relwidth=0.03, relheight=0.749)

        self.send_button = tkinter.Button(self.canvas, text='Send', font='Courier 12 bold', command=threading.Thread(target=self.send_data).start())
        self.send_button.place(anchor='n', relx=0.9, rely=0.89, relwidth=0.15, relheight=0.07)
        
        self.data_entry = tkinter.Entry(self.canvas, font="Courier 14", bg='#d1d1d1', justify='left')
        self.data_entry.place(anchor='n', relx=0.41, rely=0.875, relwidth=0.8, relheight=0.1)

        self.queue = queue.Queue()


    def connect_func(self):
        if  self.connect_state == "NOPE":
            self.com_port = self.port_entry.get()               
            self.baud_rate = self.baud_rate_var.get()
            self.connect_button['text'] = "Close"    
            print("COM PORT IS : ", self.com_port)
            print("BAUD RATE IS : ", self.baud_rate) 
            self.serial = serial.Serial(port = self.com_port, baud = self.baud_rate, parity=serial.PARITY_NONE,
                                stopbits=serial.STOPBITS_ONE,
                                bytesize=serial.EIGHTBITS)
            self.thread = Serialthread(self.queue, self.serial)
            self.thread.start()
            self.process_serial()

        elif self.connect_state == "Connected":
            self.serial.close()
            print("Closing serial connection with port" + str(self.com_port))
            self.connect_button['text'] = "Connect"
            self.connect_state = "NOPE"

    def process_serial(self):
        while self.queue.qsize():
            try:
                received_data = self.queue.get()
                print("Data received " + str(received_data))
                self.comm_text.config(text= received_data)
            except queue.Empty:
                pass
        self.after(10, self.process_serial)

    #송신 버튼
    def transmit_serial(self):
        data = self.data_entry.get()
        Serialthread.ser.write(data.encode())
        self.data_entry.delete(0, len(self.data_entry.get()))


