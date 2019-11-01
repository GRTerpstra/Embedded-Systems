from tkinter import *

class View():
    def __init__(self, mainModel, redraw = True):
        self.width = 100
        self.height = 100

        self.mainModel = mainModel
        self.screen = None

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

    def getScreem(self):
        canvas = Canvas()

        return canvas