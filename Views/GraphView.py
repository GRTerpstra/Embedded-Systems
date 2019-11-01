from Views.View import View

class GraphView(View):
    def __init__(self, mainModel, graphModel, redraw = True):
        super().__init__(mainModel, redraw)

        self.graphMode = graphModel

        return

    def getScreen(self):
        super().getScreen()

        return