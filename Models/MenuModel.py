from enum import Enum
from Controllers.MainController import SensorType

class MenuModel:
    def __init__(self, mainModel):
        self.mainModel = mainModel
        self.pageTypes = dict()

        for page in PageType:
            self.pageTypes[page.name] = page.value

        return

    def switchPage(self, type):
        self.mainModel.currPage = type
        self.mainModel.updateViews()

        return

class PageType(Enum):
    LIGHT = "LIGHT SENSOR"
    TEMPERATURE = "TEMPERATURE SENSOR"

    def __str__(self):
        return str(self.name)