import tkinter
from tkinter import Tk
from win32com.client.dynamic import Dispatch
import time
import threading
import multiprocessing
import pythoncom

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
    def __init__(self):
        self.acrobat = Acrobat()
    def next_page(self, event=""):
        #app.GetActiveDoc().GetAVPageView().GoTo(self.acrobat.cur_page+1)
        self.acrobat.GoToPage(self.acrobat.cur_page()+1)
        self.root.event_generate("<<changePage>>")

        
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
    def auto_next(self):
        self.stop_thread = False
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
            varPage = tkinter.StringVar(self.root, value=str(i))
            self.entCurPage.config(textvariable=varPage)
            if self.stop_thread == True:
            	break
            time.sleep(sec)
        
    def test():
        print("testing")
    def add_list(self, event):
        if self.acrobat.cur_page()+1 not in self.list_page:
            self.list_page.append(self.acrobat.cur_page()+1)
            self.list_page = sorted(self.list_page)
        self.showing()
        print(self.list_page)
    def clear_list(self, event):
        self.list_page = []
        self.showing()
    def remove_cur(self, event):
        if self.acrobat.cur_page()+1 in self.list_page:
            self.list_page.remove(self.acrobat.cur_page()+1)
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
        listPage = ",".join(map(str, self.list_page))
        varList = tkinter.StringVar(self.root, value=listPage)
        self.show_list.config(textvariable=varList)
        self.update_list()
        
    def update_list(self, event=""):
        self.show_numList.config(text=len(self.list_page))
    def start_thread(self):
        self._stop_event = threading.Event()
        self.thread_next = threading.Thread(name='auto_next', target=self.auto_next)
        self.thread_next.start()

    def stop_thread(self):
    	self.stop_thread = True

    def EnterPage(self, event=""):
        self.acrobat.GoToPage(int(self.entCurPage.get())-1)
    def main_frame(self):
        self.root = Tk()
        #tkinter.Button(self.root, text="prev", command=self.prev_page).pack()
        #tkinter.Button(self.root, text="next", command=self.next_page).pack()

        self.entCurPage = tkinter.Entry(self.root, width=5)
        self.show_numList = tkinter.Label(text=len(self.list_page))
        self.entCurPage.bind("<Return>", self.EnterPage)

        self.root.bind("<<changePage>>", self.update_page)    
        
        self.entCurPage.pack(side="right")

        self.update_page()
        
        tkinter.Button(self.root, text="auto next", command=self.start_thread).pack()
        self.sec = tkinter.Entry(self.root, width=5)
        self.sec.pack()
        tkinter.Label(self.root, text="sec").pack()
        self.root.bind("<Alt-a>", self.add_list)
        self.root.bind("<Alt-c>", self.clear_list)
        self.root.bind("<Alt-d>", self.remove_cur)
        self.root.bind("<Left>", self.prev_page)
        self.root.bind("<Right>", self.next_page)
        self.root.bind("<Up>", self.up_page)
        self.root.bind("<Down>", self.down_page)
        self.root.bind("<<update_list>>", self.update_list)
        tkinter.Button(self.root, text="stop", command=self.stop_thread).pack()

        
        self.root.attributes("-topmost", True)

        self.show_list = tkinter.Entry(self.root, width=50)
        self.show_numList.pack(side="right")
        self.show_list.pack()
    #def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    obj = Action()
    
    obj.main_frame()
