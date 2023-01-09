from tkinter import*
from tkinter.ttk import*
from time import strftime
root = Tk()
root.title('Clock')
lbl = Label(userFrame, font = ('Helvetica', 40, 'bold'), background = '#111111',foreground = 'white')
def time():
    string = strftime('%H:%M:%S %p')
    lbl.config(text = string)
    lbl.after(1000, time)
    lbl.pack(anchor = CENTER)


time()
mainloop()
