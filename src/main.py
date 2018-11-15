import requests
import json
import time
import tkinter as tk


from tkinter import *
########### API Functions - data fetching from api.warframestat.us
def fetchTimer():
    response = requests.get("https://api.warframestat.us/pc/cetusCycle") #get my data to display
    data =response.json()
    # some formatting to do
    retarray =[] # order of isDay, time left, and shortstring (0, 1, 2)
    if data['isDay']:
        retarray.append("Day")
    else:
        retarray.append("Night")
    retarray.append(data['timeLeft'])
    retarray.append(data['shortString'])
    return retarray
def nitain():
    response = requests.get("https://api.warframestat.us/pc/alerts")
    data = response.json()
    for element in data:
        temp = element["mission"]
        rewards = temp["reward"]
        if "Nitain" in rewards["asString"]:
            return True
    return False

def baro():
    response = requests.get("https://api.warframestat.us/pc/voidTrader") #get my data to display
    data =response.json()
    #startString, active, location, endstring
    retarray=[]
    retarray.append(data["active"])
    retarray.append(data["startString"].rsplit(' ', 1)[0])

    retarray.append(data["location"])
    retarray.append(data["endString"].rsplit(' ', 1)[0])
    return retarray

def alerts():
    response = requests.get("https://api.warframestat.us/pc/alerts") #get my data to display
    data =response.json()
    #mission, eta
    retarray=[]

    for x in data:
        temp =[]
        #strip away information we dont want
        missiondict = x["mission"]

        if "Blueprint" in missiondict["reward"]["asString"]:
            missiondict["reward"]["asString"] = missiondict["reward"]["asString"].replace("Blueprint", "BP")
            # shorten the blueprint word to BP to save space
        temp.append(missiondict["reward"]["asString"])
        temp.append(x["eta"].rsplit(' ', 1)[0]) #time left in this alert
        temp.append(missiondict["nightmare"])
        temp.append(missiondict["node"])
        temp.append(missiondict["type"])
        temp.append(missiondict["minEnemyLevel"])
        temp.append(missiondict["maxEnemyLevel"])
        retarray.append(temp)
    return retarray
###########

