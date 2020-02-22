# เขียนให้getหน้าได้ต่างๆได้ และ สามารถเอาหน้าที่getไเ้ ไปทำบางอย่างได้
# เขียนให้มันdetectหน้าสีได้

import tkinter
from tkinter import Tk
from win32com.client.dynamic import Dispatch
import time
import threading
import multiprocessing
import pythoncom
import sys
from tkinter import ttk

class Acrobat:
    def __init__(self):
        self.app = Dispatch("AcroExch.app")
    def cur_page(self):
        return self.app.GetActiveDoc().GetAVPageView().GetPageNum()
    def numPages(self):
        return self.app.GetActiveDoc().GetPDDoc().GetNumPages()
    def GoToPage(self, To):
        self.app.GetActiveDoc().GetAVPageView().GoTo(To)

class Action:
    list_page = []
    not_page = []
    def __init__(self):
        self.acrobat = Acrobat()
        [self.not_page.append(i) for i in range(1,self.acrobat.numPages()+1)]
        #print(self.not_page)

    def close2(self, num, list_page):
        for i in range(len(list_page)):
            if num in list_page:
                if list_page[i] == num:
                    return [i-1, i+1]
            else:
                if self.list_page[i] < num and self.list_page[i+1] > num:
                    return [i, i+1]
    def next_list(self, event=""):
        #curPage = app.GetActiveDoc().GetAVPageView().GetPageNum()
        #app.GetActiveDoc().GetAVPageView().GoTo(curPage-1)
        cur = self.acrobat.cur_page()+1
        try:
            toPage = self.close2(cur, self.list_page)
        except:
            toPage = [0, -1]
        if toPage[1] == len(self.list_page):
            toPage[1] = 0
        self.acrobat.GoToPage(self.list_page[toPage[1]]-1)
        self.root.event_generate("<<changePage>>")
    def next_page(self, event=""):
        #app.GetActiveDoc().GetAVPageView().GoTo(self.acrobat.cur_page+1)
        self.acrobat.GoToPage(self.acrobat.cur_page()+1)
        self.root.event_generate("<<changePage>>")
    def listToStrFormat(self, inList=[]):
        if len(inList) == 0:
            return ""
        start = inList[0]
        end = inList[0]
        total = ""
        inList = sorted(inList)

        for i in range(len(inList)):
            if len(inList)-1 != i:
                if inList[i] == inList[i+1]-1: # ถ้าค่าindexของinList ไปเท่ากับ index ของ inListตัวถัดไป
                    end = inList[i+1]
                else:
                    if start >= end:
                        total += str(start)+","
                    else:
                        total += str(start)+"-"+str(end)+","
                    start = inList[i+1]
            else:
                if start >= end:
                    total += str(start)+","
                else:
                    total += str(start)+"-"+str(end)+","

        return total[:-1]
    def down_page(self, event=""):
        #app.GetActiveDoc().GetAVPageView().GoTo(self.acrobat.cur_page+1)
        self.acrobat.GoToPage(self.acrobat.cur_page()+2)
        self.root.event_generate("<<changePage>>")
    def up_page(self, event=""):
        #app.GetActiveDoc().GetAVPageView().GoTo(self.acrobat.cur_page+1)
        self.acrobat.GoToPage(self.acrobat.cur_page()-2)
        self.root.event_generate("<<changePage>>")
    def prev_page(self, event=""):
        #curPage = app.GetActiveDoc().GetAVPageView().GetPageNum()
        #app.GetActiveDoc().GetAVPageView().GoTo(curPage-1)
        self.acrobat.GoToPage(self.acrobat.cur_page()-1)
        self.root.event_generate("<<changePage>>")
    def prev_list(self, event=""):
        #curPage = app.GetActiveDoc().GetAVPageView().GetPageNum()
        #app.GetActiveDoc().GetAVPageView().GoTo(curPage-1)
        cur = self.acrobat.cur_page()+1
        try:
            toPage = self.close2(cur, self.list_page)
        except:
            toPage = [-1, 0]
        self.acrobat.GoToPage(self.list_page[toPage[0]]-1)   # <<<<<<<<<<<<<<<<<<<<<<<<<<
        self.root.event_generate("<<changePage>>")
    def auto_next(self, event=""):
        self.break_thread = False
        pythoncom.CoInitialize()
        self.root.event_generate("<<changePage>>")
        app = Dispatch("AcroExch.app")
        numPages = app.GetActiveDoc().GetPDDoc().GetNumPages()
        cur = app.GetActiveDoc().GetAVPageView().GetPageNum()
        sec = float(self.sec.get())
        for i in range(cur, numPages):
        #print(numPages)
        #while(True):
            app.GetActiveDoc().GetAVPageView().GoTo(i)
            varPage = tkinter.StringVar(self.root, value=str(i+1))
            self.entCurPage.config(textvariable=varPage)
            if self.break_thread == True:
            	self.status_run.config(text="status: not auto", fg="red")
            	sys.exit()
            time.sleep(float(self.sec.get()))
        self.status_run.config(text="status: last page", fg="red")
        self.but_auto.config(text="start auto", fg="green")

    def test():
        print("testing")
    def add_list(self, event):
        if self.acrobat.cur_page()+1 not in self.list_page:
            self.list_page.append(self.acrobat.cur_page()+1)
            self.not_page.remove(self.acrobat.cur_page()+1)
            self.list_page = sorted(self.list_page)
        self.showing()
    def clear_list(self, event):
        self.list_page = []
        self.not_page = []
        [self.not_page.append(i) for i in range(1,self.acrobat.numPages()+1)]
        self.showing()
    def remove_cur(self, event):
        if self.acrobat.cur_page()+1 in self.list_page:
            self.list_page.remove(self.acrobat.cur_page()+1)
            self.not_page.append(self.acrobat.cur_page()+1)
            self.list_page = sorted(self.list_page)
        self.showing()
    def start_process(self):
        self.process = multiprocessing.Process(target=self.auto_next)
        self.process.start()
    def stop_process(self):
        self.process.terminate()


    def update_page(self, event=""):
        #if self.entCurPage.get() != str(self.acrobat.cur_page()):
        varPage = tkinter.StringVar(self.root, value=str(self.acrobat.cur_page()+1))
        self.entCurPage.config(textvariable=varPage)


    def showing(self):
        #listPage = ",".join(map(str, self.list_page))

        # self.not_page = sorted(self.not_page)
        listPage = self.listToStrFormat(inList=self.list_page)
        varList = tkinter.StringVar(self.root, value=listPage)
        self.show_list.config(textvariable=varList)
        print("list_page", self.list_page)
        print("not_page", self.not_page)
        self.update_list()

    def update_list(self, event=""):
        self.show_numList.config(text=len(self.list_page))
    def start_thread(self):
        self._stop_event = threading.Event()
        self.thread_next = threading.Thread(name='auto_next', target=self.auto_next)
        self.thread_next.start()
    def check_thread(self, event=""):
        try:
    	    if self.thread_next.is_alive() == True:
    	    	self.stop_thread()
    	    	self.status_run.config( text="status: not auto", fg="red")
    	    	self.but_auto.config(text="start auto", fg="green")
    	    else:
    	    	self.start_thread()
    	    	self.status_run.config(text="status: auto", fg="green")
    	    	self.but_auto.config(text="stop auto", fg="red")
        except AttributeError:
        	self.start_thread()
        	self.status_run.config(text="status: auto", fg="green")
        	self.but_auto.config(text="stop auto", fg="red")

    def stop_thread(self, event=""):
    	self.break_thread = True

    def EnterPage(self, event=""):
        self.acrobat.GoToPage(int(self.entCurPage.get())-1)
    def main_frame(self):
        self.root = Tk()
        #tkinter.Button(self.root, text="prev", command=self.prev_page).pack()
        #tkinter.Button(self.root, text="next", command=self.next_page).pack()

        self.entCurPage = tkinter.Entry(self.root, width=5)
        self.show_numList = tkinter.Label(text=len(self.list_page), fg="red")
        self.entCurPage.bind("<Return>", self.EnterPage)

        self.root.bind("<<changePage>>", self.update_page)

        self.entCurPage.pack(side="right")

        self.update_page()
       	self.status_run = tkinter.Label(self.root, text="status: not auto", fg="red")
       	self.status_run.pack(side="left")
        self.but_auto = tkinter.Button(self.root, text="start auto",fg="green", command=self.check_thread)
        self.but_auto.pack()
        sec_var = tkinter.StringVar()
        sec_var.set("0")
        self.sec = ttk.Spinbox(self.root, width=5, from_=0, to=10, increment=0.1)
        self.sec.set(0)
        self.sec.pack()
        tkinter.Label(self.root, text="sec").pack()
        self.root.bind("<Alt-a>", self.add_list)
        self.root.bind("<Alt-c>", self.clear_list)
        self.root.bind("<Alt-d>", self.remove_cur)
        self.root.bind("<Alt-s>", self.check_thread)
        self.root.bind("<Alt-Left>", self.prev_page)
        self.root.bind("<Alt-Right>", self.next_page)
        self.root.bind("<Alt-Up>", self.up_page)
        self.root.bind("<Alt-Down>", self.down_page)
        self.root.bind("<<update_list>>", self.update_list)
        self.root.bind("<Control-Left>", self.prev_list)
        self.root.bind("<Control-Right>", self.next_list)
        #tkinter.Button(self.root, text="stop", command=self.stop_thread).pack()


        self.root.attributes("-topmost", True)

        self.show_list = tkinter.Entry(self.root, width=50)
        self.show_numList.pack(side="right")
        self.show_list.pack()
    #def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    obj = Action()

    obj.main_frame()
