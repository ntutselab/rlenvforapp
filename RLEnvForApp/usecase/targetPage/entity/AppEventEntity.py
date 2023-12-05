class AppEventEntity:
    def __init__(self, xpath: str, value: str, category: str):
        self._xpath = xpath
        self._value = value
        self._category = category

    def getXpath(self):
        return self._xpath

    def getValue(self):
        return self._value

    def getCategory(self):
        return self._category
