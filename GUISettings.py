from GUIStat import GUIStat
from GUISetting import GUISetting
from Models.MenuModel import PageType
from Controllers.MainController import SensorType

class GUISettings:
    mainWidth = 1000
    mainHeight = 600
    mainMargin = 6
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
    menuBtnFont = ("Times New Roman", 11, 'bold')
    menuBtnHeight = 28
    menuBtnHoverColor = "#3d414a"
    menuBtnBorderColor = menuBgColor
    menuBtnBorderHoverColor = "red"
    graphBgColor = "#282a30"
    graphBorderColor = "black"
    graphTextColor = "white"
    graphLineColor = "black"
    graphLineOffsetX = 6
    graphLineOffsetY = 6
    graphMarginX = 8
    graphMarginY = 10
    graphBarWidth = 42
    graphBarHeight = 42
    graphWidth = 620
    tabHeight = 55
    tabBgColor = "#282a30"
    tabBorderColor = "black"
    tabBorderWidth = 1
    tabBorderHeight = 1
    tabTitleBgColor = "#444953"
    tabTitleHeight = 26
    tabTitlePaddingX = 6
    tabTitlePaddingY = 4
    tabTitleFont = ("Times New Roman", 10, 'bold')
    tabTitleColor = "white"
    tabLabelPaddingY = 11
    tabLabelFont = ("Times New Roman", 15, 'bold')
    settingHeight = 100
    setLabelMarginX = 5
    closeWidth = 22
    closeHeight = 22
    closeBorderWidth = 1
    closeBorderHeight = 1
    closeBorderColor = "black"
    closeShadowWidth = 1
    closeShadowHeight = 1
    closeShadowColor = "#ff6464"
    closeColor = "#FF0000"
    closeFont = ("Times New Roman", 10, 'bold')
    updateTime = 1000
    connPort = 9600

    colorOne = "#8ab71b"
    colorTwo = "#2aa3d6"

    tabStats = {
        str(SensorType.TEMPERATURE): ["currTemp", "targetTemp", "sectionTempTime", "totalTempTime"],
        str(SensorType.LIGHT): ["currLight", "targetLight", "sectionLightTime", "totalLightTime"]
    }

    tabSettings = {
        str(SensorType.TEMPERATURE): ["tempTarget", "tempDistance", "tempTime"],
        str(SensorType.LIGHT): ["lightTarget", "lightDistance", "lightTime"]
    }

    Stats = {
        "currLight": GUIStat("current light", 0),
        "targetLight": GUIStat("target light", 0),
        "sectionLightTime": GUIStat("section time", 0),
        "totalLightTime": GUIStat("total time", 0),
        "currTemp": GUIStat("current temperature", 0),
        "targetTemp": GUIStat("target temperature", 0),
        "sectionTempTime": GUIStat("section time", 0),
        "totalTempTime": GUIStat("total time", 0)
    }

    Settings = {
        str(SensorType.DISTANCE): GUISetting(str(SensorType.DISTANCE), 0, 100, 50),
        str(SensorType.LIGHT): GUISetting(str(SensorType.LIGHT), 0, 100, 30),
        str(SensorType.TEMPERATURE): GUISetting(str(SensorType.TEMPERATURE), 0, 50, 40),

        "lightTarget": GUISetting("target light", 0, 100, 50),
        "lightDistance": GUISetting("target distance", 0, 100, 50),
        "lightTime": GUISetting("section time", 0, 100, 30),
        "tempTarget": GUISetting("target temperature", 0, 100, 50),
        "tempDistance": GUISetting("target distance", 0, 100, 50),
        "tempTime": GUISetting("section time", 0, 100, 30),
    }
