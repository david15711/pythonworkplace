import serial
import time
from gettext import*
from tkinter import*

py_serial = serial.Serial(port= 'COM5',
                        baudrate= 9600,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS)


win = Tk()  #창 생성
win.geometry("1000x500")   #창 크기
win.title("atmega128 시리얼 통신")  #창 이름
win.option_add("*font", "맑은고딕 25")  #글자 폰트와 크기
win.configure(bg = 'white') #창 색

ent = Entry(win)    #입력창 선언
ent.config(width=32)
ent.pack(pady=10)

btn = Button(win, text= '송신', width=10, height=10)
def ent_p():
    a = ent.get()
    py_serial.write(a.encode())
    ent.delete(0, len(ent.get()))    #입력창 비우기 0부터 끝까지
btn.config(command= ent_p)
btn.pack(side=RIGHT)

label = Label(win, width= 30, height=10)
label.config(text= py_serial.readline()[:len(py_serial.readline())-1].decode())
label.pack(pady=10)

while True:

    command= input('atmega128에게 내릴 명령: ')
    py_serial.write(command.encode())

    time.sleep(1)

    if py_serial.readable():
        response = py_serial.readline()
        print(response[:len(response)-1].decode())