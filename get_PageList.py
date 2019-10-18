import pdfrw
import tkinter
import tkinter.filedialog

inp = ""
def file_chooser():
    global inp
    inp = tkinter.filedialog.askopenfilename()   
    return inp
def get_listIndex(read):
    list_index = []
    for i in range(len(read.pages)):
        if read.pages[i].krit == "(index_insert)":
            list_index.append(str(i+1)+"-"+str(i+2))
    return list_index
def show_list(page_list):
    global wid_out
    text_list = tkinter.StringVar()
    text_list.set(",".join(page_list))
    wid_out.config(textvariable=text_list)
    
root = tkinter.Tk()
root.title("get_PageList")
tkinter.Button(root, text="file", command=file_chooser).pack()
wid_out = tkinter.Entry(root, width=100)
wid_out.pack()
tkinter.Button(root, text="get index", command=lambda: show_list(get_listIndex(pdfrw.PdfFileReader(inp)))).pack()
root.mainloop()
