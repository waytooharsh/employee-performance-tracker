from tkinter import *
from tkinter import ttk
from typing import DefaultDict
import connectdb
from time import strftime

user_db=connectdb.connect()

querycur = user_db.cursor(buffered=True)
schema = ('id', 'name', 'hours', 'minutes')

def fetchData(userList):
    uid = searchBar.get()
    sql = "SELECT \
        perfdata.uid, userlogin.name, perfdata.uphrs, perfdata.upmins FROM \
        perfdata \
        JOIN userlogin ON perfdata.uid=userlogin.id \
        WHERE uid=%s"
    querycur.execute(sql,(uid,))
    res = querycur.fetchone()
    print('Fetched')
    for record in userList.get_children():
        userList.delete(record)
    userList.insert("", END, values=res)    

mainWin = Tk(className='Employee Monitor')
mainWin.state("zoomed")
mainWin['background'] = "#262626"


headLabel = Label(mainWin, text = "Employee Performance Monitor", bg="black" ,fg="white", font="Helvetica 32 bold")
headLabel.config(anchor=CENTER)
headLabel.pack()
'''
loginFrame = Frame(mainWin, bg="#8C93A8", width=600, height=250)  
loginFrame.pack(pady=50) 
global idEntry
global passEntry
Label(loginFrame, text = "LOGIN", bg="black" ,fg="white", font="Helvetica 20 bold").grid(row=0, column=0, columnspan=2, ipadx = 50,padx=10, pady=10)
Label(loginFrame, text = "Enter your login details..", bg="#8C93A8", fg="black", font="Helvetica 14").grid(row=1, column=0, sticky='w')
Label(loginFrame, text = "User ID:", bg="#8C93A8", fg="white", font="Helvetica 16").grid(row=2, column=0, sticky='w', padx=10, pady=7)
idEntry = Entry(loginFrame, font="Helvetica 16")

idEntry.grid(row=2, column=1, sticky='w', padx=10, pady=7)
#Password Entry
Label(loginFrame, text = "Password:", bg="#8C93A8", fg="white", font="Helvetica 16").grid(row=3, column=0, sticky='w', padx=10, pady=7)
passEntry = Entry(loginFrame,font="Helvetica 16", show='*')
passEntry.grid(row=3, column=1, sticky='w', padx=10, pady=7)
#Submit Button
Button(loginFrame, text="Login", fg="black",font="Helvetica 15 bold", command=login, height =1, width=10).grid(row=4, column=0, columnspan=2, padx=10, pady=7)

# ADMIN FRAME
global searchBar
global records
adminFrame = Frame(mainWin, bg="#8C93A8", width=1000, height=700)

newUser = Frame(adminFrame, bg='#111111', width = 400, height=400)
newUser.grid(row=2, column=0,padx=20, pady=20)
newUser.grid_propagate(0)
Label(newUser, text='ADD NEW USER', fg="white", bg='#111111',font="Helvetica 20 bold").grid(row=0, column=0, columnspan=2, padx=10, pady=5)
Label(newUser, text='Username:', fg="white", bg='#111111',font="Helvetica 16").grid(row=3, column=0, padx=10, pady=10,sticky='w')
newID = Entry(newUser, font="Helvetica 16")
newID.grid(row=3, column=1,sticky='w', padx=10, pady=10)
Label(newUser, text='Password:', fg="white", bg='#111111',font="Helvetica 16").grid(row=4, column=0, padx=10, pady=10,sticky='w')
newPass = Entry(newUser, font="Helvetica 16")
newPass.grid(row=4, column=1,sticky='w', padx=10, pady=10)
Label(newUser, text='Full Name:', fg="white", bg='#111111',font="Helvetica 16").grid(row=5, column=0, padx=10, pady=10,sticky='w')
newName = Entry(newUser, font="Helvetica 16")
newName.grid(row=5, column=1,sticky='w', padx=10, pady=10)
menu = StringVar()
menu.set('Select Role')
newRole = OptionMenu(newUser, menu,"Admin", "User")
newRole.config(width=20, font="Helvetica 12")
newRole.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
Button(newUser, text="Submit", fg="black",font="Helvetica 15 bold", command=None, height =1, width=10).grid(row=9, column=0, columnspan=2, padx=10, pady=10)
Button(newUser, text="Stop", fg="black",font="Helvetica 15 bold", command=None, height =1, width=10).grid(row=10, column=0, columnspan=2, padx=1, pady=1)

showStats = Frame(adminFrame, bg='#111111', width = 600, height=600)
showStats.grid(row=2, column=1,padx=20, pady=20)
statsHead = Frame(showStats, bg='black', width=550, height=100)
statsHead.grid(row=0, column=0, columnspan=2,padx=10, pady=10)
Label(statsHead, text='SHOW EMPLOYEE STATS', fg="white", bg='#111111',font="Helvetica 20 bold").grid(row=0, column=0, columnspan=3, padx=10, pady=5)
Label(statsHead, text='Search User:', fg="white", bg='#111111',font="Helvetica 16").grid(row=3, column=0, padx=10, pady=10,sticky='w')
searchBar = Entry(statsHead, font="Helvetica 16")
searchBar.grid(row=3, column=1,sticky='w', padx=10, pady=10)
Button(statsHead, text='Search',fg="black",font="Helvetica 15 bold", command=lambda: fetchData(userList), width=8).grid(row=3, column=2, pady=4, padx=10)


tableView = Frame(showStats,bg='#111111', width = 600, height=600)
tableView.grid(row=8, column=0,padx=20, pady=20)
userList=ttk.Treeview(tableView, column=schema)

userList.heading("id", text="User ID")
userList.heading("name", text="User Name")
userList.heading("hours", text="Hours")
userList.heading("minutes", text="Minutes")
userList['show'] = "headings"
userList.grid(row=8, column=0)

adminFrame.pack(pady=50)
adminFrame.pack_propagate(0)

records = table(schema)
records.showTable()
        

def showFrame(frame):
    frame.pack(pady=50)
    frame.pack_propagate(0)
    frame.tkraise()
    
'''

userFrame = Frame(mainWin, bg="#8C93A8", width=1000, height=700)
Label(userFrame, text="CURRENT TIME", bg ="#111111", fg="white", font="Helvetica 20 bold", width=20, height=2).grid(row=0, column=0, columnspan=2,padx=20, pady=20)
timeLabel = Label(userFrame, font = ('Helvetica', 30, 'bold'), background = '#111111',foreground = 'white', width=30)
Label(userFrame, text="YOU ARE LOGGED ON\nYOUR PERFORMANCE IS BEING MONITORED", bg ="#111111", fg="white", font="Helvetica 20 bold", width=40, height=2).grid(row=20, column=0, columnspan=2,padx=20, pady=20)
def time():
    string = strftime('%H:%M:%S %p')
    timeLabel.config(text = string)
    timeLabel.after(1000, time)
    timeLabel.grid(row=10, column=0, columnspan=2)
time()


userFrame.pack(pady=50)
userFrame.propagate(0)
mainWin.mainloop()