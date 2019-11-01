class MainController:
    def __init__(self, mainModel):
        self.mainModel = mainModel

        self.running = False

        return

    def start(self):
        self.running = True

    def stop(self):
        self.running = False