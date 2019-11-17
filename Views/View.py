from tkinter import *
from GUISettings import GUISettings
import math

class View:
    def __init__(self, mainModel, redraw = True):
        #size
        self.width = 100
        self.height = 100

        #position (offset)
        self.offsetX = 0
        self.offsetY = 0

        #background
        self.bgColor = GUISettings.mainBgColor

        #border
        self.borderWidth = 0
        self.borderHeight = 0
        self.borderColor = "black"

        #shadow
        self.shadowWidth = 0
        self.shadowHeight = 0
        self.shadowColor = NONE

        self.mainModel = mainModel
        self.screen = None

        self.show = False
        self.updateNeeded = True

        self.canvas = None

        super().__init__()

        self.mainModel.addView(self)

        return

    def update(self, reset = False):
        if(reset):
            self.screen = self.getScreem()

        self.updateNeeded = False

    def getCanvas(self, reset = False):
        if(self.screen == None or reset):
            return self.getScreen()

        return self.screen

    def getScreen(self):
        canvas = Canvas(self.mainModel.mainFrame, width=self.width, height=self.height, highlightthickness=0)

        self.drawFrame(canvas, 0, 0, self.width, self.height, self.bgColor, self.borderColor, self.borderWidth, self.borderHeight)

        self.canvas = canvas

        return canvas

    def drawFrame(self, canvas, x, y, width, height, color, borderColor = NONE, borderWidth = 0, borderHeight = 0, shadowColor = NONE, shadowWidth = 0, shadowHeight = 0):
        if canvas is NONE:
            return

        if borderHeight > 0 or borderWidth > 0:
            canvas.create_rectangle(x, y, x + width, y + height, fill=borderColor, outline=borderColor, width=0)

        if shadowHeight > 0 or shadowWidth > 0:
            canvas.create_rectangle(x + borderWidth, y + borderHeight, x + width - borderWidth, y + height - borderHeight, fill=shadowColor, outline=shadowColor, width=0)

        canvas.create_rectangle(x + borderWidth + shadowWidth, y + borderHeight + shadowHeight, x + width - borderWidth - shadowWidth, y + height - borderHeight - shadowHeight, fill=color, outline=color, width=0)

        return

    def drawTab(self, canvas, x, y, width, height, stat, color):
        tab = Canvas(canvas, height=GUISettings.tabHeight, width=width, highlightthickness=0, bd=0,
                     bg=GUISettings.tabBorderColor)

        tab.create_rectangle(GUISettings.tabBorderWidth, GUISettings.tabBorderHeight,
                             width - GUISettings.tabBorderWidth,
                             GUISettings.tabTitleHeight - GUISettings.tabBorderHeight, fill=GUISettings.tabTitleBgColor,
                             width=0)
        tab.create_rectangle(GUISettings.tabBorderWidth, GUISettings.tabTitleHeight,
                             width - GUISettings.tabBorderWidth, GUISettings.tabHeight - GUISettings.tabBorderHeight,
                             fill=GUISettings.tabBgColor, width=0)
        title = Label(tab, text=str.upper(stat.title), justify="left", font=(GUISettings.tabTitleFont), fg="white",
                      bg=GUISettings.tabTitleBgColor, bd=0)

        value = Label(tab, text=str(0), justify="left", font=GUISettings.tabLabelFont, fg=color,
                      bg=GUISettings.tabBgColor, bd=0, highlightthickness=0)

        title.place(x=GUISettings.tabTitlePaddingX, y=GUISettings.tabBorderHeight + GUISettings.tabTitlePaddingY)
        value.place(x=GUISettings.tabBorderWidth, y=GUISettings.tabLabelPaddingY, relx = 0.5, rely = 0.5, anchor = CENTER)
        tab.place(x=x, y=y)

        return value

    def drawSetting(self, canvas, x, y, width, height, setting):
        #print(setting)

        return
