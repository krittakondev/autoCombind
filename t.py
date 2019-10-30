import tkinter as tk

def handle_focus(event):
    if event.widget == root:
        print("I have gained the focus")

root = tk.Tk()
entry1 = tk.Entry(root)
entry2 = tk.Entry(root)

entry1.pack()
entry2.pack()

entry1.bind("<FocusIn>", handle_focus)

root.mainloop()
