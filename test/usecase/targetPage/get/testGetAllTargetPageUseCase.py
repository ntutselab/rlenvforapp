import unittest

from RLEnvForApp.adapter.repository.targetPage.InMemoryTargetPageRepository import \
    InMemoryTargetPageRepository
from RLEnvForApp.usecase.environment.autOperator.dto.CodeCoverageDTO import \
    CodeCoverageDTO
from RLEnvForApp.usecase.targetPage.create import (CreateTargetPageInput,
                                                   CreateTargetPageOutput,
                                                   CreateTargetPageUseCase)
from RLEnvForApp.usecase.targetPage.dto.AppEventDTO import AppEventDTO
from RLEnvForApp.usecase.targetPage.dto.DirectiveDTO import DirectiveDTO
from RLEnvForApp.usecase.targetPage.get import (GetAllTargetPageInput,
                                                GetAllTargetPageOutput,
                                                GetAllTargetPageUseCase)


class MyTestCase(unittest.TestCase):
    def set_up(self) -> None:
        self._repository = InMemoryTargetPageRepository()
        self._target_page_url = "./register.html"
        self._root_url = "./"
        self._task_id = "testTaskID"
        self._app_event_dto = AppEventDTO(
            xpath="/HTML[1]/BODY[1]/DIV[1]/FORM[1]/DIV[4]/DIV[2]/P[1]/A[2]", value="")
        self._original_code_coverage_dto = CodeCoverageDTO(
            code_coverage_type="statement", code_coverage_vector=[
                1, 0, 1, 0, 1, 0, 1, 0, 1, 0])
        code_coverage_dto = CodeCoverageDTO(
            code_coverage_type="statement", code_coverage_vector=[
                1, 1, 1, 1, 1, 0, 0, 0, 0, 0])
        self._directive_dto = DirectiveDTO(
            app_event_dt_os=[
                self._app_event_dto],
            code_coverage_dt_os=[code_coverage_dto])

        create_target_page_use_case = CreateTargetPageUseCase.CreateTargetPageUseCase(
            repository=self._repository)
        create_target_page_input = CreateTargetPageInput.CreateTargetPageInput(target_page_url=self._target_page_url,
                                                                            root_url=self._root_url,
                                                                            app_event_dt_os=[
                                                                                self._app_event_dto],
                                                                            task_id=self._task_id,
                                                                            basic_code_coverage=self._original_code_coverage_dto,
                                                                            directive_dt_os=[self._directive_dto])
        create_target_page_output = CreateTargetPageOutput.CreateTargetPageOutput()
        create_target_page_use_case.execute(
            create_target_page_input, create_target_page_output)
        self._target_page_id = create_target_page_output.get_id()

    def test_get_all_target_page(self):
        get_all_target_page_use_case = GetAllTargetPageUseCase.GetAllTargetPageUseCase(
            repository=self._repository)
        get_all_target_page_input = GetAllTargetPageInput.GetAllTargetPageInput()
        get_all_target_page_output = GetAllTargetPageOutput.GetAllTargetPageOutput()

        get_all_target_page_use_case.execute(
            input=get_all_target_page_input,
            output=get_all_target_page_output)

        self.assertEqual(1, len(get_all_target_page_output.get_target_page_dt_os()))
