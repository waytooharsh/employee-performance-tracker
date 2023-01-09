import tkinter
from tkinter import messagebox
window=tkinter.Tk()
window.geometry("700x400")
def pr(x):
    print(option_Menu)
    print(x)
options = ("a","b","c")

option_Menu = tkinter.StringVar(window)
menu = tkinter.OptionMenu(window,option_Menu, *options, command=pr)
menu.grid(row=2,column=2)
option_Menu.set(2)
selection=option_Menu.get()

print(selection)

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        print('Destroy Called')
        window.destroy()


window.protocol("WM_DELETE_WINDOW", on_closing)
tkinter.mainloop()