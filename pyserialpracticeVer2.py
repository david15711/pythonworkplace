import time
import serial
from tkinter import*
from gettext import*
import threading
from win32api import GetSystemMetrics

print("Width =", GetSystemMetrics(0)*2)
print("Height =", GetSystemMetrics(1)*2)

global py_serial
default_port = 'COM7'
default_baud = '115200'
serial_state = 0
#창 정의
gui = Tk()
gui.title('UART serial GUI')
gui.geometry("700x500+100+100")
gui.option_add("font", "맑은고딕 25")
gui.config(bg= '#101215')
#포트 입력 구간
lab_port = Label(gui, text='port', bg= '#36393f', fg= 'white', width= 8, height= 1)
lab_port.place(anchor='nw', relx=0.01, rely=0.02, relwidth=0.18, relheight=0.05)
ent_port = Entry(gui, width=12, bg= 'white', fg= 'black')
ent_port.insert(0, default_port)
ent_port.config(width=12)
ent_port.place(anchor='nw', relx=0.21, rely=0.02, relwidth=0.18, relheight=0.05)
#보율 입력 구간
lab_baud = Label(gui, text='baud rate', bg= '#36393f', fg= 'white', width= 8, height= 1)
lab_baud.place(anchor='nw', relx=0.41, rely=0.02, relwidth=0.18, relheight=0.05)
ent_baud = Entry(gui, width=12, bg= 'white', fg= 'black')
ent_baud.insert(0, default_baud)
ent_baud.config(width=12)
ent_baud.place(anchor='nw', relx=0.61, rely=0.02, relwidth=0.18, relheight=0.05)
#
def connect_serial():
    global py_serial
    global serial_state
    if serial_state == 0:
        py_serial = serial.Serial(port= ent_port.get(), baudrate= ent_baud.get(),
                                parity=serial.PARITY_NONE,
                                stopbits=serial.STOPBITS_ONE,
                                bytesize=serial.EIGHTBITS)
        init_btn['text']= 'close serial'
        serial_state = 1
        return()
    elif serial_state == 1:
        py_serial.close()
        init_btn['text']= 'start serial'
        serial_state = 0
        return()

#시리얼 통신 시작
init_btn = Button(gui, text= 'start serial', bg= 'white', fg= 'black', width= 8, height=1)
init_btn.place(anchor='nw', relx=0.81, rely=0.02, relwidth=0.18, relheight=0.05)
init_btn.config(command=connect_serial)

#데이터 보내기 구간
lab_data = Label(gui, text='send data', bg= '#36393f', fg= 'white', width= 8, height= 1)
lab_data.place(anchor='nw', relx=0.01, rely=0.12, relwidth=0.18, relheight=0.05)
ent_data = Entry(gui, width=12, bg= 'white', fg= 'black')
ent_data.config(width=12)
ent_data.place(anchor='nw', relx=0.21, rely=0.12, relwidth=0.18, relheight=0.05)

def wait_answer():
    global py_serial
    if py_serial.readable():
        response = py_serial.readline()
        print(response[:len(response)-1].decode())
        answer_label.config(text= response[:len(response)-1].decode())

#송신 버튼
transmit_btn = Button(gui, text= '송신', width=8, height=1)
def transmit_serial():
    global py_serial
    if serial_state == 0:
        answer_label['text'] = "connect serial first...\n"     
        ent_data.delete(0, len(ent_data.get())) 
        return()      
    if ent_data.get() == '':
        ent_data.insert(0, ' \n')
        wait_answer
    a = ent_data.get()
    py_serial.write(a.encode())
    ent_data.delete(0, len(ent_data.get()))   #입력창 비우기 0부터 끝까지
    wait_answer()
    return()
transmit_btn.config(command= transmit_serial)
transmit_btn.place(anchor='nw', relx=0.41, rely=0.12, relwidth=0.18, relheight=0.05)
answer_label = Label(gui, bg= 'black', fg= 'white')
answer_label.place(relx=0.4, rely=0.5, relwidth= 0.2, relheight= 0.1)

# 창 시작
gui.mainloop()
py_serial.close()
serial_state = False

#필요 기능
#지속적 시리얼 read or write (클래스, 쓰레드 폴링 이용)
#블루투스 시리얼 기능, 해상도 자동 인식, RGB send 알고리즘
