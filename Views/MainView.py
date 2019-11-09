from Views.View import View
from tkinter import *
from GUISettings import GUISettings

class MainView(View):
    def __init__(self, mainModel, redraw = True):
        super().__init__(mainModel, redraw)

        self.offsetX = 0
        self.offsetY = 0

        self.borderWidth = GUISettings.mainBorderWidth
        self.borderHeight = GUISettings.mainBorderHeight

        self.width = GUISettings.mainWidth
        self.height = GUISettings.mainHeight

        self.show = True

        return

    def getScreen(self):
        canvas = super().getScreen()

        return super().getScreen()