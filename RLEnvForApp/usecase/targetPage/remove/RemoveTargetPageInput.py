class RemoveTargetPageInput:
    def __init__(self, targetPageId: str):
        self._targetPageId = targetPageId

    def getTargetPageId(self):
        return self._targetPageId
