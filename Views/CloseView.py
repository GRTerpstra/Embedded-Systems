from Views.View import View
from tkinter import *
from GUISettings import GUISettings
from functools import partial

class CloseView(View):
    def __init__(self, mainModel, redraw = True):
        super().__init__(mainModel, redraw)

        self.offsetX = 0
        self.offsetY = 0

        self.height = GUISettings.closeHeight
        self.width = GUISettings.closeWidth

        self.bgColor = GUISettings.closeColor
        self.borderColor = GUISettings.closeBorderColor

        self.borderWidth = GUISettings.closeBorderWidth
        self.borderHeight = GUISettings.closeBorderHeight

        self.shadowWidth = GUISettings.closeShadowWidth
        self.shadowHeight = GUISettings.closeShadowHeight
        self.shadowColor = GUISettings.closeShadowColor

        self.show = True

        return

    def getScreen(self):
        canvas = Canvas(self.mainModel.backRoot, height=self.height, width=self.width, highlightthickness=0, bd=0)

        closebtn = Button(canvas, text='X', relief="flat", width=self.width - self.borderWidth*2, height=self.height - self.borderHeight*2, bg=self.bgColor, fg="orange", activebackground=self.bgColor, borderwidth=self.borderWidth, highlightthickness=5, highlightbackground="purple", justify=LEFT, command=lambda : self.mainModel.close())
        closebtn.pack(side='left')

        self.drawFrame(canvas, 0, 0, self.height, self.width, self.bgColor, self.borderColor, self.borderWidth, self.borderHeight, self.shadowColor, self.shadowWidth, self.shadowHeight)

        return canvas