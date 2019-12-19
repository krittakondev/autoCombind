import tkinter
import pdfrw
import tkinter.filedialog
import tkinter.messagebox
import os
from tkinter import ttk
import datetime
from PyPDF2 import PdfFileReader, PdfFileWriter
import shutil
import subprocess
from tkinter import simpledialog 

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

    def combind_loop(self, files, file_index, fileHeader=[], outfile="ไฟล์รวม", passwd=None):
        #blankPage = "blank.pdf"
        #blankPage = PdfFileReader(open(blankPage,"rb")).getPage(0)
        print("starting combind...\n")
        countNum = 0
        writer = PdfFileWriter()
        cur_dir = os.path.dirname(files[0])
        page_list = []

        # รวมช่วงไฟล์ header
        if len(fileHeader) > 0:
            for head in fileHeader:
                pagesHead = PdfFileReader(open(head, "rb")) 
                for page in range(pagesHead.numPages):
                    writer.addPage(pagesHead.getPage(page))
                    countNum += 1
                if self.is_odd(pagesHead.numPages):
                    # writer.addPage(blankPage)
                    writer.addBlankPage()
                    writer.addBookmark("blank", writer.getNumPages()-1)
                        # else:
                        #     page_list.append()
           
        for i in range(len(files)):
            # ไฟล์ที่มาร์คสีแดง ให้แทรกขาวหลังทุกหน้า 
            if(self.listFile.itemcget(i, "fg")=="red"):
                _1page = PdfFileReader(open(files[i], 'rb'))
                for _1 in range(_1page.numPages):
                    writer.addPage(_1page.getPage(_1))
                    # writer.addPage(blankPage)
                    writer.addBlankPage()
                    writer.addBookmark("blank", writer.getNumPages()-1)
                    
            else:
                # ไฟล์ insert
                if file_index != "" and self.showInsertBox.get()==1:
                    readFile = PdfFileReader(open(file_index, "rb"))
                    if readFile.numPages == len(self.listFile.get(0,"end")): 
                        #add_index = self.add_pageInfo(readFile.pages[i], "index_insert")
                    
                        writer.addPage(readFile.getPage(i))
                        writer.addBookmark("คั่น", writer.getNumPages()-1)

                    else:
                        print(len(self.listFile.get("end")))
                        return "หน้าคั่นไม่เท่ากัน"
                        
                    if self.insertBlank.get() == 1:
                        
                        # writer.addpage(blankPage)
                        writer.addBlankPage()
                        writer.addBookmark("blank", writer.getNumPages()-1)
                        
                mainLesson = PdfFileReader(open(files[i], "rb"))
                writer.appendPagesFromReader(mainLesson)
                # for ml in range(mainLesson.numPages):
                #     # print("เลขหน้า: "+str(ml)+"\nรอบที่: "+str(i))
                #     writer.addPage(mainLesson.getPage(ml))
                if self.insertBlank.get() == 1:
                    is_insert = self.is_odd(PdfFileReader(open(files[i], "rb")).getNumPages())
                    #writer.addpages(pdfrw.PdfFileReader(files[i]).pages)
                    if len(files)-1 == i and is_insert == False:
                        # writer.addPage(blankPage)
                        # writer.addPage(blankPage)   
                        writer.addBlankPage()
                        writer.addBookmark("blankLast", writer.getNumPages()-1)
                        # writer.addBlankPage()
                        # writer.addBookmark("blank", writer.getNumPages()-1)
                
                    if is_insert:
                        # writer.addPage(blankPage)   
                        writer.addBlankPage()
                        writer.addBookmark("blank", writer.getNumPages()-1)
            print(writer.getNumPages())
        outfile = tkinter.filedialog.asksaveasfilename(title="ตั้งชื่อไฟล์รวม", filetypes=(("file pdf", "*.pdf"), ("file all", "*.*")))
        
        while(outfile == "" or outfile == None):
            ask_resave = tkinter.messagebox.askquestion("การsaveไฟล์", "โปรแกรมcombindไฟล์เสร็จเรียบร้อยแล้วแต่คุณยังไม่ได้บันทึกไฟล์ คุณต้องการกลับไปsaveไฟล์ใหม่หรือไม่?", icon="warning")
            if(ask_resave == "yes"):
                outfile = tkinter.filedialog.asksaveasfilename(title="ตั้งชื่อไฟล์รวม", filetypes=(("file pdf", "*.pdf"), ("file all", "*.*")))
            else:
                return None
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
        oFile = open(saveTo,'wb')
        print("saving")
        if passwd != None:
            print("encrypt...")
            writer.encrypt(passwd, passwd)
        test = writer.write(oFile)  
        oFile.close()
        print("saved")
        # writer.write(open(os.path.join(path_log, os.path.join("files",genName)), "wb"))
        return os.path.realpath(saveTo)
        #return saveTo

    def mark_1side(self, event):
        cur = self.get_listFile()
        if(self.listFile.itemcget(cur[0], "fg")=="red"):
            self.listFile.itemconfig(cur[0], {"fg": "black"})
        else:
            self.listFile.itemconfig(cur[0], {"fg":"red"})
        self.listFile.selection_clear(0, tkinter.END)

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
    
    def searchBookmarkPages(self, loFile, val, startZero=False):
        pages = []
        r = PdfFileReader(open(loFile, "rb"))
        all_bookmark = r.getOutlines()
        for bm in all_bookmark:
            if bm["/Title"] == val:
                pageNum = r.getDestinationPageNumber(bm)
                if(startZero == False):
                    pageNum += 1
                if pageNum not in pages: 
                    pages.append(pageNum)
        return pages
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



    def showNum_onSelected(self, event):
        try:
            self.listFile.insert(self.remem[0], self.remem[1])
        except AttributeError:
            pass
        selected = self.insert_index.get()
        self.numPagesInsert = PdfFileReader(open(selected, 'rb')).getNumPages()
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
            passwdChecked = None
            if self.pdfEncrypt.get() == 1:
                passwd = simpledialog.askstring("ใส่รหัสผ่าน", "Enter password", parent=self.root, show="*")
                if passwd == None:
                    return False
                elif len(passwd) <= 5:
                    tkinter.messagebox.showerror("รหัสผ่านผิดพลาด", "โปรดกรอกรหัส 6 ตัวขึ้นไป")
                    return False
                else:
                    passwdNew = simpledialog.askstring("ใส่รหัสผ่านอีกครั้ง", "Enter password again", parent=self.root, show="*")
                    if passwdNew == None:
                        return False
                    elif len(passwdNew) <= 5:
                        tkinter.messagebox.showerror("รหัสผ่านผิดพลาด", "โปรดกรอกรหัส 6 ตัวขึ้นไป")
                        return False
                    if passwd == passwdNew:
                        passwdChecked = passwdNew
                    else:
                        tkinter.messagebox.showerror("รหัสผ่านผิดพลาด", "โปรดกรอกรหัสให้ตรงกันทั้งสองครั้ง")
                        return False
            #index_selected = self.listFile.get(0, "end").index(self.insert_index.get())
            #self.listFile.delete(index_selected)
            saveTo = self.combind_loop(self.listFile.get(0, tkinter.END), self.insert_index.get(), self.fileHeader, self.fileout.get(), passwd=passwdChecked)
            if saveTo == "หน้าคั่นไม่เท่ากัน":
                tkinter.messagebox.showerror("รวมไฟล์","ไม่สามารถรวมไฟล์ได้เนื่องจากจำนวนบทกับจำนวนหน้าไม่เท่ากัน")                
            elif saveTo != None:
                askOpen = tkinter.messagebox.askquestion("รวมไฟล์","รวมไฟล์สำเรียบร้อยไฟล์จะเก็บไว้ที่ "+saveTo+" ต้องการเปิดไฟล์เลยหรือไม่?")
                if (askOpen=="yes"):
                    #subprocess.Popen([saveTo], shell=True)
                    os.startfile(saveTo)
                path_log = os.path.realpath(os.path.join(self.MAIN_PATH,"log"))
                genName = datetime.datetime.now().strftime("%y%m%d_%S%M%H.pdf")
                print("check dir")
                if(os.path.isdir(path_log)==False):
                    os.mkdir(path_log)
                if(os.path.isdir(os.path.join(path_log, "files"))==False):
                    print("make dir")
                    os.mkdir(os.path.join(path_log, "files"))
                path_log_file = os.path.join(path_log, "files")
                blank_list = self.listToStrFormat(self.searchBookmarkPages(saveTo, "blank"))
                index_list = self.listToStrFormat(self.searchBookmarkPages(saveTo, "คั่น"))
                msgHeader = "# "+os.path.basename(saveTo)+"\n\n"
                msgTotal = msgHeader+"[หน้าขาว]\n"+blank_list+"\n\n[หน้าคั่น]\n"+index_list+"\n\n"
                print(blank_list, index_list)
                with open(saveTo+".txt", "w",encoding="utf8") as info:
                    info.writelines(msgTotal)
                shutil.copy2(saveTo+".txt", os.path.join(path_log, genName+".txt"))
                shutil.copy2(saveTo, os.path.join(path_log_file, genName))
        except Exception as e:
            print(e)
            #print(help(dir))
            print(e.args)
            if e.args[0] == "list index out of range":

                        
                #saveTo = self.combind_loop(self.listFile.get(0, tkinter.END), "", self.fileHeader, self.fileout.get())
                tkinter.messagebox.showerror("เกิด error", str(e))
            
            elif e.args[0] == 13:
                tkinter.messagebox.showerror("รวมไฟล์","ไม่สามารถsaveไฟล์ได้เนื่องจากไฟล์กำลังเปิดอยู่ โปรดใช้ชื่อใหม่หรือปิดไฟล์pdfที่เปิดอยู่ออก")
            elif e.args[0] == "Could not read PDF file เลือกไฟล์หน้าคั่นบท":
                tkinter.messagebox.showerror("รวมไฟล์","คุณยังไม่ได้เลือกหน้าคั่น โปรดเลือกหน้าคั่น")
            else:
                tkinter.messagebox.showerror("เกิด error", str(e))
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
        self.infoPage["num"] = str(PdfFileReader(open(self.listFile.get(cur_se), 'rb')).getNumPages())
        self.infoPage["lesson_num"] = str(cur_se[0]+1)
        #self.show_infoName.forget()
        self.show_lessonNum.config(text="ไฟล์ที่: "+self.infoPage["lesson_num"])
        self.show_infoName.config(text="ชื่อไฟล์: "+self.infoPage["name"])
        self.show_infoNum.config(text="จำนวนหน้า: "+self.infoPage["num"])
        
        self.show_lessonNum.pack()
        self.show_infoName.pack()
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
    def openFile(self,fileIn):
        print(fileIn)
        os.startfile(fileIn)


    def menu_combindList(self, event):
        row_select = self.listFile.nearest(event.y)
        self.listFile.select_clear(0, "end")
        self.listFile.selection_set(row_select)
        self.listFile.activate(row_select)

        if(len(self.listFile.curselection()) != 0):
            self.menuListFile.post(event.x_root, event.y_root)
        print(row_select)
    def main_gui(self):

        self.frame_left = self.add_frame()
        self.frame_right = self.add_frame()
        self.frame_infoFile = self.add_frame()
        self.frame_menu = self.add_frame()
        self.frame_left.grid(row=1, column=1)
        self.frame_right.grid(row=1, column=2)
        self.frame_infoFile.grid(row=2, column=1)
        self.frame_menu.grid(row=2, column=2)

        
        self.show_lessonNum = tkinter.Label(self.frame_infoFile, font=("Courier", 15))
        self.show_infoName = tkinter.Label(self.frame_infoFile, font=("Courier", 15))
        self.show_infoNum = tkinter.Label(self.frame_infoFile, font=("Courier", 15))
        
        
        self.listFile = tkinter.Listbox(self.frame_left, width=80)
        self.menuListFile = tkinter.Menu(self.listFile, tearoff=0)
        self.menuListFile.add_command(label="open file", command=lambda: self.openFile(fileIn=self.listFile.get(self.listFile.curselection())))
        self.menuListFile.add_command(label="open folder", command=lambda: os.startfile(os.path.dirname(self.listFile.get(self.listFile.curselection()))))
        self.menuListFile.add_command(label="delete", command=self.delete_selectedList)

        self.insert_index = ttk.Combobox(self.frame_right, values=self.listFile.get(0, tkinter.END), width=40)
        self.insert_index.set("เลือกไฟล์หน้าคั่นบท")
        tkinter.Label(self.frame_left, text="ไฟล์แต่ละบท", font=("Courier", 30)).pack()
        self.listFile.pack(side=tkinter.LEFT)
        self.listFile.bind("<KeyPress>", self.onKey_listFile)
        #self.listFile.bind("<<ListboxSelect>>", self.onEvent_listFile)
        self.listFile.bind("<Double-Button-1>", self.onEvent_listFile)
        #self.listFile.bind("<<UpdateValue>>", self.update_value)
        self.listFile.bind("<Control-b>", self.mark_1side)
        self.listFile.bind("<Button-3>", self.menu_combindList)
     
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
        self.pdfEncrypt = tkinter.IntVar()
        #elf.blankList = tkinter.IntVar()
        self.show_insertBlank = tkinter.Checkbutton(self.frame_right,text="แทรกหน้าขาวถ้าไม่เข้าคู่",font=("", 13), variable=self.insertBlank)
        self.opt_encrypt = tkinter.Checkbutton(self.frame_right,text="เข้ารหัส",font=("", 13), variable=self.pdfEncrypt)
        #self.get_blankList = tkinter.Checkbutton(self.frame_right,text="เลขหน้าแทนการแทรกขาว",font=("", 13), variable=self.blankList)
        self.show_insertBlank.pack()
        self.opt_encrypt.pack()
        #self.get_blankList.pack()
        tkinter.Button(self.frame_menu, text="เลือกไฟล์", font=("Courier", 13), command=lambda: self.onclick_seFile(), fg="yellow", bg="#999999").pack()
        tkinter.Button(self.frame_menu, text="clear", command=lambda: self.clear_alllist()).pack()
        #tkinter.Button(self.frame_menu, text="delete", command=lambda: self.delete_selectedList()).pack()
        defaultName = tkinter.StringVar()
        defaultName.set("รวมไฟล์")
        self.fileout = ttk.Entry(self.frame_menu, font=("Courier", 13), textvariable=defaultName)
        #self.fileout.pack()
        tkinter.Button(self.frame_menu , text="action", command=lambda: self.onclick_combind()).pack(pady=10, ipadx=50, padx=10)
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
