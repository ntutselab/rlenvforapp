class IConverter:
    def __init__(self):
        pass

    def convert(self, stateElement, length: int = 0):
        listFeature: [] = self._convertToListFeature(stateElement=stateElement)
        return self._paddingToLength(listFeature=listFeature, length=length)

    def _convertToListFeature(self, stateElement) -> []:
        pass

    def _paddingToLength(self, listFeature: [], length: int):
        while len(listFeature) < length:
            listFeature.append(0)

        if len(listFeature) > length and length != 0:
            return listFeature[:length]

        return listFeature
