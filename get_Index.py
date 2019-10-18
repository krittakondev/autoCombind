import pdfrw
import tkinter
import tkinter.filedialog
import threading

def file_chooser():
    inp = tkinter.filedialog.askopenfilename()   
    return inp
def get_list(read):
    list_index = []
    for i in range(len(read.pages)):
        if read.pages[i].krit == "(index_insert)":
            list_index.append(str(i+1)+"-"+str(i+2))
    return list_index
root = tkinter.Tk()
root.title("getIndex")
myThread = threading.Thread(target=file_chooser)
inp = file_chooser()
list_index = get_list(pdfrw.PdfFileReader(inp))
show_text = tkinter.StringVar()
show_text.set(",".join(list_index))
text = tkinter.Entry(root, textvariable=show_text, width=100)

text.pack()
root.mainloop()
