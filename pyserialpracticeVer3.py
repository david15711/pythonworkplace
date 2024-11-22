import time
import serial
from gettext import*
from tkinter import*
from threading import*
import queue






        
class gui(Tk):

    def __init__(self):
        

        self.gui = Tk()
        self.gui.title('UART serial GUI')
        self.gui.geometry("1000x500+100+100")
        self.gui.option_add("font", "맑은고딕 25")
        self.gui.config(bg= 'black')
        self.lab_port = Label(self.gui, text='port', bg= 'black', fg= 'white', width= 8, height= 1)
        self.lab_port.grid(row=0, column=0, padx=10)
        self.ent_port = Entry(self.gui, width=12, bg= 'white', fg= 'black')
        self.ent_port.config(width=12)
        self.ent_port.grid(row=0, column=1, padx= 10)
        self.init_btn = Button(self.gui, text= 'start serial', bg= 'white', fg= 'black', width= 8, height=1)
        self.init_btn.grid(row= 0, column=2, padx= 10)
        self.init_btn.config(command= self.init_serial)
        self.port = self.ent_port.get()
        
        self.transmit_btn = Button(self.gui, text= '송신', width=8, height=1)  
        self.transmit_btn.config(command= self.transmit_serial)
        self.transmit_btn.grid(row=3, column=2, padx=10)
        self.answer_label = Label(self.gui, bg= 'black', fg= 'white', width= 60, height= 30)
        self.answer_label.place(relx=0.2, rely=0.2) 
        
        self.lab_data = Label(self.gui, text='send data', bg= 'black', fg= 'white', width= 8, height= 1)
        self.lab_data.grid(row=3, column=0, padx=10)
        self.ent_data = Entry(self.gui, width=12, bg= 'white', fg= 'black')
        self.ent_data.config(width=12)
        self.ent_data.grid(row=3, column=1, padx=10)
        
        self.queue = queue.Queue()

    def init_serial(self):
        self.thread = Serialthread(self.queue)
        self.thread.start()
        self.process_serial()

    def wait_answer(self):
        if  self.queue.qsize():
            self.response = self.queue.get()
            print(self.response[:len(self.response)-1])
            self.answer_label.config(text= self.response[:len(self.response)-1])
        self.after(10, self.process_serial)

    def process_serial(self):
        while self.queue.qsize():
            try:
                received_data = self.queue.get()
                print("Data received " + str(received_data))
                self.answer_label.config(text= received_data)
            except queue.Empty:
                pass
        self.after(10, self.process_serial)

    #송신 버튼
    def transmit_serial(self):
        data = self.ent_data.get()
        self.thread.py_serial.write(data.encode())
        self.ent_data.delete(0, len(self.ent_data.get()))


class Serialthread(Thread):
    
    py_serial = serial.Serial(port= gui.port, baudrate= 9600,
                                parity=serial.PARITY_NONE,
                                stopbits=serial.STOPBITS_ONE,
                                bytesize=serial.EIGHTBITS)
    
    def __init__(self, que):
        Thread.__init__(self)
        self.queue = que
        
    def run(self):
        if self.py_serial.readable():
            text = self.py_serial.readline()
            self.queue.put(text[:len(text)-1].decode())


app_main = gui()
app_main.mainloop()
