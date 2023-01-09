import mysql.connector
import hashlib
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from time import strftime
import connectdb
import uptime

#Class to hold details of logged-in user
class activeUser:
    privilege = None
    uid = None
    name = None
    def __init__(self,uid, name, privilege):
        self.privilege = privilege
        self.uid = uid
        self.name = name
    def getuser(self):
        return self.uid

schema = ('id', 'name', 'hours', 'minutes')

user_db=connectdb.connect()
querycur = user_db.cursor(buffered=True)

#Function to Add new Employee to the Database
def createUser():
    uid = newID.get()
    name = newName.get()
    role = menu.get()
    pwd = newPass.get()
    password = hashlib.md5(bytes(pwd, 'utf-8')).hexdigest()
    if role=="Admin":
        role=0
    elif role=='User':
        role=1

    sql = "INSERT INTO userlogin (role, id, pass, name) VALUES (%s, %s, %s, %s)"
    val = (role, uid, password, name)
    querycur.execute(sql,val)
    user_db.commit()
    
    sql = "INSERT INTO perfdata(uid, uphrs, upmins) VALUES (%s, %s, %s)"
    val = (uid, '0', '0')
    querycur.execute(sql,val)
    user_db.commit()
    messagebox.showinfo('Success','User Created Successfully')

#Current Time Pumping function
def time():
    string = strftime('%H:%M:%S %p')
    timeLabel.config(text = string)
    timeLabel.after(1000, time)
    timeLabel.grid(row=10, column=0, columnspan=2)

#LOGIN FUNCTION: Uses MySQL databse for validating user ID and password
def login():
    uid = idEntry.get()
    pwd = passEntry.get()
    
    password = hashlib.md5(bytes(pwd, 'utf-8')).hexdigest() 
    querycur.execute("SELECT pass,name,role FROM userlogin WHERE id= %s", (uid, ))
    res = querycur.fetchone()

    if res[0] == password:
        loginFrame.destroy()
        userObj = activeUser(uid,res[1], res[2])
        curr_user = userObj
        if curr_user.privilege == 0: #Use Admin Frame
            showFrame(adminFrame)
        if curr_user.privilege == 1: #Use User Frame
            showFrame(userFrame)
            time()
        welcomeTxt = 'Login Successful!\nWELCOME ' + res[1]
        messagebox.showinfo('Success',welcomeTxt)
        initiate(curr_user)
    else:
        messagebox.showinfo('Alert','Invalid Credentials! Please Try Again...')

#Function to fetch data from SQL about employees and Display in GUI
def fetchData(userList):
    uid = searchBar.get()
    sql = "SELECT \
        perfdata.uid, userlogin.name, perfdata.uphrs, perfdata.upmins FROM \
        perfdata \
        JOIN userlogin ON perfdata.uid=userlogin.id \
        WHERE uid=%s"
    querycur.execute(sql,(uid,))
    user_db.commit()
    res = querycur.fetchone()

    for record in userList.get_children():
        userList.delete(record)
    userList.insert("", END, values=res)

def showAll(userList):
    sql = "SELECT \
        perfdata.uid, userlogin.name, perfdata.uphrs, perfdata.upmins FROM \
        perfdata \
        JOIN userlogin ON perfdata.uid=userlogin.id"
    querycur.execute(sql)
    user_db.commit()
    res = querycur.fetchall()
    for record in userList.get_children():
        userList.delete(record)
    for each in res:
        userList.insert("", END, values=each)

#Activate Login session
def initiate(user):
    uptime.activeStatus=1
    uptime.startSession(user)

#Graphical User Interface...

mainWin = Tk(className='Employee Monitor')
mainWin.state("zoomed")
mainWin['background'] = "#262626"

#WELCOME SCREEN
headLabel = Label(mainWin, text = "Employee Performance Monitor", bg="black" ,fg="white", font="Helvetica 32 bold")
headLabel.config(anchor=CENTER)
headLabel.pack()

loginFrame = Frame(mainWin, bg="#8C93A8", width=600, height=250)  
loginFrame.pack(pady=50)

Label(loginFrame, text = "LOGIN", bg="black" ,fg="white", font="Helvetica 20 bold").grid(row=0, column=0, columnspan=2, ipadx = 50,padx=10, pady=10)
Label(loginFrame, text = "Enter your login details..", bg="#8C93A8", fg="black", font="Helvetica 14").grid(row=1, column=0, sticky='w')
#User ID entry
Label(loginFrame, text = "User ID:", bg="#8C93A8", fg="white", font="Helvetica 16").grid(row=2, column=0, sticky='w', padx=10, pady=7)
idEntry = Entry(loginFrame, font="Helvetica 16")

idEntry.grid(row=2, column=1, sticky='w', padx=10, pady=7)
#Password Entry
Label(loginFrame, text = "Password:", bg="#8C93A8", fg="white", font="Helvetica 16").grid(row=3, column=0, sticky='w', padx=10, pady=7)
passEntry = Entry(loginFrame,font="Helvetica 16", show='*')
passEntry.grid(row=3, column=1, sticky='w', padx=10, pady=7)
#Submit Button
Button(loginFrame, text="Login", fg="black",font="Helvetica 15 bold", command=login, height =1, width=10).grid(row=4, column=0, columnspan=2, padx=10, pady=7)

