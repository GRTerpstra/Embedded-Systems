class MenuModel:
    def __init__(self, mainModel):
        self.mainModel = mainModel
        self.currPage = PageType.HOME

        return

class PageType(Enum):
    HOME = 0
    LIGHT = 1
    TEMPERATURE = 2