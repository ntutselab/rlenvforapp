from RLEnvForApp.usecase.targetPage.dto.TargetPageDTO import TargetPageDTO


class GetAllTargetPageOutput:
    def __init__(self):
        self._targetPageDTOs: [TargetPageDTO] = []

    def set_target_page_dt_os(self, targetPageDTOs: [TargetPageDTO]):
        self._targetPageDTOs = targetPageDTOs

    def get_target_page_dt_os(self) -> [TargetPageDTO]:
        return self._targetPageDTOs
