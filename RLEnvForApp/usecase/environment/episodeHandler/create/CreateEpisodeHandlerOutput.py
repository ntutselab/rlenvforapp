class CreateEpisodeHandlerOutput:
    def __init__(self):
        self._id = ""
        self._index = -1

    def setId(self, id: str):
        self._id = id

    def getId(self):
        return self._id

    def setIndex(self, index: int):
        self._index = index

    def getIndex(self):
        return self._index
