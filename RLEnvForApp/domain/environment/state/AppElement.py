class AppElement:
    def __init__(self, tagName: str, name: str, type: str, placeholder: str, label:str, xpath: str, value: str):
        self._tagName = tagName
        self._name = name
        self._type = type
        self._placeholder = placeholder
        self.label = label
        self._xpath = xpath
        self._value = value

    def getTagName(self):
        return self._tagName

    def getName(self):
        return self._name

    def getType(self):
        return self._type

    def getPlaceholder(self):
        return self._placeholder

    def getLabel(self):
        return self.label

    def getXpath(self):
        return self._xpath

    def getValue(self):
        return self._value

    def setValue(self, value):
        self._value = value