### TKINTER THINGS
class App(tk.Tk):
    def __init__(self):

        self.root = tk.Tk()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self._offsetx = 0
        self._offsety = 0

        pos = self.getpos()
        self.x= int(pos[0])
        self.y= int(pos[1])
        self.root.geometry("+%d+%d" % (self.x, self.y))
        self.root.propagate(1)
        self.root.overrideredirect(1) #set window borderless
        self.root.configure(background="#2b2d31")
        self.locked= False


        ##frames for arrangement
        topframe = Frame(self.root, bg="#2b2d31", height=5, bd=1)
        topframe.pack(side=RIGHT, expand= FALSE, fill=Y)
        ephoto = tk.PhotoImage(file="img/exit.png")
        self.lphoto= tk.PhotoImage(file="img/lock.png")
        self.uphoto= tk.PhotoImage(file="img/unlock.png")
        exitbutton = Button(topframe, image=ephoto, pady=5, fg="black", bg= "#2b2d31", command=self.destroy_window, relief=FLAT)
        exitbutton.pack(side=TOP)


        self.lockbutton = Button(topframe, image=self.uphoto, pady=5, fg="black", bg= "#2b2d31", command=self.lock, relief=FLAT)
        self.lockbutton.pack(side=TOP)

        topframe.bind('<ButtonPress-1>', self.clickwin)
        topframe.bind('<B1-Motion>', self.dragwin)
        tframe=Frame(self.root, bg="#2b2d31")
        tframe.pack(fill=X)
        mainframe=Frame(self.root, bg="#36393e")
        mainframe.pack(fill=X)
        cframe=Frame(mainframe, bg="#36393e", padx=10)
        cframe.pack()
        atframe = Frame(mainframe, bg="#2b2d31")
        atframe.pack(fill=X)
        self.aframe=Frame(mainframe, bg="#36393e")
        self.aframe.pack(fill=X)
        btframe = Frame(mainframe, bg="#2b2d31")
        btframe.pack(fill=X)
        self.bframe = Frame(mainframe, bg="#36393e")
        self.bframe.pack()


        ### CETUS CYCLE LABELS
        self.title = tk.Label(tframe,text="Cetus Cycle", font=("Helvetica", 12), bg="#2b2d31", fg="white", padx=2)
        self.title.pack(side=LEFT)

        self.cycle = tk.Label(cframe,text="It is currently", font=("Helvetica", 10), bg="#36393e", fg="white")
        self.cycle.pack(side=LEFT)

        self.tod = tk.Label(cframe,text="", font=("Helvetica", 10), bg="#36393e", fg="white")
        self.tod.pack(side=LEFT)

        self.withtext = tk.Label(cframe,text="with", font=("Helvetica", 10), bg="#36393e", fg="white")
        self.withtext.pack(side=LEFT)

        self.timer = tk.Label(cframe,text="", font=("Helvetica", 10),bg="#36393e", fg="white")
        self.timer.pack(side=LEFT)
        ### CETUS CYCLE LABELS END

        ### ALERT LABELS
        self.atitle = tk.Label(atframe,text="Alerts", font=("Helvetica", 12), bg="#2b2d31", fg="white", padx=2)
        self.atitle.pack(side=LEFT)
        ## ALERT LABELS END

        # BARO LABELS
        self.btitle = tk.Label(btframe,text="Baro Ki'Teer", font=("Helvetica", 12), bg="#2b2d31", fg="white", padx=2)
        self.btitle.pack(side=LEFT)
        self.update_clock()
        self.root.mainloop()

    def update_clock(self):
        self.root.geometry('+%d+%d' % (self.x, self.y))
        data = fetchTimer()
        self.tod.configure(text=data[0])
        if data[0] == "Day":
            self.tod.configure(fg="yellow")
            self.timer.configure(fg="cyan")
        else:
            self.tod.configure(fg="cyan")
            self.timer.configure(fg="yellow")

        self.timer.configure(text=data[2])

        barodata= baro()
        alertdata = alerts()

        #destroy old frame, create new frame
        for child in self.aframe.winfo_children():
            child.destroy()

        for child in self.bframe.winfo_children():
            child.destroy()
        for i in range(len(alertdata)):
            tleft= alertdata[i][0]
            if "Nitain" in tleft:
                cleft = "white"
            elif "BP" in tleft:
                cleft="cyan"
            elif "Endo" in tleft:
                cleft = "yellow"
            else:
                cleft = "#49FF00"

            reward=tk.Label(self.aframe, text=tleft, bg="#36393e", fg=cleft)
            reward.grid(row=i, column=0, sticky="W", padx=5)
            tright = "Time: " + alertdata[i][1]
            timer=tk.Label(self.aframe, text=tright, bg="#36393e", fg="white")
            timer.grid(row=i, column=1, sticky="E", padx=5)

        if not barodata[0]: ##baro not here :(
            temp = "Arriving in " + barodata[1] + " at " + barodata[2]
            tk.Label(self.bframe, text=temp,bg="#36393e", fg="white").pack()
        else:
            temp= "Currently at " + barodata[2] + " for " + barodata[3]
            tk.Label(self.bframe, text=temp, bg="#36393e", fg="#49FF00").pack()

        self.root.after(60000, self.update_clock) #update every minute
    def destroy_window(self):
        #need to save settings here
        self.savepos(self.root.winfo_x(),self.root.winfo_y())
        self.root.destroy()
    def lock(self): #function for switching the lock, and image
        self.locked = not self.locked
        if self.locked:
            self.lockbutton.configure(image=self.lphoto)
        else:
            self.lockbutton.configure(image=self.uphoto)

    def savepos(self,x,y): #function for saving user's window position to settings file upon exit
        f= open("settings.ini","w+")
        f.write("+%d+%d" % (x,y))
        f.close()

    def getpos(self): #function for loading users saved window pos
        try:
            f= open("settings.ini","r")
            content = f.read()
            f.close()
            retarray = content.split('+')
            retarray.pop(0)
            return retarray
        except: #no settings exist, return 100 100 as placeholder
            return [100,100]

    def dragwin(self,event):
        x = self.root.winfo_pointerx() - self._offsetx
        y = self.root.winfo_pointery() - self._offsety
        if not self.locked:
            self.root.geometry('+{x}+{y}'.format(x=x,y=y))

    def clickwin(self,event):
        self._offsetx = event.x + self.root.winfo_width() -10
        self._offsety = event.y
app=App()
#tkinter things
