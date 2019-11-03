from Views.View import View
from tkinter import *
from GUISettings import GUISettings
from functools import partial

class MenuView(View):
    def __init__(self, mainModel, menuModel, redraw = True):
        super().__init__(mainModel, redraw)

        self.offsetX = 0
        self.offsetY = 8

        self.bgColor = GUISettings.menuBgColor

        self.borderWidth = GUISettings.menuBorderWidth
        self.borderHeight = GUISettings.menuBorderHeight

        self.height = GUISettings.menuHeight
        self.width = GUISettings.mainWidth

        self.menuModel = menuModel

        self.show = True

        return

    def getScreen(self):
        canvas = super().getScreen()

        canvas.create_rectangle(self.borderWidth, self.borderHeight, self.width - self.borderWidth*2, self.borderHeight+2, width=0, fill=GUISettings.menuShadowColor, outline=GUISettings.menuShadowColor)
        canvas.create_rectangle(self.borderWidth, self.height - self.borderHeight - 2, self.width - self.borderWidth*2, self.height - self.borderHeight, width=0, fill=GUISettings.menuShadowColor, outline=GUISettings.menuShadowColor)

        #create buttons
        if len(self.menuModel.pageTypes) > 0:
            for name, title in self.menuModel.pageTypes.items():
                button = Button(canvas, text = title, command = partial(self.menuModel.switchPage, name))
                button.configure(activebackground = "#33B5E5", relief = FLAT)
                window = canvas.create_window(10, 10, anchor=NW, window=button)

        return canvas