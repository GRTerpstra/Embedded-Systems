class GUISetting:
    def __init__(self, title, minValue, maxValue, defaultValue = -1, steps = 10):
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

        self.defaultValue = defaultValue
        self.currValue = defaultValue
        self.steps = steps

        return

    def setValue(self, value):
        self.value = max(self.minValue, min(value, self.maxValue))

    def reset(self):
        self.setValue(self.defaultValue)