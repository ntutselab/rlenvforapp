# GetTargetPage

class GetTargetPageInput:
    def __init__(self, targetPageId: str):
        self._targetPageId = targetPageId

    def getTargetPageId(self) -> str:
        return self._targetPageId