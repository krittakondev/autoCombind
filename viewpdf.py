import tkinter
from tkinter import Tk
from win32com.client.dynamic import Dispatch
import time
import threading
import multiprocessing

class Acrobat:
    def __init__(self):
        self.app = Dispatch("AcroExch.app")
    def cur_page(self):
        return self.app.GetActiveDoc().GetAVPageView().GetPageNum()
    def numPages(self):
        return self.app.GetActiveDoc().GetPDDoc().GetNumPages()
    def GoToPage(self, To):
        self.app.GetActiveDoc().GetAVPageView().GoTo(To-1)

class Action:
    list_page = []
    def __init__(self):
        self.acrobat = Acrobat()
    def next_page(self, event=""):
        #app.GetActiveDoc().GetAVPageView().GoTo(self.acrobat.cur_page+1)
        self.acrobat.GoToPage(self.acrobat.cur_page()+2)
        
    def down_page(self, event=""):
        #app.GetActiveDoc().GetAVPageView().GoTo(self.acrobat.cur_page+1)
        self.acrobat.GoToPage(self.acrobat.cur_page()+3)
    def up_page(self, event=""):
        #app.GetActiveDoc().GetAVPageView().GoTo(self.acrobat.cur_page+1)
        self.acrobat.GoToPage(self.acrobat.cur_page()-1)
    def prev_page(self, event=""):
        #curPage = app.GetActiveDoc().GetAVPageView().GetPageNum()
        #app.GetActiveDoc().GetAVPageView().GoTo(curPage-1)
        self.acrobat.GoToPage(self.acrobat.cur_page())
    def auto_next(self):
        numPages = self.acrobat.numPages()
        cur = self.acrobat.cur_page()
        for i in range(cur, numPages):
        #print(numPages)
        #while(True):
            self.acrobat.GoToPage(i)
            time.sleep(0.5)
        
    def add_list(self, event):
        self.list_page.append(self.acrobat.cur_page())
        print(self.list_page)
    def stop_thread(self):
        print(threading.activeCount())

    def start_thread(self):
        e = threading.Event()
        self.thread_next = threading.Thread(name='auto_next', target=self.auto_next, args=(e, ))
        self.thread_next.start()
    def main_frame(self):
        self.root = Tk()
        tkinter.Button(self.root, text="prev", command=self.prev_page).pack()
        tkinter.Button(self.root, text="next", command=self.next_page).pack()
        tkinter.Button(self.root, text="auto next", command=self.auto_next).pack()
        self.root.bind("a", self.add_list)
        self.root.bind("<Left>", self.prev_page)
        self.root.bind("<Right>", self.next_page)
        self.root.bind("<Up>", self.up_page)
        self.root.bind("<Down>", self.down_page)
        tkinter.Button(self.root, text="stop", command=self.auto_next).pack()

        self.root.attributes("-topmost", True)

        show_list = tkinter.Text(self.root, width=50, height=2).pack()
    #def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    obj = Action()
    
    obj.main_frame()
