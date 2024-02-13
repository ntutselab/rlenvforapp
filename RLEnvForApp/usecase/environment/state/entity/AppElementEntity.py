class AppElementEntity:
    def __init__(self, tag_name: str, name: str,
                 type: str, xpath: str, value: str):
        self._tag_name = tag_name
        self._name = name
        self._type = type
        self._xpath = xpath
        self._value = value

    def get_tag_name(self):
        return self._tag_name

    def get_name(self):
        return self._name

    def get_type(self):
        return self._type

    def get_xpath(self):
        return self._xpath

    def get_value(self):
        return self._value
