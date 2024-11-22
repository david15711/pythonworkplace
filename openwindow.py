from gettext import *
from tkinter import*
from datetime import datetime

win = Tk()  #창 생성
win.geometry("1000x500")   #창 크기
win.title("GUI 연습용 창")  #창 이름
win.option_add("*font", "맑은고딕 25")  #글자 폰트와 크기
win.configure(bg = 'white') #창 색

btn = Button(win, text = "현재 시각 확인", width=30)  #버튼 선언
def alert():
    dnow = datetime.now()
    btn.config(text = dnow)
btn.config(command = alert) #버튼 클릭시 실행

btn2 = Button(win, text = '입력창 숫자 확인', width = 30)   #버튼2 선언
def ent_p():
    a = ent.get()
    print(a)
    ent.delete(0, len(ent.get()))    #입력창 비우기 0부터 끝까지
btn2.config(command = ent_p)
ent = Entry(win)    #입력창 선언
ent.config(width=32)





btn.place(relx= 0.2, rely=0)  #버튼 배치
btn2.place(relx=0.2, rely=0.1)
ent.place(relx= 0.2, rely=0.2)  #입력창 배치
win.mainloop()  #창 실행