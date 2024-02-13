class RemoveTargetPageInput:
    def __init__(self, target_page_id: str):
        self._target_page_id = target_page_id

    def get_target_page_id(self):
        return self._target_page_id
