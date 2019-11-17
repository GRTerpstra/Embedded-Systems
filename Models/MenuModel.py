from enum import Enum
class MenuModel:
    def __init__(self, mainModel):
        self.mainModel = mainModel
        self.pageTypes = dict()

        for page in PageType:
            self.pageTypes[page.name] = page.value

        return

class PageType(Enum):
    #HOME = "HOME"
    LIGHT = "LIGHT SENSOR"
    TEMPERATURE = "TEMPERATURE SENSOR"

    def __str__(self):
        return str(self.name)