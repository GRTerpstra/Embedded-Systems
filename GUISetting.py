class GUISetting:
    def __init__(self, key, title, minValue, maxValue, defaultValue = -1, steps = 10):
        self.key = key
        self.title = title
        self.minValue = minValue
        self.maxValue = maxValue

        if defaultValue >= 0:
            if defaultValue > maxValue:
                defaultValue = maxValue
            elif defaultValue < minValue:
                defaultValue = minValue
        else:
            defaultValue = self.minValue

        if defaultValue > 255:
            defaultValue = 255

        self.tempValue = defaultValue
        self.defaultValue = defaultValue
        self.currValue = defaultValue
        self.steps = steps

        return

    def setValue(self, value, save=True):
        value = max(self.minValue, min(value, self.maxValue))

        if save == True:
            self.currValue = value

        self.tempValue = value

    def updateValue(self):
        self.setValue(self.tempValue)

    def reset(self):
        self.setValue(self.currValue)