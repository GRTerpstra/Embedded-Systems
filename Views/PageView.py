from Views.View import View
from tkinter import *
from GUISettings import GUISettings
from Models.MenuModel import PageType

class PageView(View):
    def __init__(self, mainModel, redraw = True):
        super().__init__(mainModel, redraw)

        self.offsetX = GUISettings.mainBorderWidth
        self.offsetY = 48

        self.height = GUISettings.mainHeight - self.offsetY - GUISettings.mainBorderHeight
        self.show = True

        return

    def getScreen(self):
        pageType = str(self.mainModel.currPage)

        width = GUISettings.mainWidth - GUISettings.mainBorderWidth*2 - GUISettings.graphWidth - GUISettings.graphMarginX*2
        offsetX = GUISettings.graphWidth + GUISettings.mainBorderWidth + GUISettings.graphMarginX*2

        self.width = width
        self.offsetX = offsetX

        canvas = Canvas(self.mainModel.mainRoot, height=self.height, width=width, highlightthickness=0, bd=0, bg=GUISettings.mainBgColor)
        tabs = []
        settings = []

        offsetX = 0
        offsetY = GUISettings.mainMargin

        if pageType in GUISettings.tabStats.keys():
            tabs = GUISettings.tabStats[pageType]

        if pageType in GUISettings.tabSettings.keys():
            settings = GUISettings.tabSettings[pageType]

        if len(tabs) > 0:
            tabWidth = width / 2 - GUISettings.mainMargin
            tabHeight = GUISettings.tabHeight
            color = GUISettings.colorOne
            row = 0

            for key in tabs:
                stat = None

                if key in GUISettings.Stats.keys():
                    stat = GUISettings.Stats[key]

                if stat is None:
                    continue

                if row % 2 == 0:
                    color = GUISettings.colorTwo
                else:
                    color = GUISettings.colorOne

                label = self.drawTab(canvas, offsetX, offsetY, tabWidth, tabHeight, stat, color)

                if offsetX > 0:
                    offsetX = 0
                    offsetY += (GUISettings.mainMargin + tabHeight)
                    row += 1
                else:
                    offsetX = GUISettings.mainMargin + tabWidth
                    color = GUISettings.colorTwo

        if len(settings) > 0:
            setHeight = GUISettings.settingHeight
            setWidth = width - GUISettings.mainMargin

            if offsetX > 0:
                offsetY += (GUISettings.mainMargin + tabHeight)

            offsetX = 0

            for key in settings:
                setting = None

                if key in GUISettings.Settings.keys():
                    setting = GUISettings.Settings[key]

                if setting is None:
                    continue

                self.drawSetting(canvas, offsetX, offsetY, setWidth, setHeight, setting)
                offsetY += (GUISettings.mainMargin + setHeight)

        self.canvas = canvas

        return canvas