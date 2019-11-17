from Views.View import View
from tkinter import *
from GUISettings import GUISettings
from functools import partial

class MenuView(View):
    def __init__(self, mainModel, menuModel, redraw = True):
        super().__init__(mainModel, redraw)

        self.offsetX = 0
        self.offsetY = GUISettings.mainMargin + GUISettings.mainBorderHeight

        self.bgColor = GUISettings.menuBgColor

        self.borderWidth = GUISettings.menuBorderWidth
        self.borderHeight = GUISettings.menuBorderHeight

        self.borderColor = GUISettings.menuBorderColor

        self.height = GUISettings.menuHeight
        self.width = GUISettings.mainWidth

        self.mainModel = mainModel
        self.menuModel = menuModel

        self.show = True

        return

    def getScreen(self):
        canvas = Canvas(self.mainModel.mainRoot, height=self.height, width=self.width, highlightthickness=0, bd=0, bg=GUISettings.menuBgColor)
        mainModel = self.mainModel
        self.drawFrame(canvas, 0, 0, self.width, self.height, self.bgColor, self.borderColor, self.borderWidth, self.borderHeight, GUISettings.menuShadowColor, 0, 2)

        #create buttons
        if len(self.menuModel.pageTypes) > 0:
            margin =  0

            navbar = Canvas(canvas, width=self.width, height=GUISettings.menuBtnHeight, bg=GUISettings.menuBgColor, bd=0, highlightthickness=0)

            # create buttons
            if len(self.menuModel.pageTypes) > 0:
                index = 0

                for name, title in self.menuModel.pageTypes.items():
                    outside = Frame(navbar, borderwidth=0, relief="flat", highlightcolor="white", bg=GUISettings.menuBgColor)
                    inside = Frame(outside, borderwidth=0, relief="flat", highlightcolor="white", bg=GUISettings.menuBgColor)

                    outside.pack(side="left", padx=(5, 5))
                    inside.pack(side="left")

                    label = Label(inside, text=title, justify="left", font=GUISettings.menuBtnFont, fg="white", bg=GUISettings.menuBgColor, bd=1, highlightthickness=1, highlightcolor="yellow", anchor='w')

                    label.bind("<Enter>", self.on_enter)
                    label.bind("<Leave>", self.on_leave)
                    label.bind("<Button-1>", lambda event, n=name: self.mainModel.switchPage(n))

                    label.pack(anchor="w", side="left")

            navbar.pack(side="left", padx=(5, 5))

        return canvas

    def on_enter(self, event):
        event.widget.configure(bg=GUISettings.menuBtnHoverColor, cursor="hand2")

    def on_leave(self, event):
        event.widget.configure(bg=GUISettings.menuBgColor, cursor="arrow")