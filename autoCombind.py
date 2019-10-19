import tkinter
import pdfrw
import tkinter.filedialog
import tkinter.messagebox
import os
from tkinter import ttk
import datetime


class GUI():
    def __init__(self, title):
        self.root = tkinter.Tk()
        self.root.title(title)
        #self.root.geometry("300x300")
        
    def add_frame(self):
        return tkinter.Frame(self.root)

        
    def fileSelect(self):
        return tkinter.filedialog.askopenfilenames()
    def mainloop(self):
        self.root.mainloop()


class run_program(GUI):
    def add_pageInfo(self, pageDict, msg):
        pageDict.krit = msg
        return pageDict
    
    def is_odd(self, file):
        page_info = pdfrw.PdfFileReader(file).pages
        if len(page_info) % 2 == 0:
            return False
        else:
            return True
    def combind_loop(self, files, file_index, fileHeader=[], outfile="ไฟล์รวม"):
        blankPage = "blank.pdf"
        writer = pdfrw.PdfWriter()
        cur_dir = os.path.dirname(files[0])
        if len(fileHeader) > 0:
            for head in fileHeader:
                writer.addpages(pdfrw.PdfFileReader(head).pages)
                if self.is_odd(head):
                    writer.addpage(pdfrw.PdfFileReader(blankPage).pages[0])
           
        for i in range(len(files)):
            if file_index != "":
                add_index = self.add_pageInfo(pdfrw.PdfFileReader(file_index).pages[i], "index_insert")
                writer.addpage(add_index)
                writer.addpage(pdfrw.PdfFileReader(blankPage).pages[0])
            if self.is_odd(files[i]):
                writer.addpages(pdfrw.PdfFileReader(files[i]).pages)
                writer.addpage(pdfrw.PdfFileReader(blankPage).pages[0])
            elif len(files)-1 == i:
                writer.addpages(pdfrw.PdfFileReader(files[i]).pages)
                writer.addpage(pdfrw.PdfFileReader(blankPage).pages[0])
                writer.addpage(pdfrw.PdfFileReader(blankPage).pages[0])
            else:
                writer.addpages(pdfrw.PdfFileReader(files[i]).pages)
        saveTo = cur_dir+"/"+outfile+".pdf"
        writer.write(saveTo)  
        writer.write("log/"+datetime.datetime.now().strftime("%y%m%d_%S%M%H.pdf"))
        return saveTo
    def onclick_seFile(self, event=""):
        files = self.fileSelect()
        self.list_filename = files
        for i in range(len(files)):
            self.listFile.insert(tkinter.END, files[i])
        self.insert_index.config(values=self.listFile.get(0, tkinter.END))
        self.listFile.event_generate("<<ListboxSelect>>")
    def clear_alllist(self):
        self.listFile.delete(0, tkinter.END)
        self.insert_index.config(values=self.listFile.get(0, tkinter.END))
        self.insert_index.set("เลือกไฟล์หน้าคั่นบท")
        self.fileHeader = []
        self.showHead.config(text="")
        self.listFile.event_generate("<<ListboxSelect>>")
        self.show_numPages.config(text="0 คั่นบท")
    def get_listFile(self):
        return self.listFile.curselection()
    def set_fileHeader(self):
        cur_se = self.listFile.curselection()
        fileHeader = self.listFile.get(cur_se)
        self.fileHeader.append(fileHeader)
        self.showHead.config(text=self.showHead.cget("text")+"\n"+fileHeader)
        self.listFile.delete(cur_se)
        self.listFile.event_generate("<<ListboxSelect>>")
    
    def showNum_onSelected(self, event):
        try:
            self.listFile.insert(self.remem[0], self.remem[1])
        except AttributeError:
            pass
        selected = self.insert_index.get()
        numPages = len(pdfrw.PdfFileReader(selected).pages)
        self.show_numPages.config(text=str(numPages)+" คั่นบท")
        index_selected = self.listFile.get(0, "end").index(self.insert_index.get())
        
        self.listFile.delete(index_selected)
        self.remem = (index_selected, self.insert_index.get())
        self.listFile.event_generate("<<ListboxSelect>>")
    def delete_selectedList(self):
        self.listFile.delete(self.get_listFile())
        self.listFile.event_generate("<<ListboxSelect>>")
    def onclick_combind(self):
        try:
            #index_selected = self.listFile.get(0, "end").index(self.insert_index.get())
            #self.listFile.delete(index_selected)
            saveTo = self.combind_loop(self.listFile.get(0, tkinter.END), self.insert_index.get(), self.fileHeader, self.fileout.get())
            tkinter.messagebox.showinfo("รวมไฟล์","รวมไฟล์สำเรียบร้อยไฟล์จะเก็บไว้ที่ "+saveTo)
        except Exception as e:
            if str(e) == "tuple.index(x): x not in tuple":

                        
                saveTo = self.combind_loop(self.listFile.get(0, tkinter.END), "", self.fileHeader, self.fileout.get())
                tkinter.messagebox.showinfo("รวมไฟล์","รวมไฟล์สำเรียบร้อยไฟล์จะเก็บไว้ที่ "+saveTo)
    def onKey_listFile(self, event):
        if event.keysym == "Prior":
            self.select_up()
        elif event.keysym == "Next":
            self.select_down()
        elif event.keysym == "Delete":
            self.delete_selectedList()
            
            
    def onEvent_listFile(self, event):
        
        self.show_numFiles.config(text=str(len(self.listFile.get(0,"end")))+" บท")
                
    def select_up(self):
        cur = (self.get_listFile(), self.listFile.get(self.get_listFile()))
        self.listFile.delete(cur[0])
        self.listFile.insert(cur[0][0]-1, cur[1]) 
        self.listFile.selection_set(cur[0][0]-1)
        
    def select_down(self):
        cur = (self.get_listFile(), self.listFile.get(self.get_listFile()))
        self.listFile.delete(cur[0])
        self.listFile.insert(cur[0][0]+1, cur[1]) 
        self.listFile.selection_set(cur[0][0]+1)
        
    def main_gui(self):
        self.frame_left = self.add_frame()
        self.frame_right = self.add_frame()
        self.frame_menu = self.add_frame()
        self.frame_left.grid(row=1, column=1)
        self.frame_right.grid(row=1, column=2)
        self.frame_menu.grid(row=2, column=2)
        self.listFile = tkinter.Listbox(self.frame_left, width=50)
        self.insert_index = ttk.Combobox(self.frame_right, values=self.listFile.get(0, tkinter.END), width=40)
        self.insert_index.set("เลือกไฟล์หน้าคั่นบท")
        tkinter.Label(self.frame_left, text="ไฟล์แต่ละบท", font=("Courier", 30)).pack()
        self.listFile.pack(side=tkinter.LEFT)
        self.listFile.bind("<KeyPress>", self.onKey_listFile)
        self.listFile.bind("<<ListboxSelect>>", self.onEvent_listFile)
        tkinter.Button(self.frame_left, text="Up", command=self.select_up).pack()
        tkinter.Button(self.frame_left, text="Down", command=self.select_down).pack()
        tkinter.Button(self.frame_right, text="เลือกสาระบัญและปกใน", font=("Courier", 15), command=lambda: self.set_fileHeader()).pack()
        self.show_numFiles = tkinter.Label(self.frame_left,fg="red",font=("Courier", 15), text="0 บท")
        self.show_numFiles.pack(side=tkinter.LEFT)
        self.showHead = tkinter.Label(self.frame_right, text="", font=("Courier", 10))
        self.showHead.pack()
        self.insert_index.pack(side=tkinter.LEFT)       
        self.show_numPages = tkinter.Label(self.frame_right,font=("Courier", 13), text="0 คั่นบท", fg="red")
        self.insert_index.bind("<<ComboboxSelected>>", self.showNum_onSelected)
        self.show_numPages.pack()
        tkinter.Button(self.frame_menu, text="เลือกไฟล์", font=("Courier", 13), command=lambda: self.onclick_seFile()).pack()
        tkinter.Button(self.frame_menu, text="clear", command=lambda: self.clear_alllist()).pack()
        tkinter.Button(self.frame_menu, text="delete", command=lambda: self.delete_selectedList()).pack()
        defaultName = tkinter.StringVar()
        defaultName.set("รวมไฟล์")
        self.fileout = tkinter.Entry(self.frame_menu, font=("Courier", 13), textvariable=defaultName)
        self.fileout.pack()
        tkinter.Button(self.frame_menu, text="combind", fg="pink", bg="green", command=lambda: self.onclick_combind()).pack()
        self.root.bind_all("<Control-o>", self.onclick_seFile)
        self.root.mainloop()
    
    #def pageInsert(self):
        
    

if __name__ == "__main__":
    #root = tkinter.Tk()
    #root.withdraw()
    #file = tkinter.filedialog.askopenfilenames()
    #combind_loop(file)
    run = run_program("autoCombind")
    run.fileHeader = []
    run.main_gui()
