class StopApplicationUnderTestInput:
    def __init__(self, id):
        self._Id = id

    def get_id(self):
        return self._Id
