class RemoveTargetPageInput:
    def __init__(self, targetPageId: str):
        self._targetPageId = targetPageId

    def get_target_page_id(self):
        return self._targetPageId
