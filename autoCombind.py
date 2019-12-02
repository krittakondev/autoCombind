import tkinter
import pdfrw
import tkinter.filedialog
import tkinter.messagebox
import os
from tkinter import ttk
import datetime
from PyPDF2 import PdfFileReader, PdfFileWriter
import shutil

"""
เขียนเพิ่มเติมให้สามารถใช้หน้าคั่นหน้าเดี่ยวกันได้

"""

class GUI():
    def __init__(self, title):
        self.root = tkinter.Tk()
        self.root.title(title)
        #self.root.geometry("300x300")
        
    def add_frame(self):
        return tkinter.Frame(self.root)

        
    def fileSelect(self):
        return tkinter.filedialog.askopenfilenames(filetypes=[("pdf files", "*.pdf")])
    def mainloop(self):
        self.root.mainloop()

class run_program(GUI):
    infoPage = {}
    MAIN_PATH = os.path.dirname(os.path.realpath(__file__))

    def pdfRead(self, pdfFile):
        f = open(pdfFile, "rb")
        reader = pdfR(f)
        f.close()
        return reader
    def add_pageInfo(self, pageDict, msg):

        pageDict.krit = str(msg)
        return pageDict
    
    def is_odd(self, numPages):
        #page_info = pdfrw.PdfFileReader(file).pages
        if numPages % 2 == 0:
            return False
        else:
            return True

    def combind_loop(self, files, file_index, fileHeader=[], outfile="ไฟล์รวม"):
        blankPage = "blank.pdf"
        blankPage = PdfFileReader(open(blankPage,"rb")).getPage(0)
        countNum = 0
        writer = PdfFileWriter()
        cur_dir = os.path.dirname(files[0])
        page_list = []
        if len(fileHeader) > 0:
            for head in fileHeader:
                pagesHead = PdfFileReader(open(head, "rb"))
                for page in range(pagesHead.numPages):
                    writer.addPage(pagesHead.getPage(page))
                    countNum += 1
                if self.is_odd(pagesHead.numPages):
                    # writer.addPage(blankPage)
                    writer.addBlankPage()
                        # else:
                        #     page_list.append()
           
        for i in range(len(files)):
            if(self.listFile.itemcget(i, "fg")=="red"):
                _1page = PdfFileReader(open(files[i], 'rb'))
                for _1 in range(_1page.numPages):
                    writer.addPage(_1page.getPage(_1))
                    # writer.addPage(blankPage)
                    writer.addBlankPage()
                    print(writer.getNumPages())
                    
            else:
                if file_index != "" and self.showInsertBox.get()==1:
                    readFile = PdfFileReader(open(file_index, "rb"))
                    if readFile.numPages == len(self.listFile.get(0,"end")): 
                        #add_index = self.add_pageInfo(readFile.pages[i], "index_insert")
                    
                        writer.addPage(readFile.getPage(i))
                    else:
                        print(len(self.listFile.get("end")))
                        return "หน้าคั่นไม่เท่ากัน"
                        
                    if self.insertBlank.get() == 1:
                        
                        # writer.addpage(blankPage)
                        writer.addBlankPage()
                        
                mainLesson = PdfFileReader(open(files[i], "rb"))
                writer.appendPagesFromReader(mainLesson)
                # for ml in range(mainLesson.numPages):
                #     # print("เลขหน้า: "+str(ml)+"\nรอบที่: "+str(i))
                #     writer.addPage(mainLesson.getPage(ml))
                if self.insertBlank.get() == 1:
                    is_insert = self.is_odd(PdfFileReader(open(files[i], "rb")).numPages)
                    #writer.addpages(pdfrw.PdfFileReader(files[i]).pages)
                    if len(files)-1 == i and is_insert == False:
                        # writer.addPage(blankPage)
                        # writer.addPage(blankPage)   
                        writer.addBlankPage()
                        writer.addBlankPage()
                
                    if is_insert:
                        # writer.addPage(blankPage)   
                        writer.addBlankPage()
            print(writer.getNumPages())
        if outfile[-4:].lower() == ".pdf":
            saveTo = os.path.join(cur_dir, outfile)
        else:
            saveTo = os.path.join(cur_dir, outfile+".pdf")
        # path_log = os.path.join(os.path.dirname(os.path.realpath(__file__)),"log")
        # genName = datetime.datetime.now().strftime("%y%m%d_%S%M%H.pdf")
        # if(os.path.exists(path_log)==False):
        #     os.mkdir(path_log)
        #     if(os.path.exists(os.path.join(path_log, "files"))==False):
        #         os.mkdir(os.path.join(path_log, "files"))
        print("saving")
        test = writer.write(open(saveTo,'wb'))  
        print("saved")
        # writer.write(open(os.path.join(path_log, os.path.join("files",genName)), "wb"))
        return saveTo

    def mark_1side(self, event):
        cur = self.get_listFile()
        if(self.listFile.itemcget(cur[0], "fg")=="red"):
            self.listFile.itemconfig(cur[0], {"fg": "black"})
        else:
            self.listFile.itemconfig(cur[0], {"fg":"red"})

    def onclick_seFile(self, event=""):
        files = self.fileSelect()
        self.list_filename = files
        for i in range(len(files)):
            self.listFile.insert(tkinter.END, files[i])
        self.insert_index.config(values=self.listFile.get(0, tkinter.END))
        self.insert_index.xview_moveto(1.0)
        self.listFile.event_generate("<<UpdateValue>>")
    def clear_alllist(self):
        self.listFile.delete(0, tkinter.END)
        self.insert_index.config(values=self.listFile.get(0, tkinter.END))
        self.insert_index.set("เลือกไฟล์หน้าคั่นบท")
        self.fileHeader = []
        self.showHead.config(text="")
        self.listFile.event_generate("<<UpdateValue>>")
        self.show_numPages.config(text="0 คั่นบท")
    def get_listFile(self):
        return self.listFile.curselection()
    def set_fileHeader(self):
        cur_se = self.listFile.curselection()
        fileHeader = self.listFile.get(cur_se)
        self.fileHeader.append(fileHeader)
        self.showHead.config(text=self.showHead.cget("text")+"\n"+fileHeader)
        self.listFile.delete(cur_se)
        self.listFile.event_generate("<<UpdateValue>>")
    
    def showNum_onSelected(self, event):
        try:
            self.listFile.insert(self.remem[0], self.remem[1])
        except AttributeError:
            pass
        selected = self.insert_index.get()
        self.numPagesInsert = len(pdfrw.PdfFileReader(selected).pages)
        self.show_numPages.config(text=str(self.numPagesInsert)+" คั่นบท")
        index_selected = self.listFile.get(0, "end").index(self.insert_index.get())
        
        self.listFile.delete(index_selected)
        self.remem = (index_selected, self.insert_index.get())
        self.listFile.event_generate("<<UpdateValue>>")
    def delete_selectedList(self):
        self.listFile.delete(self.get_listFile())
        self.listFile.event_generate("<<UpdateValue>>")
    def onclick_combind(self):
        try:
            #index_selected = self.listFile.get(0, "end").index(self.insert_index.get())
            #self.listFile.delete(index_selected)
            saveTo = self.combind_loop(self.listFile.get(0, tkinter.END), self.insert_index.get(), self.fileHeader, self.fileout.get())
            if saveTo == "หน้าคั่นไม่เท่ากัน":
                tkinter.messagebox.showerror("รวมไฟล์","ไม่สามารถรวมไฟล์ได้เนื่องจากจำนวนบทกับจำนวนหน้าไม่เท่ากัน")
            else:
                tkinter.messagebox.showinfo("รวมไฟล์","รวมไฟล์สำเรียบร้อยไฟล์จะเก็บไว้ที่ "+saveTo)
                path_log = os.path.join(self.MAIN_PATH,"log")
                genName = datetime.datetime.now().strftime("%y%m%d_%S%M%H.pdf")
                if(os.path.exists(path_log)==False):
                    os.mkdir(path_log)
                    if(os.path.exists(os.path.join(path_log, "files"))==False):
                        os.mkdir(os.path.join(path_log, "files"))
                path_log_file = os.path.join(path_log, "files")
                shutil.copy2(saveTo, os.path.join(path_log_file, genName))
        except Exception as e:
            print(e.args)
            if e.args[0] == "list index out of range":

                        
                #saveTo = self.combind_loop(self.listFile.get(0, tkinter.END), "", self.fileHeader, self.fileout.get())
                tkinter.messagebox.showerror("รวมไฟล์","ไม่สามารถรวมไฟล์ได้เนื่องจากจำนวนบทกับจำนวนหน้าไม่เท่ากัน")
            
            elif e.args[0] == 13:
                tkinter.messagebox.showerror("รวมไฟล์","ไม่สามารถsaveไฟล์ได้เนื่องจากไฟล์กำลังเปิดอยู่")
            elif e.args[0] == "Could not read PDF file เลือกไฟล์หน้าคั่นบท":
                tkinter.messagebox.showerror("รวมไฟล์","คุณยังไม่ได้เลือกหน้าคั่น โปรดเลือกหน้าคั่น")
    def onKey_listFile(self, event):
        if event.keysym == "Prior":
            self.select_up()
        elif event.keysym == "Next":
            self.select_down()
        elif event.keysym == "Delete":
            self.delete_selectedList()
            
            
    def onEvent_listFile(self, event):
        cur_se = self.listFile.curselection()
        self.infoPage["name"] = os.path.basename(self.listFile.get(cur_se))
        self.infoPage["num"] = str(len(pdfrw.PdfReader(self.listFile.get(cur_se)).pages))
        self.infoPage["lesson_num"] = str(cur_se[0]+1)
        #self.show_infoName.forget()
        self.show_infoName.config(text="ชื่อไฟล์: "+self.infoPage["name"])
        self.show_infoNum.config(text="จำนวนหน้า: "+self.infoPage["num"])
        self.show_lessonNum.config(text="บทที่: "+self.infoPage["lesson_num"])
        self.show_infoName.pack()
        self.show_lessonNum.pack()
        self.show_infoNum.pack()
        

    def update_value(self, event):
        #self.listFile.event_generate("<<ListboxSelect>>")
        self.show_numFiles.config(text=str(len(self.listFile.get(0,"end")))+" บท")
        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        self.listFile.xview_moveto(1.0)
        
    def select_up(self):
        cur = (self.get_listFile(), self.listFile.get(self.get_listFile()))
        self.listFile.delete(cur[0])
        self.listFile.insert(cur[0][0]-1, cur[1]) 
        self.listFile.selection_set(cur[0][0]-1)
        #self.listFile.select_set(cur[0]-1)
        
    def select_down(self):
        cur = (self.get_listFile(), self.listFile.get(self.get_listFile()))
        self.listFile.delete(cur[0])
        self.listFile.insert(cur[0][0]+1, cur[1]) 
        self.listFile.selection_set(cur[0][0]+1)
     
        #self.listFile.select_set(cur[0]+1)
    def check_box(self):
        #self.listFile.select_set(2)
        if self.showInsertBox.get() == 1:
            self.insert_index.pack(side=tkinter.LEFT)
            
            self.frameRadio.pack()
            #tkinter.Radiobutton(self.frameRadio, text="หน้าเดียว").pack() # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
            #tkinter.Radiobutton(self.frameRadio, text="ทุกหน้า").pack()
            self.show_numPages.pack()
        else:
            self.insert_index.forget()
            self.show_numPages.forget()
            self.frameRadio.forget()
    def main_gui(self):
        self.frame_left = self.add_frame()
        self.frame_right = self.add_frame()
        self.frame_infoFile = self.add_frame()
        self.frame_menu = self.add_frame()
        self.frame_left.grid(row=1, column=1)
        self.frame_right.grid(row=1, column=2)
        self.frame_infoFile.grid(row=2, column=1)
        self.frame_menu.grid(row=2, column=2)
        
        self.show_infoName = tkinter.Label(self.frame_infoFile, font=("Courier", 15))
        self.show_infoNum = tkinter.Label(self.frame_infoFile, font=("Courier", 15))
        self.show_lessonNum = tkinter.Label(self.frame_infoFile, font=("Courier", 15))
        
        self.listFile = tkinter.Listbox(self.frame_left, width=80)
        self.insert_index = ttk.Combobox(self.frame_right, values=self.listFile.get(0, tkinter.END), width=40)
        self.insert_index.set("เลือกไฟล์หน้าคั่นบท")
        tkinter.Label(self.frame_left, text="ไฟล์แต่ละบท", font=("Courier", 30)).pack()
        self.listFile.pack(side=tkinter.LEFT)
        self.listFile.bind("<KeyPress>", self.onKey_listFile)
        self.listFile.bind("<<ListboxSelect>>", self.onEvent_listFile)
        self.listFile.bind("<<UpdateValue>>", self.update_value)
        self.listFile.bind("<Control-b>", self.mark_1side)
     
        self.scrollList = tkinter.Scrollbar(self.frame_left, orient="vertical")
        self.scrollList.config(command=self.listFile.yview)
        self.scrollList.pack(side=tkinter.LEFT, fill='y')    
        
        #print(self.listFile.xview()) #<<<<<<<<<<<<<<<<<<<<<<<<
        
        self.listFile.config(yscrollcommand=self.scrollList.set)

        upImage = tkinter.PhotoImage(file=os.path.join(self.MAIN_PATH, "up.png"))
        upImage = upImage.subsample(25,25)
        downImage = tkinter.PhotoImage(file=os.path.join(self.MAIN_PATH, "down.png"))
        downImage = downImage.subsample(25,25)
        tkinter.Button(self.frame_left, image=upImage, command=self.select_up).pack()
        tkinter.Button(self.frame_left, image=downImage, command=self.select_down).pack()
        tkinter.Button(self.frame_right, text="เลือกสาระบัญและปกใน", font=("Courier", 15), command=lambda: self.set_fileHeader()).pack()
        self.show_numFiles = tkinter.Label(self.frame_left,fg="red",font=("Courier", 15), text="0 บท")
        self.show_numFiles.pack(side=tkinter.LEFT)
        self.showHead = tkinter.Label(self.frame_right, text="", font=("Courier", 10))
        self.showHead.pack()
        #self.insert_index.pack(side=tkinter.LEFT)       
        self.show_numPages = tkinter.Label(self.frame_right,font=("Courier", 13), text="0 คั่นบท", fg="red")
        self.insert_index.bind("<<ComboboxSelected>>", self.showNum_onSelected)
        self.showInsertBox = tkinter.IntVar()
        self.show_insert = tkinter.Checkbutton(self.frame_right,text="หน้าคั่นบท",font=("Courier", 13), variable=self.showInsertBox, command=self.check_box)
        self.frameRadio = ttk.Labelframe(self.frame_right, text="options")
        self.show_insert.pack()
        #self.show_numPages.pack()
        self.insertBlank = tkinter.IntVar()
        self.blankList = tkinter.IntVar()
        self.show_insertBlank = tkinter.Checkbutton(self.frame_right,text="แทรกหน้าขาวถ้าไม่เข้าคู่",font=("", 13), variable=self.insertBlank)
        self.get_blankList = tkinter.Checkbutton(self.frame_right,text="เลขหน้าแทนการแทรกขาว",font=("", 13), variable=self.blankList)
        self.show_insertBlank.pack()
        self.get_blankList.pack()
        tkinter.Button(self.frame_menu, text="เลือกไฟล์", font=("Courier", 13), command=lambda: self.onclick_seFile(), fg="yellow", bg="#999999").pack()
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
