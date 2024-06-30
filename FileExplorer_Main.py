from tkinter import messagebox
from tkinter import *
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo
import tkinter as tk
import tkinter.ttk as ttk
import os
import subprocess


Master = tk.Tk()
Master.geometry('600x400')
Master.title("File Explorer")

Style = ttk.Style(Master)
Style.configure('Treeview',
font=('bold',10))

GeneralDrives = [
    'A:/', 'B:/', 'C:/',
    'D:/', 'E:/', 'F:/',
    'G:/', 'H:/', 'I:/',
    'J:/', 'K:/', 'L:/',
    'M:/', 'N:/', 'O:/',
    'P:/', 'Q:/', 'R:/',
    'S:/', 'T:/', 'U:/',
    'V:/', 'W:/', 'X:/',
    'Y:/', 'Z:/'
]

CachedDirectory = []
AllowedDrives = []
PathBrowser = []
CurrentDrive = None

def InsertDrives():
    for i in Side.get_children(): #We clear any existing contents
        Side.delete(i)

    for r in range(len(AllowedDrives)):
        Side.insert(parent='',iid=r, text='',values=[AllowedDrives[r]], index='end') #Make new frame

def FindAllowed():
    for Drives in GeneralDrives:
        if os.path.exists(Drives): #Is there a drive named after the general drives?
            AllowedDrives.append(Drives)

    InsertDrives()

def AddFolder(FilePath):
    global CurrentDrive
    global PathBrowser
    for i in Main.get_children(): #As before clear view
        Main.delete(i)

    PathBrowser = []
   
    Folders = os.listdir(FilePath) #Main part of getting contents
    CurrentDrive = str(FilePath)
    UpdateSize()
    UpdateAdmin()
    Directory.config(text=FilePath)
    for Items in range(len(Folders)):
        Main.insert(parent='',iid=Items, text='',values=[Folders[Items]],index='end')
        PathBrowser.append(str(FilePath)+'/'+Folders[Items])
       
def GetDrive():
    Index = int(Side.selection()[0])
    Path = AllowedDrives[Index]
    AddFolder(Path)

def UpdateAdmin():
    global CurrentDrive
    Admin.config(text=('Permissions ID:', os.stat(CurrentDrive).st_uid))

def ChangeDirectory():
    global CurrentDrive
    Fetched = []
    NewDir = None
    print("No")
    print(CurrentDrive)
    if CurrentDrive != None:      
      for filename,_,_ in os.walk(str(CurrentDrive)+"."):
            Fetched.append(str(filename))
      #NewDir = Fetched[0]
      print(Fetched)
      print(NewDir)

def Insert(Path):
    global CurrentDrive
    global PathBrowser
    CurrentDrive = Path
    Directory.config(text=Path)
    UpdateSize()
    UpdateAdmin()
    try:
        for i in Main.get_children(): #As before clear view
            Main.delete(i)
        Files = os.listdir(Path)
        PathBrowser = []
        for F in range(len(Files)):
            Main.insert(parent='',iid=F,text='',index='end', values = [Files[F]])
            PathBrowser.append(str(Path)+'/'+Files[F])
    except Exception as e:
        messagebox.showerror(str(e)[:13],str(e)[13:])

def OpenSubprocess():
    #An attempt to call from subprocess in case os.system does not work
    Index = int(Main.selection()[0])
    Path = PathBrowser[Index]
    subprocess.call([Path])

def OpenStartfile():
    #A further attempt if both processes does not work
    Index = int(Main.selection()[0])
    Path = PathBrowser[Index]
    os.startfile([Path])

def UpdateSize():
    global CurrentDrive
    if CurrentDrive != None:
        Size.config(text=str(os.stat(CurrentDrive).st_size)+" Bytes")

def Open():
    Index = int(Main.selection()[0])
    Path = PathBrowser[Index]
    if os.path.isdir(Path):
        Insert(Path)
    else:
        os.system('"%s"' % Path)
   

def ExecuteEdit():
    Index = int(Edit.selection()[0])
    Option = FileOptions[Index]
    if Option == "Remove File":
        File = askstring('Files', 'What file do you want to remove? (include file format)')
        if File != None and File != "":
            showinfo('Files', 'Removed {}'.format(File))
        else:
            showinfo('Files', 'No files were removed.')
    elif Option == "Copy Directory":
        File = askstring('Files', 'What directory do you want to copy? (use directory format!)')
        if File != None and File != "":
            showinfo('Files', 'Copied {}'.format(File))
        else:
            showinfo('Files', 'No directories were copied.')
   


Task = Label(Master,bg="white")
Task.pack(side=TOP,fill=BOTH)
Reverse = Button(Task,width=4,text="Back")
Reverse.pack(side=LEFT)
Forward = Button(Task,width=4,text="Enter")
Forward.pack(side=LEFT)
CopyText = Button(Task,width=14,text="Copy Contents")
CopyText.pack(side=LEFT)
Directory = Button(Task,width=164,text=(CurrentDrive == None and "") or CurrentDrive)
Directory.pack(side=LEFT)
DeleteFile = Button(Task,width=14,text="Delete File")
DeleteFile.pack(side=LEFT)
MetaData = Button(Task,width=14,text="MetaData")
MetaData.pack(side=LEFT)
Container = Button(Master)
Container.pack(side=BOTTOM,fill=BOTH)
Size = Button(Container,text="")
Size.pack(side=LEFT)
Admin = Button(Container,text="")
Admin.pack(side=LEFT)
E = Button(Container,text="Version 2.0")
E.pack(side=LEFT)

#Drives
Side = ttk.Treeview(Master)
Side.pack(side=tk.LEFT, anchor=tk.W, fill=tk.Y)
Side['column'] = ['Drives']
Side.column('#0', anchor=tk.W, width=0, stretch=tk.NO)
Side.column('Drives', anchor=tk.W, width=100)
Side.heading('Drives', text ='Local Drives', anchor=tk.W)
Side.bind('<<TreeviewSelect>>',lambda e: GetDrive()) #Bind input to function


#Contents
Main = ttk.Treeview(Master)
Main['column'] = ['Files']
Main.column('#0', anchor=tk.W, width=0, stretch = tk.NO)
Main.column('Files', anchor=tk.W, width=500)
Main.heading('Files', text = "Contents", anchor = tk.W)
Main.bind('<<TreeviewSelect>>',lambda e: Open()) #Bind input to function

Main.pack(side=tk.LEFT, anchor=tk.W, fill=tk.Y)

#Other
Edit = ttk.Treeview(Master)
Edit['column'] = ['Options']
Edit.column('#0', anchor=tk.W, width=0, stretch = tk.NO)
Edit.column('Options', anchor=tk.W, width=1000)
Edit.heading('Options', text = "File Contents", anchor = tk.W)
Edit.bind('<<TreeviewSelect>>',lambda e: ExecuteEdit()) #Bind input to function



Edit.pack(side=tk.LEFT, anchor=tk.W, fill=tk.Y)

FindAllowed()
Master.mainloop(
