from tkinter.font import Font
from Controllers.MainController import SensorType
from SensorSetting import SensorSetting

class GUISettings:
    mainWidth = 1000
    mainHeight = 600
    mainBgColor = "#2e3138"
    mainBorderColor = "black"
    mainBorderWidth = 1
    mainBorderHeight = 1
    menuBgColor = "#444953"
    menuHeight = 40
    menuBorderColor = "black"
    menuBorderWidth = 1
    menuBorderHeight = 1
    menuShadowColor = "#575c65"
    graphBgColor = "#282a30"
    graphBorderColor = "black"
    graphTextColor = "white"
    graphLineColor = "black"
    graphLineOffsetX = 6
    graphLineOffsetY = 6
    graphMarginX = 0
    graphMarginY = 10
    graphBarWidth = 42
    graphBarHeight = 42
    closeWidth = 22
    closeHeight = 22
    closeBorderWidth = 1
    closeBorderHeight = 1
    closeBorderColor = "black"
    closeShadowWidth = 1
    closeShadowHeight = 1
    closeShadowColor = "#ff6464"
    closeColor = "#FF0000"
    updateTime = 1000
    connPort = 9600

    sensorSettings = {
        SensorType.DISTANCE: SensorSetting(SensorType.DISTANCE, 0, 255, 50),
        SensorType.LIGHT: SensorSetting(SensorType.DISTANCE, 0, 255, 30),
        SensorType.TEMPERATURE: SensorSetting(SensorType.DISTANCE, 0, 255, 40)
    }