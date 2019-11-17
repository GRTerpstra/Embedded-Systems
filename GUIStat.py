class GUIStat:
    def __init__(self, title, value):
        self.title = title
        self.defaultValue = value
        self.value = value

        return

    def setValue(self, value):
        self.value = value

    def reset(self):
        self.setValue(self.defaultValue)