'''
===========================ADMIN FRAME============================
'''
global searchBar
global records
#HEADER TELLING THAT ADMIN IS BEING MONITORED
adminFrame = Frame(mainWin, bg="#8C93A8", width=1000, height=700)
adminAlert = Frame(adminFrame,bg="#8C93A8")
Label(adminAlert, text="YOU ARE LOGGED ON\nYOUR PERFORMANCE IS BEING MONITORED", bg ="#111111", fg="white", font="Helvetica 20 bold", width=40, height=2).grid(row=20, column=0, columnspan=2,padx=20, pady=20)
adminAlert.grid(row=0,column=0, columnspan=2)

#New User Creation Frame
newUser = Frame(adminFrame, bg='#111111', width = 400, height=400)
newUser.grid(row=2, column=0,padx=20, pady=20)
newUser.grid_propagate(0)

Label(newUser, text='ADD NEW USER', fg="white", bg='#111111',font="Helvetica 20 bold").grid(row=0, column=0, columnspan=2, padx=10, pady=5)

#ID ENTRY...
Label(newUser, text='Username:', fg="white", bg='#111111',font="Helvetica 16").grid(row=3, column=0, padx=10, pady=10,sticky='w')
newID = Entry(newUser, font="Helvetica 16")
newID.grid(row=3, column=1,sticky='w', padx=10, pady=10)

#PASSWORD ENTRY
Label(newUser, text='Password:', fg="white", bg='#111111',font="Helvetica 16").grid(row=4, column=0, padx=10, pady=10,sticky='w')
newPass = Entry(newUser, font="Helvetica 16")
newPass.grid(row=4, column=1,sticky='w', padx=10, pady=10)

#FULL NAME ENTRY
Label(newUser, text='Full Name:', fg="white", bg='#111111',font="Helvetica 16").grid(row=5, column=0, padx=10, pady=10,sticky='w')
newName = Entry(newUser, font="Helvetica 16")
newName.grid(row=5, column=1,sticky='w', padx=10, pady=10)

#ROLE SELECTION (ADMIN OR USER)
menu = StringVar()
menu.set('Select Role')
newRole = OptionMenu(newUser, menu,"Admin", "User")
newRole.config(width=20, font="Helvetica 12")
newRole.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

#SUBMIT BUTTON
Button(newUser, text="Submit", fg="black",font="Helvetica 15 bold", command=createUser, height =1, width=10).grid(row=9, column=0, columnspan=2, padx=10, pady=20)

#EMPLOYEE STATS VIEWING FRAME
showStats = Frame(adminFrame, bg='#111111', width = 600, height=600)
showStats.grid(row=2, column=1,padx=20, pady=20)
statsHead = Frame(showStats, bg='black', width=550, height=100)
statsHead.grid(row=0, column=0, columnspan=2,padx=10, pady=10)

#HEADER
Label(statsHead, text='SHOW EMPLOYEE STATS', fg="white", bg='#111111',font="Helvetica 20 bold").grid(row=0, column=0, columnspan=3, padx=10, pady=5)
Label(statsHead, text='Search User:', fg="white", bg='#111111',font="Helvetica 16").grid(row=3, column=0, padx=10, pady=10,sticky='w')

#SEARCH BAR
searchBar = Entry(statsHead, font="Helvetica 16")
searchBar.grid(row=3, column=1,sticky='w', padx=10, pady=10)

#SEARCH BUTTON
Button(statsHead, text='Search',fg="black",font="Helvetica 15 bold", command=lambda: fetchData(userList), width=8).grid(row=3, column=2, pady=4, padx=10)
#BUTTON TO SHOW ALL EMPLOYEES' RECORDS IN DATABASE
Button(statsHead, text='Show All',fg="black",font="Helvetica 15 bold", command=lambda: showAll(userList), width=20).grid(row=4, column=0, columnspan=3, pady=10, padx=10)

#DATABASE TABLE VIEWER
tableView = Frame(showStats,bg='#111111', width = 600, height=600)
tableView.grid(row=8, column=0,padx=20, pady=20)
userList=ttk.Treeview(tableView, column=schema)

userList.heading("id", text="User ID")
userList.heading("name", text="User Name")
userList.heading("hours", text="Hours")
userList.heading("minutes", text="Minutes")
userList['show'] = "headings"
userList.grid(row=8, column=0)

'''
==============USER FRAME============
'''

userFrame = Frame(mainWin, bg="#8C93A8", width=1000, height=700)

#CLOCK
Label(userFrame, text="CURRENT TIME", bg ="#111111", fg="white", font="Helvetica 20 bold", width=20, height=2).grid(row=0, column=0, columnspan=2,padx=20, pady=20)
timeLabel = Label(userFrame, font = ('Helvetica', 30, 'bold'), background = '#111111',foreground = 'white', width=30)

#ALERT MESSAGE
Label(userFrame, text="YOU ARE LOGGED ON\nYOUR PERFORMANCE IS BEING MONITORED", bg ="#111111", fg="white", font="Helvetica 20 bold", width=40, height=2).grid(row=20, column=0, columnspan=2,padx=20, pady=20)

#FUNCTION TO LOGOUT AND EXIT (INVOKED ON PRESSING CLOSE BUTTON)
def logout():
    if messagebox.askokcancel("Alert","Do you want to Logout and Exit?"):
        uptime.activeStatus=1
        connectdb.disconnect(user_db)
        connectdb.disconnect(uptime.user_db)
        mainWin.destroy()

mainWin.protocol("WM_DELETE_WINDOW", logout)

#FUNCTION TO CHANGE FRAMES IN GUI WINDOW
def showFrame(frame):
    frame.pack(pady=50)
    frame.pack_propagate(0)
    frame.tkraise()

#STARTS AND HOLDS GUI WINDOW ON SCREEN
mainWin.mainloop()