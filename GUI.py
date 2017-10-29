from Tkinter import *
import os


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        self.choose_mode

    # Creation of init_window
    def init_window(self):
        global choose_mode
        global alert_type
        global slider

        # changing the title of our master widget
        self.master.title("Driver Attention Detector")
        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)
        # creating a button instance
        quitButton = Button(self, text="Quit", fg="red", command=quit).place(x=175, y=350)
        goButton = Button(self, text="Activate Detection",
                          command=self.activate).place(x=100, y=235, height=100, width=220)
        Label(self, text="Choose Mode:").place(x=40, y=15)
        Label(self, text="Time Threshold (seconds):").place(x=225, y=82)
        self.choose_mode = StringVar()
        self.alert_type = StringVar()
        self.slider = StringVar()
        Radiobutton(root,
                    text="View Analysis",
                    padx=0,
                    variable=self.choose_mode,
                    value="view", cursor="dot").place(x=34, y=75)
        Radiobutton(root,
                    text="Stealth Mode (Background)",
                    padx=0,
                    variable=self.choose_mode,
                    value="stealth", cursor="dot").place(x=34, y=45)

        Label(self, text="Choose Alert Sound:").place(x=40, y=105)

        Radiobutton(root,
                    text="Classic Yishy Harel Sound",
                    padx=0,
                    variable=self.alert_type,
                    value="yishy", cursor="dot").place(x=34, y=135)
        Radiobutton(root,
                    text="Wake Up to Rock'N'Roll",
                    padx=0,
                    variable=self.alert_type,
                    value="rock", cursor="dot").place(x=34, y=165)
        Radiobutton(root,
                    text="Let Mozart Shake Me Up",
                    padx=0,
                    variable=self.alert_type,
                    value="mozart", cursor="dot").place(x=34, y=195)

        Scale(root, from_=1, to=4, orient=HORIZONTAL, variable=self.slider).place(x=250, y=100)
        #choose default values:
        self.slider.set(1)
        self.alert_type.set("rock")
        self.choose_mode.set("view")

    def activate(self):
        root.destroy()
        os.system("main.py" + " " + self.choose_mode.get() +
                  " " + self.alert_type.get() + " " + self.slider.get())
        quit(self)


root = Tk()
# size of the window
root.geometry("400x400")
# print choose_mode.get()
app = Window(root)
root.mainloop()
