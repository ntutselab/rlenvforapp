# GetTargetPage
from RLEnvForApp.usecase.targetPage.dto.TargetPageDTO import TargetPageDTO


class GetTargetPageOutput:
    def __init__(self):
        self._targetPageDTO: TargetPageDTO = None

    def setTargetPageDTO(self, targetPageDTO: TargetPageDTO):
        self._targetPageDTO = targetPageDTO

    def getTargetPageDTO(self) -> TargetPageDTO:
        return self._targetPageDTO
