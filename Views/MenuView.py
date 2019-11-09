from Views.View import View
from tkinter import *
from GUISettings import GUISettings
from functools import partial

class MenuView(View):
    def __init__(self, mainModel, menuModel, redraw = True):
        super().__init__(mainModel, redraw)

        self.offsetX = 0
        self.offsetY = 0

        self.bgColor = GUISettings.menuBgColor

        self.borderWidth = GUISettings.menuBorderWidth
        self.borderHeight = GUISettings.menuBorderHeight

        self.height = GUISettings.menuHeight
        self.width = GUISettings.mainWidth

        self.menuModel = menuModel

        self.show = True

        return

    def getScreen(self):
        canvas = Canvas(self.mainModel.mainRoot, height=self.height, width=self.width, highlightthickness=0, bd=0)

        self.drawFrame(canvas, 0, 0, self.width, self.height, self.bgColor, self.borderColor, self.borderWidth,
                       self.borderHeight, self.shadowColor, self.shadowWidth, self.shadowHeight)

        #create buttons
        if len(self.menuModel.pageTypes) > 0:
            margin =  0
            index = 0

            navbar = Canvas(canvas, width=500, height=50)

            # create buttons
            if len(self.menuModel.pageTypes) > 0:
                index = 0

                for name, title in self.menuModel.pageTypes.items():
                    button = Button(navbar, text=title, command=partial(self.menuModel.switchPage, name), height=2)
                    button.configure(background=GUISettings.menuBgColor, activebackground="#33B5E5", relief=FLAT)
                    button.grid(column=index, row=0)
                    margin += button.winfo_width()
                    print(button.winfo_width())
                    index += 1

            navbar.pack(fill="both", expand=1)

        return canvas