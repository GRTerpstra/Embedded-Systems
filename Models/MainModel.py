from tkinter import *
import GUISettings

class MainModel():
    def __init__(self,):
        self.views = []

        # set settings
        self.settings = GUISettings.GUISettings()

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

        mainFrame = Frame(mainRoot, width=self.settings.mainWidth, height=self.settings.mainHeight)

        self.mainRoot = mainRoot
        self.bgRoot = bgRoot
        self.mainFrame = mainFrame
        self.canvas = Canvas(mainFrame)

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
            view.update()

class PageType(Enum):
    HOME = 0
    LIGHT = 1
    TEMPERATURE = 2