from Views.View import View
from tkinter import *
from GUISettings import GUISettings
from Models.MenuModel import PageType

class GraphView(View):
    def __init__(self, mainModel, graphModel, redraw = True):
        super().__init__(mainModel, redraw)

        self.graphMode = graphModel
        self.show = True

        self.offsetX = 0
        self.offsetY = 46

        self.width = 620
        self.height = 540

        self.margin = 8

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
        canvas = Canvas(self.mainModel.mainRoot, height=self.height + self.margin*2, width=self.width + self.margin*2, highlightthickness=0, bd=0, bg=GUISettings.mainBgColor)

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

        #canvas.create_rectangle(0, 0, 100, 100, fill='black')

        self.canvas = canvas

        self.updateGraph()

        return canvas

    def updateGraph(self):
        if self.canvas is None:
            return

        offsetX = GUISettings.graphBarWidth + self.borderWidth + self.margin
        offsetY = self.borderHeight + self.margin

        self.canvas.delete("temp")
        self.canvas.delete("state")

        rows = 10
        columns = 10

        maxWidth = (self.width - GUISettings.graphBarWidth - self.borderWidth * 2)
        maxHeight = (self.height - GUISettings.graphBarHeight - self.borderHeight * 2)

        width = (maxWidth / rows)

        data = self.mainModel.getData(self.mainModel.currPage)[-(columns+1):]

        for x in range(rows + 1):
            self.canvas.create_text(offsetX + x * (maxWidth / rows),
                               offsetY + maxHeight + GUISettings.graphLineOffsetY + 2 + self.borderHeight,
                               text='%d' % (10 * x), anchor=N, tags="state")

        for y in range(columns + 1):
            self.canvas.create_text(offsetX - self.borderWidth - GUISettings.graphLineOffsetX - 2,
                               offsetY + y * (maxHeight / columns),
                               text='%d' % (10 * (columns - y)), anchor=E, tags="state")

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
            old = data[i]
            new = data[i+1]

            oldX = width * i
            newX = width * (i+1)
            oldY = old/100 * maxHeight
            newY = new/100 * maxHeight

            self.canvas.create_line(offsetX + oldX, offsetY + oldY, offsetX + newX, offsetY + newY, width=2, fill="red", tags="temp")

    def update(self, reset = False):
        self.num += 1

        type = self.mainModel.currPage

        self.updateGraph()

        pass