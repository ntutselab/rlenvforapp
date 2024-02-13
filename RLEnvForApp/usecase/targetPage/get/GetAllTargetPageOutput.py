from RLEnvForApp.usecase.targetPage.dto.TargetPageDTO import TargetPageDTO


class GetAllTargetPageOutput:
    def __init__(self):
        self._target_page_dt_os: [TargetPageDTO] = []

    def set_target_page_dt_os(self, target_page_dt_os: [TargetPageDTO]):
        self._target_page_dt_os = target_page_dt_os

    def get_target_page_dt_os(self) -> [TargetPageDTO]:
        return self._target_page_dt_os
