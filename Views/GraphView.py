from Views.View import View
from tkinter import *

class GraphView(View):
    def __init__(self, mainModel, graphModel, redraw = True):
        super().__init__(mainModel, redraw)

        self.graphMode = graphModel

        return

    def getScreen(self):
        canvas = super().getScreen()

        #canvas.create_rectangle(0, 0, 100, 100, fill='black')

        return canvas