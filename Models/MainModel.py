from tkinter import *
from GUISettings import GUISettings
from enum import Enum

class MainModel():
    def __init__(self,):
        self.views = []
        self.frames = dict()

        # set settings
        self.settings = GUISettings

        # create main frame/canvas
        mainRoot = Tk()
        mainRoot.overrideredirect(True)

        bgRoot = Toplevel(mainRoot)
        bgRoot.wm_attributes('-alpha', 0.3)
        bgRoot.wm_attributes("-fullscreen", True)
        bgRoot.overrideredirect(True)

        # Gets both half the screen width/height and window width/height
        centerX = int(mainRoot.winfo_screenwidth() / 2 - self.settings.mainWidth / 2)
        centerY = int(mainRoot.winfo_screenheight() / 2 - self.settings.mainHeight / 2)

        # set start position and margin
        mainRoot.geometry('{}x{}+{}+{}'.format(self.settings.mainWidth, self.settings.mainHeight, centerX, centerY))

        mainFrame = Frame(mainRoot, width=self.settings.mainWidth, height=self.settings.mainHeight, bg=self.settings.mainBgColor)

        self.mainRoot = mainRoot
        self.bgRoot = bgRoot
        self.mainFrame = mainFrame

        return

    def start(self):
        self.mainFrame.pack()
        self.mainRoot.mainloop()

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
                print("add frame!")

            view.update()

    def removeView(self, view):
        if view is None or view not in self.views:
            return

        if self.frames[view] is not None:
            frame = self.frames[view]

        self.views.remove(view)

class PageType(Enum):
    HOME = 0
    LIGHT = 1
    TEMPERATURE = 2