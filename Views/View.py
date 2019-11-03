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

        if self.borderHeight > 0 or self.borderWidth > 0:
            canvas.create_rectangle(0, 0, self.width, self.height, fill=self.borderColor, outline=self.borderColor, width=0)

        canvas.create_rectangle(self.borderWidth, self.borderHeight, self.width-self.borderWidth, self.height-self.borderHeight, fill=self.bgColor, outline=self.bgColor, width=0)

        return canvas