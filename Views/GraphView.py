from Views.View import View
from tkinter import *
from GUISettings import GUISettings
from Models.MenuModel import PageType

class GraphView(View):
    def __init__(self, mainModel, graphModel, redraw = True):
        super().__init__(mainModel, redraw)

        self.graphMode = graphModel
        self.show = True

        self.offsetX = GUISettings.mainBorderWidth
        self.offsetY = 48

        self.margin = GUISettings.mainMargin

        self.width = GUISettings.graphWidth
        self.height = GUISettings.mainHeight - self.margin*2 - self.offsetY - GUISettings.mainBorderHeight

        self.bgColor = GUISettings.graphBgColor

        self.borderColor = GUISettings.graphBorderColor
        self.borderWidth = 1
        self.borderHeight = 1

        self.titleX = NONE
        self.titleY = NONE

        self.graph = None

        self.num = 0

        return

    def getScreen(self):
        canvas = Canvas(self.mainModel.mainRoot, height=self.height + self.margin * 2, width=self.width + self.margin * 2, highlightthickness=0, bd=0, bg=GUISettings.mainBgColor)

        if self.show is True:
            self.drawFrame(canvas, GUISettings.graphBarWidth + self.margin, self.margin, self.width - GUISettings.graphBarWidth, self.height - GUISettings.graphBarHeight, self.bgColor, self.borderColor, self.borderWidth, self.borderHeight, self.borderColor)

            rows = 10
            colums = 10

            offsetX = GUISettings.graphBarWidth + self.borderWidth + self.margin
            offsetY = self.borderHeight + self.margin

            maxWidth = (self.width - GUISettings.graphBarWidth - self.borderWidth * 2)
            maxHeight = (self.height - GUISettings.graphBarHeight - self.borderHeight * 2)

            for x in range(rows-1):
                canvas.create_line(offsetX + (x + 1) * (maxWidth / rows), offsetY, offsetX + (x + 1) * (maxWidth / rows), offsetY + maxHeight, width=1, fill=GUISettings.graphLineColor, dash=(2,8))

            for x in range(rows+1):
                canvas.create_line(offsetX + x * (maxWidth/rows), offsetY + maxHeight - self.borderHeight, offsetX + x * (maxWidth/rows), offsetY + maxHeight + GUISettings.graphLineOffsetY + self.borderHeight, width=1, fill=self.borderColor)

            for y in range(colums-1):
                canvas.create_line(offsetX, offsetY + (y + 1) * (maxHeight / colums), offsetX + maxWidth,
                                   offsetY + (y + 1) * (maxHeight / colums), width=1, fill=GUISettings.graphLineColor, dash=(2, 8))

            for y in range(colums+1):
                canvas.create_line(offsetX - self.borderWidth - GUISettings.graphLineOffsetX,
                                   offsetY + y * (maxHeight / colums), offsetX,
                                   offsetY + y * (maxHeight / colums), width=1, fill=self.borderColor)

        self.canvas = canvas

        self.updateGraph()

        return canvas

    def updateGraph(self):
        if self.canvas is None:
            return

        pageType = str(self.mainModel.currPage)
        setting = None

        if pageType in GUISettings.Settings.keys():
            setting = GUISettings.Settings[pageType]

        offsetX = GUISettings.graphBarWidth + self.borderWidth + self.margin
        offsetY = self.borderHeight + self.margin

        self.canvas.delete("temp")
        self.canvas.delete("state")

        if setting is not None:
            self.show = True

            rows = 10
            columns = 10

            maxWidth = (self.width - GUISettings.graphBarWidth - self.borderWidth * 2)
            maxHeight = (self.height - GUISettings.graphBarHeight - self.borderHeight * 2)

            width = (maxWidth / rows)

            data = self.mainModel.getData(str(self.mainModel.currPage))[-(columns+1):]

            for x in range(rows + 1):
                if self.mainModel.runTime <= (GUISettings.updateTime * rows):
                    val = x * GUISettings.updateTime / 1000
                else:
                    val = (self.mainModel.runTime - (GUISettings.updateTime * (rows - x + 1))) / 1000

                self.canvas.create_text(offsetX + x * (maxWidth / rows),
                                   offsetY + maxHeight + GUISettings.graphLineOffsetY + 2 + self.borderHeight,
                                   text='%d' % val, anchor=N, tags="state")

            for y in range(columns + 1):
                val = setting.maxValue - (setting.maxValue / rows * y)

                self.canvas.create_text(offsetX - self.borderWidth - GUISettings.graphLineOffsetX - 2,
                                   offsetY + y * (maxHeight / columns),
                                   text='%d' % val, anchor=E, tags="state")

            if self.mainModel.currPage == PageType.LIGHT:
                titleX = "Tijd (Seconden)"
                titleY = "Hoeveelheid licht"
            elif self.mainModel.currPage == PageType.TEMPERATURE:
                titleX = "Tijd (Seconden)"
                titleY = "Temperatuur (Celsius)"
            else:
                titleX = ""
                titleY = ""

            self.canvas.create_text(GUISettings.graphBarWidth + maxWidth / 2, maxHeight + GUISettings.graphBarHeight,
                               text=titleX, anchor=E, tags="state")

            self.canvas.create_text(GUISettings.graphBarWidth + maxWidth / 2, maxHeight + GUISettings.graphBarHeight,
                                    text=titleY, anchor=E, tags="state")

            for i in range(len(data)-1):
                old = int(data[i])
                new = int(data[i+1])

                oldX = width * i
                newX = width * (i+1)
                oldY = maxHeight - old/setting.maxValue * maxHeight
                newY = maxHeight - new/setting.maxValue * maxHeight

                self.canvas.create_line(offsetX + oldX, offsetY + oldY, offsetX + newX, offsetY + newY, width=2, fill="red", tags="temp")
        else:
            self.show = False

    def update(self, reset = False):
        self.updateGraph()

        pass