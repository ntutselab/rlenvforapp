from RLEnvForApp.usecase.repository import TargetPageRepository
from RLEnvForApp.usecase.targetPage.create import (CreateTargetPageInput,
                                                   CreateTargetPageOutput,
                                                   CreateTargetPageUseCase)
from RLEnvForApp.usecase.targetPage.dto.AppEventDTO import AppEventDTO


class TargetPageHierarchyInitial:
    def __init__(self):
        pass

    def create_target_page(self, targetPageRepository: TargetPageRepository.TargetPageRepository,
                         target_page_url: str, root_url: str, app_event_dt_os: [AppEventDTO]):
        create_target_page_use_case = CreateTargetPageUseCase.CreateTargetPageUseCase(
            repository=targetPageRepository)
        create_target_page_input = CreateTargetPageInput.CreateTargetPageInput(target_page_url=target_page_url,
                                                                            root_url=root_url,
                                                                            app_event_dt_os=app_event_dt_os)
        create_target_page_output = CreateTargetPageOutput.CreateTargetPageOutput()
        create_target_page_use_case.execute(
            create_target_page_input, create_target_page_output)

        return create_target_page_output.get_id()
