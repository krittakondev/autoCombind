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
    def __init__(self):
        self.acrobat = Acrobat()
    def next_page(self):
        #app.GetActiveDoc().GetAVPageView().GoTo(self.acrobat.cur_page+1)
        self.acrobat.GoToPage(self.acrobat.cur_page()+2)
        
    def prev_page(self):
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
        tkinter.Button(self.root, text="stop", command=self.auto_next).pack()

        self.root.attributes("-topmost", True)

        tkinter.Text(self.root, width=100, height=2).pack()
    #def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    obj = Action()
    
    obj.main_frame()
