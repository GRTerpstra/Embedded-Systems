from tkinter import *
from GUISettings import GUISettings
import math
from functools import partial

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
        set = Canvas(canvas, height=height, width=width, highlightthickness=0, bd=0, bg=GUISettings.mainBgColor)

        tBox = Canvas(set, height=GUISettings.setTitleHeight, width=width, highlightthickness=0, bd=0, bg=GUISettings.mainBgColor)
        title = Label(tBox, text=str.upper(setting.title), font=(GUISettings.setTitleFont), fg="white",
                      bg=GUISettings.mainBgColor, bd=0)

        sBox = Canvas(set, height=height-GUISettings.setTitleHeight, width=(width - GUISettings.setLabelWidth - GUISettings.setLabelMarginX - GUISettings.setBarBorder*2), highlightthickness=0, bd=0, bg=GUISettings.mainBgColor)

        lBox = Canvas(set, height=GUISettings.setLabelHeight, width=GUISettings.setLabelWidth, highlightthickness=0, bd=0, bg=GUISettings.setLabelBgColor)
        slabel = Label(lBox, text=str(setting.tempValue), font=(GUISettings.setTitleFont), fg="white", bg=GUISettings.setLabelBgColor, bd=0)

        var = DoubleVar()
        slider = Scale(sBox, width=15, from_=setting.minValue, to=setting.maxValue, showvalue=0, bd=GUISettings.setBarBorder, bg=GUISettings.mainBgColor, activebackground=GUISettings.mainBgColor, fg="white", orient=HORIZONTAL, troughcolor=GUISettings.setBarColor, relief="flat", length=(width - GUISettings.setLabelWidth - GUISettings.setLabelMarginX - GUISettings.setBarBorder*2), highlightthickness=0, variable = var, command=partial(self.mainModel.updateSet, setting.key, slabel))

        slider.set(setting.tempValue)

        title.place(x=0, y=2.5)
        slider.place(x=0, y=0)
        slabel.place(relx=0.5, rely=0.5, anchor="c")

        lBox.place(x=(width - GUISettings.setLabelWidth - GUISettings.setBarBorder*2), y=(height - GUISettings.setLabelHeight))
        tBox.place(x=0, y=0)
        sBox.place(x=0, y=GUISettings.setTitleHeight)

        set.place(x=x, y=y)

        return

    def drawButton(self, canvas, x, y, width, height, title, function, args = []):
        holder = Canvas(canvas, width=width, height=height, highlightthickness=0, bd=0, bg=GUISettings.btnBorderColor)

        btn = Button(holder, text=title, bd=1, bg=GUISettings.btnBgColor, fg="white", activeforeground="white",
                     activebackground=GUISettings.btnBgColor, borderwidth=GUISettings.btnBorderWidth, highlightthickness=0,
                     font=GUISettings.btnFont, command=lambda: function(*args),
                     anchor="c")

        btn.place(x=GUISettings.btnBorderWidth, y=GUISettings.btnBorderHeight, width=width - GUISettings.btnBorderWidth*2, height=height - GUISettings.btnBorderHeight*2)
        holder.place(x=x, y=y)

        return

    def drawToggle(self, canvas, x, y, key):
        if key not in GUISettings.Settings.keys():
            return

        setting = GUISettings.Settings[key]
        holder = Canvas(canvas, width=GUISettings.toggleWidth, height=GUISettings.toggleHeight, highlightthickness=0, bd=0, bg=GUISettings.mainBgColor)

        tBox = Canvas(holder, height=GUISettings.setTitleHeight, width=GUISettings.toggleWidth, highlightthickness=0, bd=0,
                      bg=GUISettings.mainBgColor)
        title = Label(tBox, text=str.upper(setting.title), font=(GUISettings.setTitleFont), fg="white",
                      bg=GUISettings.mainBgColor, bd=0)

        cBox = Canvas(holder, height=GUISettings.toggleHeight - GUISettings.setTitleHeight, width = GUISettings.toggleWidth, highlightthickness=0, bd=0, bg=GUISettings.mainBgColor)
        cToggle = Canvas(cBox, height=GUISettings.toggleSwitchHeight, width = GUISettings.toggleSwitchWidth, highlightthickness=0, bd=0, bg="black")

        fSwitch = Canvas(cToggle, height=GUISettings.toggleSwitchHeight - 2, width=GUISettings.toggleSwitchWidth / 2 - 2,
                           highlightthickness=0, bd=0, bg=GUISettings.toggleColor)

        if setting.tempValue == 1:
            bSwitch = Canvas(cToggle, height=GUISettings.toggleSwitchHeight - 2, width = GUISettings.toggleSwitchWidth/2-1, highlightthickness=0, bd=0, bg=GUISettings.toggleOnColor)
            bLabel = Label(bSwitch, text="ON", font=(GUISettings.toggleFont), fg="white",
                           bg=GUISettings.toggleOnColor, bd=0)

            fSwitch.place(x=GUISettings.toggleSwitchWidth/2+1, y=1)
            bSwitch.place(x=1, y=1)

            bSwitch.bind("<Button-1>", lambda event, k=key: self.mainModel.updateToggle(k, 0))
            fSwitch.bind("<Button-1>", lambda event, k=key: self.mainModel.updateToggle(k, 0))
            bLabel.bind("<Button-1>", lambda event, k=key: self.mainModel.updateToggle(k, 0))
        else:
            bSwitch = Canvas(cToggle, height=GUISettings.toggleSwitchHeight - 2,
                           width=GUISettings.toggleSwitchWidth / 2 - 1,
                           highlightthickness=0, bd=0, bg=GUISettings.toggleOffColor)
            bLabel = Label(bSwitch, text="OFF", font=(GUISettings.toggleFont), fg="white",
                           bg=GUISettings.toggleOffColor, bd=0)

            bSwitch.place(x=GUISettings.toggleSwitchWidth / 2, y=1)
            fSwitch.place(x=1, y=1)

            bSwitch.bind("<Button-1>", lambda event, k=key: self.mainModel.updateToggle(k, 1))
            fSwitch.bind("<Button-1>", lambda event, k=key: self.mainModel.updateToggle(k, 1))
            bLabel.bind("<Button-1>", lambda event, k=key: self.mainModel.updateToggle(k, 1))

        title.place(x=0, y=2.5)
        bLabel.place(relx=0.5, rely=0.5, anchor='center')

        tBox.place(x=0, y=0)
        cBox.place(x=0,y=GUISettings.setTitleHeight)
        cToggle.place(relx = 0.5, rely=0.5, anchor="c")
        holder.place(x=x, y=y)




