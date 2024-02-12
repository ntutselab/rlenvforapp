class AppEvent:
    def __init__(self, xpath: str, value: str, category: str):
        self._xpath = xpath
        self._value = value
        self._category = category

    def get_xpath(self):
        return self._xpath

    def get_value(self):
        return self._value

    def get_category(self):
        return self._category
