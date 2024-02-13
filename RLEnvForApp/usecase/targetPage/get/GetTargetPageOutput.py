# GetTargetPage
from RLEnvForApp.usecase.targetPage.dto.TargetPageDTO import TargetPageDTO


class GetTargetPageOutput:
    def __init__(self):
        self._target_page_dto: TargetPageDTO = None

    def set_target_page_dto(self, target_page_dto: TargetPageDTO):
        self._target_page_dto = target_page_dto

    def get_target_page_dto(self) -> TargetPageDTO:
        return self._target_page_dto
