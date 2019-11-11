import serial
from enum import Enum
import SensorSetting

class MainController:
    def __init__(self, mainModel):
        self.mainModel = mainModel

        return

class SensorType(Enum):
    DISTANCE = 1
    LIGHT = 2
    TEMPERATURE = 3
    MANUAL = 4

    def __str__(self):
        return str(self.name)

