#!/usr/bin/env python3
# -*-coding:utf-8-*

import threading
from selenium import webdriver
from tkinter import *
import tkinter as tk
from system.lck.GetingData import GetingData
from system.lck.OpenView import OpenView
from system.lck.TrainingModel import TrainingModel

class myUI(Frame):

    def __init__(self):
        self.root = Tk()
        var1 = StringVar()
        var2 = StringVar()
        self.root.title("QQ动态分析")
        self.root.geometry("1258x743")

        # 添加QQ背景图片
        bg = tk.Canvas(self.root, width=1258, height=743, bg='white')
        self.img = PhotoImage(file="./image/backgroud.png")
        bg.place(x=0, y=0)
        bg.create_image(0, 0, anchor=NW, image=self.img)

        login = Button(self.root, width=80, height=2, text="获取信息", bg='#FFD0FF', bd=5,
                       font="bold", command=gettingData)
        login.place(x=170, y=60)
        login = Button(self.root, width=80, height=2, text="情感分析结果", bg='#FFD0FF',
                       bd=5, font="bold", command=trainModel)
        login.place(x=170, y=280)
        login = Button(self.root, width=80, height=2, text="天气结合情感分析情况", bg='#FFD0FF',
                       bd=5, font="bold", command=openView)
        login.place(x=170, y=500)

        self.root.resizable(False, False)
        self.root.attributes("-alpha", 0.98)

def gettingData():
    # 提供正确的QQ空间账号和密码完成用户信息的获取工作,
    # 因为工作效率问题验证码的验证工作环节暂时还是由人工代替，就是验证码需要认为的去进行验证
    threading.Thread(target=GetingData, args=('1968795781', '15225794256liu')).start()
    print("开始爬取好友信息")
def trainModel():
    threading.Thread(target=TrainingModel, args=()).start()
    # TrainingModel()
    print("开始预测心情")
    driver = webdriver.Chrome()
    # 可视化页面的地址
    url = 'E:/Pycharm_xjf/ShangHai_Porject/wait.html'
    driver.get(url)
    driver.maximize_window()
    driver.close()
    driver.quit()
t = None
def openView():
    t = threading.Thread(target=OpenView, args=())
    t.start()
    print("开始显示天气情况")

def main():
    ui = myUI()
    ui.root.mainloop()
    if t is not None:
        t.join()
if __name__=="__main__":
    main()










