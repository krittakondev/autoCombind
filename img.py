import tkinter

root = tkinter.Tk()
img = tkinter.PhotoImage(file="down.png")
img = img.subsample(25,25)
tkinter.Label(root, image=img).pack()
root.mainloop()
