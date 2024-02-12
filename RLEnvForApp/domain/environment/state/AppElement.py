class AppElement:
    def __init__(self, tagName: str, name: str,
                 type: str, xpath: str, value: str):
        self._tagName = tagName
        self._name = name
        self._type = type
        self._xpath = xpath
        self._value = value

    def get_tag_name(self):
        return self._tagName

    def get_name(self):
        return self._name

    def get_type(self):
        return self._type

    def get_xpath(self):
        return self._xpath

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value
