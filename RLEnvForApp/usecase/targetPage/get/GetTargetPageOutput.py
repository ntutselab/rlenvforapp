# GetTargetPage
from RLEnvForApp.usecase.targetPage.dto.TargetPageDTO import TargetPageDTO


class GetTargetPageOutput:
    def __init__(self):
        self._targetPageDTO: TargetPageDTO = None

    def set_target_page_dto(self, targetPageDTO: TargetPageDTO):
        self._targetPageDTO = targetPageDTO

    def get_target_page_dto(self) -> TargetPageDTO:
        return self._targetPageDTO
