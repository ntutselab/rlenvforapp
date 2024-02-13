class IConverter:
    def __init__(self):
        pass

    def convert(self, state_element, length: int = 0):
        list_feature: [] = self._convert_to_list_feature(state_element=state_element)
        return self._padding_to_length(list_feature=list_feature, length=length)

    def _convert_to_list_feature(self, state_element) -> []:
        pass

    def _padding_to_length(self, list_feature: [], length: int):
        while len(list_feature) < length:
            list_feature.append(0)

        if len(list_feature) > length and length != 0:
            return list_feature[:length]

        return list_feature
