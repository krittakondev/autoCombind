import tkinter

root = tkinter.Tk()


c = tkinter.IntVar()
check = tkinter.Checkbutton(root, text="testing",variable=c, command=lambda: print(c.get()))
check.pack()

root.mainloop()
