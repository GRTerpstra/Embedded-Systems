from tkinter import *
from GUISettings import GUISettings
import math

class View():
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

        super().__init__()

        self.mainModel.addView(self)

        return

    def update(self, reset = False):
        if(reset):
            self.screen = self.getScreem()

    def getCanvas(self, reset = False):
        if(self.screen == None or reset):
            return self.getScreen()

        return self.screen

    def getScreen(self):
        canvas = Canvas(self.mainModel.mainFrame, width=self.width, height=self.height, highlightthickness=0)

        self.drawFrame(canvas, 0, 0, self.width, self.height, self.bgColor, self.borderColor, self.borderWidth, self.borderHeight)

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
