class IConverter:
    def __init__(self):
        pass

    def convert(self, stateElement, length: int = 0):
        listFeature: [] = self._convert_to_list_feature(stateElement=stateElement)
        return self._padding_to_length(listFeature=listFeature, length=length)

    def _convert_to_list_feature(self, stateElement) -> []:
        pass

    def _padding_to_length(self, listFeature: [], length: int):
        while len(listFeature) < length:
            listFeature.append(0)

        if len(listFeature) > length and length != 0:
            return listFeature[:length]

        return listFeature
