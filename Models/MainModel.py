from tkinter import *
from enum import Enum
from GUISettings import GUISettings
from Controllers.MainController import SensorType
from Views import GraphView, PageView
import random
import serial
import json
import time

class MainModel():
    def __init__(self):
        self.views = dict()
        self.frames = dict()
        self.currPage = PageType.LIGHT
        self.testCounter = 0;

        self.sensorTypes = [SensorType.DISTANCE, SensorType.LIGHT, SensorType.TEMPERATURE]
        self.switchTypes = [SensorType.LIGHT, SensorType.TEMPERATURE]
        self.sensorData = dict()

        self.conn = None
        self.manual = False
        self.running = False
        self.currType = None
        self.runTime = 0

        self.lastJson = None;

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
        centerX = int(self.screenWidth / 2 - GUISettings.mainWidth / 2)
        centerY = int(self.screenHeight / 2 - GUISettings.mainHeight / 2)

        # set start position and margin
        mainRoot.geometry('{}x{}+{}+{}'.format(GUISettings.mainWidth, GUISettings.mainHeight, centerX, centerY))
        backRoot.geometry('{}x{}+{}+{}'.format(GUISettings.closeWidth, GUISettings.closeHeight,
                                               centerX + GUISettings.mainWidth - int(GUISettings.closeWidth / 2),
                                               centerY - int(GUISettings.closeHeight / 2)))

        mainFrame = Frame(mainRoot, width=GUISettings.mainWidth, height=GUISettings.mainHeight,
                          bg=GUISettings.mainBgColor)
        closeFrame = Frame(backRoot, width=GUISettings.closeWidth, height=GUISettings.closeHeight)

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
        self.updateView(GraphView.GraphView)
        self.updateViews(False)
        self.mainRoot.after(GUISettings.updateTime, self.update)

        pageType = str(self.currPage)
        setting = None

        if pageType in GUISettings.Settings:
            setting = GUISettings.Settings[pageType]

        self.runTime += GUISettings.updateTime

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
                if view.show:
                    frame = view.getCanvas(False)
                    frame.pack_propagate(0)

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
        for type in self.switchTypes:
            tabSettings = GUISettings.tabSettings

            for tabSetting in tabSettings:
                if tabSetting in GUISettings.Settings.keys():
                    setting = GUISettings.Settings[tabSetting]
                    self.updateSetting(type, setting)


    def write(self, byte):
        if self.conn == None:
            return

        self.conn.write(byte.encode('ascii'))

        pass

    def read(self):
        if self.lastJson is not None:
            data = self.lastJson;
        else:
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
                    self.lastJson = data;
                else:
                    print("Invalid data")
                    return []

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
                if int(setting.minValue) > int(data['l']):
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
        if str(type) in GUISettings.Settings.keys():
            return GUISettings.Settings[str(type)]

        return None

    def updateSet(self, key, label, value):
        if key is None or key not in GUISettings.Settings.keys():
            return

        setting = GUISettings.Settings[key]
        setting.setValue(int(value), False)

        label.configure(text=str(setting.tempValue))

        return

    def updateSetting(self, key, save = True, value = None):
        if key is None or key not in GUISettings.Settings.keys():
            return

        setting = GUISettings.Settings[key]

        if value is not None:
            setting.setValue(value, save)

        setting.updateValue()

        #todo: update setting in arduino by writing it
        #self.write(str(data))

        if save == True:
            pass

        return

    def resetSetting(self, key, save = True):
        if key is None or key not in GUISettings.Settings.keys():
            return

        setting = GUISettings.Settings[key]
        setting.reset()

        # todo: update setting in arduino by writing it
        # self.write(str(data))

        if save == True:
            pass

        return

    def updateToggle(self, key, value):
        self.updateSetting(key, True, value)
        self.updateView(PageView)
        self.updateViews()

    def resetSettings(self, type):
        if type is None or type not in GUISettings.tabSettings.keys():
            return

        settings = GUISettings.tabSettings[type]

        for key in settings:
            self.resetSetting(key, False)

        self.updateView(PageView)
        self.updateViews()

        return

    def saveSettings(self, type):
        if type is None or type not in GUISettings.tabSettings.keys():
            return

        settings = GUISettings.tabSettings[type]

        for key in settings:
            self.updateSetting(key, True)

        self.updateView(PageView)
        self.updateViews()

        return

    def updateStat(self, key, add):
        if key is None or key not in GUISettings.Stats.keys():
            return

        stat = GUISettings.Stats[key]
        stat.setValue(stat.currValue + add)

        return

    def resetStat(self, key):
        if key is None or key not in GUISettings.Stats.keys():
            return

        stat = GUISettings.Stats[key]
        stat.reset()

        return

    def switchPage(self, type):
        if self.currPage == type:
            return

        self.updateView(PageView)
        self.currPage = type
        self.updateViews()

        return


class PageType(Enum):
    LIGHT = 0
    TEMPERATURE = 1

    def __str__(self):
        return str(self.name)
