class CreateEpisodeHandlerOutput:
    def __init__(self):
        self._id = ""
        self._index = -1

    def set_id(self, id: str):
        self._id = id

    def get_id(self):
        return self._id

    def set_index(self, index: int):
        self._index = index

    def get_index(self):
        return self._index
