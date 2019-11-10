from tkinter import *
from enum import Enum
from GUISettings import GUISettings
import serial
import time

class MainModel():
    def __init__(self):
        self.views = []
        self.frames = dict()
        self.settings = GUISettings

        # create main frame/canvas
        mainRoot = Tk()
        mainRoot.overrideredirect(True)
        mainRoot.attributes('-topmost', True)

        bgRoot = Toplevel(mainRoot)
        bgRoot.wm_attributes('-alpha', 0.3)
        bgRoot.wm_attributes("-fullscreen", True)
        bgRoot.overrideredirect(True)
        bgRoot.attributes('-topmost', False)

        backRoot = Toplevel(mainRoot)
        backRoot.overrideredirect(True)
        backRoot.attributes('-topmost', True)

        #store screen width
        self.screenWidth = mainRoot.winfo_screenwidth()
        self.screenHeight = mainRoot.winfo_screenheight()

        # Gets both half the screen width/height and window width/height
        centerX = int(self.screenWidth / 2 - self.settings.mainWidth / 2)
        centerY = int(self.screenHeight / 2 - self.settings.mainHeight / 2)

        # set start position and margin
        mainRoot.geometry('{}x{}+{}+{}'.format(self.settings.mainWidth, self.settings.mainHeight, centerX, centerY))
        backRoot.geometry('{}x{}+{}+{}'.format(self.settings.closeWidth, self.settings.closeHeight, centerX + self.settings.mainWidth - int(self.settings.closeWidth / 2), centerY - int(self.settings.closeHeight / 2)))

        mainFrame = Frame(mainRoot, width=self.settings.mainWidth, height=self.settings.mainHeight, bg=self.settings.mainBgColor)
        closeFrame = Frame(backRoot, width=self.settings.closeWidth, height=self.settings.closeHeight)

        self.mainRoot = mainRoot
        self.bgRoot = bgRoot
        self.backRoot = closeFrame
        self.closeFrame = closeFrame
        self.mainFrame = mainFrame

        return

    def start(self):
        #show frames
        self.mainFrame.pack()
        self.closeFrame.pack()

        # show frame
        self.mainRoot.after(10, self.update)
        self.mainRoot.mainloop()

    def update(self):
        self.updateViews()
        self.mainRoot.after(self.settings.updateTime, self.update)

        #self.conn.write(str(0).encode())

        #inf = ""
        #data = self.conn.readline()

        #for char in data:
            # char = char.decode('ascii')
            #print('char: ' + str(chr(char)))

            #inf += str(char)

        #print("The Arduino says:")
        #print(inf)

        #self.test = ((self.test + 1) % 2)

        return

    def addView(self, view):
        if view is None or view in self.views:
            return

        self.views.append(view)

    def updateViews(self):
        if len(self.views) == 0:
            return

        for view in self.views:
            if view not in self.frames:
                if(view.show is False):
                    continue

                frame = view.getCanvas(False)
                frame.pack()

                frame.place(x=view.offsetX, y=view.offsetY)

                self.frames[view] = frame

            view.update()

    def removeView(self, view):
        if view is None or view not in self.views:
            return

        if self.frames[view] is not None:
            frame = self.frames[view]

        self.views.remove(view)

    def close(self):
        self.mainRoot.destroy()

        return

class PageType(Enum):
    HOME = 0
    LIGHT = 1
    TEMPERATURE = 2