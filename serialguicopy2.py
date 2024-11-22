import serial
import tkinter as tk
from tkinter import ttk
import time
import threading




class Application(tk.Tk):
    rel_entrywidth_y= 0.02
    baud_rate_list = [1200, 1800, 2400, 4800, 7200, 9600, 14400, 19200, 115200]
    HEIGHT = 650
    WIDTH = 750
    
    def __init__(self):
        super().__init__()
        self.title("SERIAL COMMUNICATION")
        self.default_com = 'COM13'
        self.connect_state = "Not Connected"
        self.data = []
        self.temp = []
        self.createWidgets()


    def createWidgets(self):
        self.canvas = tk.Canvas(self, width=self.WIDTH, height=self.HEIGHT, bg='#adadad')
        self.canvas.pack()
        
        self.port_label = tk.Label(self.canvas, text="Select Port:", font="Courier 12", bg = '#adadad')
        self.port_label.place(anchor='nw', relx=0.01, rely=self.rel_entrywidth_y, relwidth=0.18, relheight=0.05)

        self.port_entry = tk.Entry(self.canvas, text='COM1', font="Courier 12", bg='#A6CCF0', justify='center')
        self.port_entry.insert(0, self.default_com)
        self.port_entry.place(anchor='nw', relx=0.21, rely=self.rel_entrywidth_y, relwidth=0.18, relheight=0.05)

        self.baud_rate_var = tk.StringVar(self.canvas)
        self.baud_rate_var.set(self.baud_rate_list[5])           # set default baud rate

        self.baud_label = tk.Label(self.canvas, text="  Baud Rate:", font="Courier 12", bg = '#adadad')
        self.baud_label.place(anchor='nw', relx=0.4, rely=self.rel_entrywidth_y, relwidth=0.18, relheight=0.05)

        self.baud_menu = tk.OptionMenu(self, self.baud_rate_var, *self.baud_rate_list)
        self.baud_menu.config(font='Courier 12', bg='#A6CCF0')
        self.baud_menu.place(anchor='nw', relx=0.6, rely=self.rel_entrywidth_y, relwidth=0.18, relheight=0.05)

        self.connect_button = tk.Button(self.canvas, text='Connect', font='Courier 12 bold', command=self.connect_func)
        self.connect_button.place(anchor='nw', relx=0.815, rely=self.rel_entrywidth_y, relwidth=0.15, relheight=0.05)

        self.canvas.create_line(0, 60, self.WIDTH, 60, width=1)

        #self.canvas.create_line(0, 570, WIDTH, 570, width=1)

        #self.separator1 = ttk.Separator(self.canvas, orient='horizontal', bg='#adadad')
        #self.separator1.place(relx=0, rely=0.5, relwidth=1, relheight=0.5)


        self.comm_text = tk.Text(self, width=40, height=10, font='Courier 12', state='disabled')
        self.comm_text.place(anchor='n', relx=0.63, rely=0.1, relwidth=0.7, relheight=0.75)
        self.comm_vsb = tk.Scrollbar(self, orient='vertical', command=self.comm_text.yview)
        self.comm_vsb.place(anchor='n', relx=0.985, rely=0.101, relwidth=0.03, relheight=0.749)

        self.send_button = tk.Button(self.canvas, text='Send', font='Courier 12 bold', command=threading.Thread(target=self.send_data).start())
        self.send_button.place(anchor='n', relx=0.9, rely=0.89, relwidth=0.15, relheight=0.07)
        
        self.data_entry = tk.Entry(self.canvas, font="Courier 14", bg='#d1d1d1', justify='left')
        self.data_entry.place(anchor='n', relx=0.41, rely=0.875, relwidth=0.8, relheight=0.1)

        
        # self.img = tk.PhotoImage(file='serial.png')
        # self.img = self.img.subsample(9)
        # self.canvas.create_image(50, 500, anchor='nw', image=self.img)




    def connect_func(self):
        if self.connect_state == "Not Connected":
            self.com_port = self.port_entry.get()
            self.baud_rate = self.baud_rate_var.get()
            self.connect_button['text'] = "Close"
            self.update_idletasks()               # making sure it changes to "Close"
            print("COM PORT IS : ", self.com_port)
            print("BAUD RATE IS : ", self.baud_rate)
            try:
                self.ser = serial.Serial(self.com_port, self.baud_rate)
                self.connect_state = "Connected"
                print("Connected to", self.com_port, "successfully!")
                self.after(500, threading.Thread(target=self.receive_data()).start())
    
            except Exception as e:
                print("Error connecting to port ", self.com_port, " ... ", e)
                self.connect_button['text'] = "Connect"
                self.connect_state = "Not Connected"
                


        elif self.connect_state == "Connected":
            self.ser.close()
            print("Closing serial connection with port", self.com_port)
            self.connect_button['text'] = "Connect"
            self.connect_state = "Not Connected"
  



    def send_data(self):
        if self.connect_state == "Connected":
            self.send_data = self.data_entry.get()
            self.ser.write(self.send_data.encode())
            print("SENDING... : " + self.send_data)
            self.data.append(self.send_data)
            self.refresh_comms(self.send_data)
        else:
            print("Connect to a serial port first...")



    def refresh_comms(self, d):
        #print("temp : ", self.temp)
        #print("data : ", d)
        if len(self.temp) < len(d):             # if data has been added
            self.comm_text.configure(state='normal')
            self.comm_text.insert('end', d[len(d)-1] + '\n')
            self.comm_text.see('end')                     # scroll text
            self.comm_text.configure(state='disabled')
            self.update_idletasks()
            self.temp.append(d[len(d)-1]) 
        
        self.update_idletasks()
        self.after(500, self.receive_data)




    def receive_data(self):
        if self.ser.in_waiting:
            received = self.ser.readline().decode()
            self.data.append(str(self.com_port) + ' : ' + received)
            print("I received :", received)
        
        self.update_idletasks()
        self.after(500, self.refresh_comms(self.data))





app = Application()
app.resizable(False, False)

app.mainloop()