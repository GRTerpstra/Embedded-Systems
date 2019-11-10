from Controllers import MainController, MenuController, GraphController
from Models import MainModel, MenuModel, GraphModel
from Views import PageView, MenuView, GraphView, MainView, CloseView

from tkinter import *

class GUI:
    def __init__(self):
        #create/set MVC (Model, View, Controller)
        self.mainModel = MainModel.MainModel()
        self.menuModel = MenuModel.MenuModel(self.mainModel)
        self.graphModel = GraphModel.GraphModel(self.mainModel)

        self.mainController = MainController.MainController(self.mainModel)
        self.menuController = MenuController.MenuController(self.mainModel, self.menuModel)
        self.graphController = GraphController.GraphController(self.mainModel, self.graphModel)

        self.mainView = MainView.MainView(self.mainModel, False)
        self.pageView = PageView.PageView(self.mainModel, False)
        self.menuView = MenuView.MenuView(self.mainModel, self.menuModel, False)
        self.graphView = GraphView.GraphView(self.mainModel, self.graphModel, False)
        self.closeView = CloseView.CloseView(self.mainModel, False)

        self.mainModel.updateViews()
        self.mainController.start()

    def close(self):
        self.bgRoot.destroy()
        self.mainRoot.destroy()