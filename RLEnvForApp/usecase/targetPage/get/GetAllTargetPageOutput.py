from RLEnvForApp.usecase.targetPage.dto.TargetPageDTO import TargetPageDTO


class GetAllTargetPageOutput:
    def __init__(self):
        self._targetPageDTOs: [TargetPageDTO] = []

    def setTargetPageDTOs(self, targetPageDTOs: [TargetPageDTO]):
        self._targetPageDTOs = targetPageDTOs

    def getTargetPageDTOs(self) -> [TargetPageDTO]:
        return self._targetPageDTOs