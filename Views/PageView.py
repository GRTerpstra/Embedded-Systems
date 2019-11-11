from Views.View import View
from tkinter import *
from Models.MenuModel import PageType

class PageView(View):
    def __init__(self, mainModel, redraw = True):
        super().__init__(mainModel, redraw)

        return

    def getScreen(self):
        canvas = super().getScreen()

        #canvas.create_rectangle(0, 0, 100, 100, fill='yellow')

        self.canvas = canvas

        return canvas