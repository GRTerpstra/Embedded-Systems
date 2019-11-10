class SensorSetting:
    def __init__(self, type, minValue, maxValue, defaultValue = -1):
        self.type = type
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