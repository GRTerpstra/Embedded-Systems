from Views.View import View

class MenuView(View):
    def __init__(self, mainModel, menuModel, redraw = True):
        super().__init__(mainModel, redraw)

        self.menuModel = menuModel

        return

    def getScreen(self):
        super().getScreen()

        return