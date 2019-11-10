import serial
from enum import Enum
import SensorSetting

class MainController:
    def __init__(self, mainModel):
        self.mainModel = mainModel
        self.running = False

        self.sensorTypes = [SensorType.DISTANCE, SensorType.LIGHT, SensorType.TEMPERATURE]
        self.switchTypes = [SensorType.LIGHT, SensorType.TEMPERATURE]
        self.sensorData = dict()
        self.sensorSettings = []

        self.manual = False
        self.running = False
        self.currType = None

        self.conn = None

        return

    def start(self):
        self.running = True
        self.reset()
        self.mainModel.start()

    def stop(self):
        self.running = False
        self.mainModel.stop()

    def switch(self, type):
        if type is None or type not in self.switchTypes:
            return

        self.currType = type

        #update settings of current sensor and distance sensor
        self.updateType(self.currType)
        self.updateType(SensorType.DISTANCE)

    def update(self):
        if self.running is not True or self.currType is None or self.currType not in self.switchTypes:
            return

        self.updateData(self.currType)
        self.updateData(SensorType.DISTANCE)

        self.mainModel.update()

        pass

    # updates the data of the sensor, based on the selected type
    def updateData(self, sensorType):
        if self.running is not True or sensorType is None:
            return

        data = self.read(sensorType)
        self.sensorData[sensorType] = data

        pass

    def updateType(self, type, data):
        if self.running is not True or type is None or type not in self.sensorSettings:
            return

        setting = self.sensorSettings[type]
        setting.currValue = data

        self.write(str(data))

        pass

    def reset(self):
        if self.conn is not None:
            self.conn.close()

        self.data = dict()

        #setup connections
        #for type in SensorType:
        type = SensorType.DISTANCE
        num = type.value

        # start connection
        self.conn = serial.Serial('COM3', 19200)

        #reset sensor settings:
        self.sensorSettings = self.mainModel.settings.sensorSettings

        for type in self.sensorSettings:
            setting = self.sensorSettings[type]
            self.updateType(type, setting.currValue)

    def write(self, byte):
        if self.conn == None:
            return

        self.conn.write(byte.encode('ascii'))

        pass

    def read(self, type):
        if self.conn == None:
            return None

        data = None

        if (self.conn.inWaiting() > 0):
            data = self.conn.read(self.conn.inWaiting()).decode('ascii')

        return data

    def getData(self, type):
        if type is None or type not in self.sensorData.keys():
            return 0

        return self.sensorData[type]

class SensorType(Enum):
    DISTANCE = 1
    LIGHT = 2
    TEMPERATURE = 3
    MANUAL = 4

    def __str__(self):
        return str(self.name)

