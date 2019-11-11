from tkinter import *
from enum import Enum
from GUISettings import GUISettings
from Controllers.MainController import SensorType
from Views import GraphView
import random
import serial
import json
import time


class MainModel():
    def __init__(self):
        self.views = dict()
        self.frames = dict()
        self.currPage = PageType.LIGHT
        self.settings = GUISettings
        self.testCounter = 0;

        self.sensorTypes = [SensorType.DISTANCE, SensorType.LIGHT, SensorType.TEMPERATURE]
        self.switchTypes = [SensorType.LIGHT, SensorType.TEMPERATURE]
        self.sensorData = dict()
        self.sensorSettings = []

        self.conn = None
        self.manual = False
        self.running = False
        self.currType = None
        self.runTime = 0

        # create main frame/canvas
        mainRoot = Tk()
        mainRoot.overrideredirect(True)
        mainRoot.attributes('-topmost', True)

        bgRoot = Toplevel(mainRoot)
        bgRoot.wm_attributes('-alpha', 0.3)
        bgRoot.wm_attributes("-fullscreen", True)
        bgRoot.overrideredirect(True)
        bgRoot.attributes('-topmost', False)

        backRoot = Toplevel(mainRoot)
        backRoot.overrideredirect(True)
        backRoot.attributes('-topmost', True)

        # store screen width
        self.screenWidth = mainRoot.winfo_screenwidth()
        self.screenHeight = mainRoot.winfo_screenheight()

        # Gets both half the screen width/height and window width/height
        centerX = int(self.screenWidth / 2 - self.settings.mainWidth / 2)
        centerY = int(self.screenHeight / 2 - self.settings.mainHeight / 2)

        # set start position and margin
        mainRoot.geometry('{}x{}+{}+{}'.format(self.settings.mainWidth, self.settings.mainHeight, centerX, centerY))
        backRoot.geometry('{}x{}+{}+{}'.format(self.settings.closeWidth, self.settings.closeHeight,
                                               centerX + self.settings.mainWidth - int(self.settings.closeWidth / 2),
                                               centerY - int(self.settings.closeHeight / 2)))

        mainFrame = Frame(mainRoot, width=self.settings.mainWidth, height=self.settings.mainHeight,
                          bg=self.settings.mainBgColor)
        closeFrame = Frame(backRoot, width=self.settings.closeWidth, height=self.settings.closeHeight)

        self.mainRoot = mainRoot
        self.bgRoot = bgRoot
        self.backRoot = closeFrame
        self.closeFrame = closeFrame
        self.mainFrame = mainFrame

        self.reset()

        return

    def start(self):
        self.running = True

        # show frames
        self.mainFrame.pack()
        self.closeFrame.pack()

        # show frame
        self.mainRoot.after(10, self.update)
        self.mainRoot.mainloop()

    def stop(self):
        self.running = False

    def switch(self, type):
        if type is None or type not in self.switchTypes:
            return

        self.currType = type

        #update settings of current sensor and distance sensor
        self.updateType(self.currType)
        self.updateType(SensorType.DISTANCE)

    def update(self):
        self.updateViews(False)
        self.updateView(GraphView.GraphView)
        self.mainRoot.after(self.settings.updateTime, self.update)

        setting = self.settings.sensorSettings[str(self.currPage)]

        self.runTime += self.settings.updateTime

        self.updateData()

        return

    def addView(self, view):
        if view is None or type(view) in self.views:
            return

        self.views[type(view)] = view

    def updateView(self, type):
        if len(self.views) == 0 or type not in self.views.keys():
            return

        view = self.views[type]
        view.updateNeeded = True

    def updateViews(self, override=TRUE):
        if len(self.views) == 0:
            return

        for type in self.views.keys():
            view = self.views[type]

            if view not in self.frames:
                if (view.show is False):
                    continue

            if override or view.updateNeeded:
                frame = view.getCanvas(False)
                frame.pack()

                frame.place(x=view.offsetX, y=view.offsetY)

                self.frames[view] = frame

                view.update()

    def removeView(self, view):
        if view is None or view not in self.views:
            return

        if self.frames[view] is not None:
            frame = self.frames[view]

        self.views.remove(view)

    def close(self):
        self.mainRoot.destroy()

        return

    def getData(self, type):
        if type is None or type not in self.sensorData.keys():
            return []

        return self.sensorData[type]

    def reset(self):
        if self.conn is not None:
            self.conn.close()

        self.conn = serial.Serial('COM3', 19200)
        self.sensorData = dict()

        # reset sensor settings:
        self.sensorSettings = GUISettings.sensorSettings

        for type in self.sensorSettings:
            setting = self.sensorSettings[type]
            self.updateType(type, setting.currValue)

    def write(self, byte):
        if self.conn == None:
            return

        self.conn.write(byte.encode('ascii'))

        pass

    def read(self):
        data = []

        if self.conn is not None:
            if self.conn.inWaiting() > 0:
                data = self.conn.readline().decode('ascii')
                self.conn.flushInput()

                dataLength = len(data)

                if data[dataLength-3] == "}" and data[0] == "{":
                    counter = 1
                    dataString = ""
                    for letter in data:
                        if(counter <= dataLength-2):
                            dataString += letter
                        counter+=1

                    data = json.loads(dataString)
                else:
                    print("Datalengte: " + str(dataLength))
                    print("FOUT: " + str(data[dataLength-3]) + "|" + str(data[0]))

        return data

    # updates the data of the sensor, based on the selected type
    def updateData(self):
        if self.running is False:
            return

        data = self.read()

        tVal = "0"
        lVal = "0"
        dVal = "0"

        if 't' in data:
            setting = self.getSetting(SensorType.TEMPERATURE)

            if setting is not None:
                if setting.minValue > int(data['t']):
                    data['t'] = setting.minValue

                if setting.maxValue < int(data['t']):
                    data['t'] = setting.maxValue

            tVal = str(data['t'])
        elif 't' in self.sensorData.keys():
            tVal = str(self.sensorData['t'][len(self.sensorData['t'])-1])

        if str(SensorType.TEMPERATURE) in self.sensorData.keys():
            self.sensorData[str(SensorType.TEMPERATURE)].append(tVal)
        else:
            self.sensorData[str(SensorType.TEMPERATURE)] = [tVal]

        if 'l' in data:
            setting = self.getSetting(SensorType.LIGHT)

            if setting is not None:
                if setting.minValue > int(data['l']):
                    data['l'] = setting.minValue

                if setting.maxValue < int(data['l']):
                    data['l'] = setting.maxValue

            lVal = str(data['l'])
        elif 'l' in self.sensorData.keys():
            lVal = str(self.sensorData['l'][len(self.sensorData['l']) - 1])

        if str(SensorType.LIGHT) in self.sensorData.keys():
            self.sensorData[str(SensorType.LIGHT)].append(lVal)
        else:
            self.sensorData[str(SensorType.LIGHT)] = [lVal]

        if 'd' in data:
            setting = self.getSetting(SensorType.DISTANCE)

            if setting is not None:
                if setting.minValue > int(data['d']):
                    data['d'] = setting.minValue

                if setting.maxValue < int(data['d']):
                    data['d'] = setting.maxValue

            dVal = str(data['d'])
        elif 'd' in self.sensorData.keys():
            dVal = str(self.sensorData['d'][len(self.sensorData['d']) - 1])

        if str(SensorType.DISTANCE) in self.sensorData.keys():
            self.sensorData[str(SensorType.DISTANCE)].append(dVal)
        else:
            self.sensorData[str(SensorType.DISTANCE)] = [dVal]

    def getSetting(self, type):
        if str(type) in GUISettings.sensorSettings.keys():
            return GUISettings.sensorSettings[str(type)]

        return None

    def updateType(self, type, data):
        if self.running is not True or type is None or type not in self.sensorSettings:
            return

        setting = self.sensorSettings[type]
        setting.currValue = data

        self.write(str(data))

        pass


class PageType(Enum):
    HOME = 0
    LIGHT = 1
    TEMPERATURE = 2

    def __str__(self):
        return str(self.name)
