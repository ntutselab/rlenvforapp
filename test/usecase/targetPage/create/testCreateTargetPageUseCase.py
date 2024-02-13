import unittest

from RLEnvForApp.adapter.repository.targetPage.InMemoryTargetPageRepository import \
    InMemoryTargetPageRepository
from RLEnvForApp.domain.targetPage.Directive import Directive
from RLEnvForApp.usecase.environment.autOperator.dto.CodeCoverageDTO import \
    CodeCoverageDTO
from RLEnvForApp.usecase.targetPage.create import (CreateTargetPageInput,
                                                   CreateTargetPageOutput,
                                                   CreateTargetPageUseCase)
from RLEnvForApp.usecase.targetPage.dto import AppEventDTO
from RLEnvForApp.usecase.targetPage.dto.DirectiveDTO import DirectiveDTO
from RLEnvForApp.usecase.targetPage.entity.TargetPageEntity import \
    TargetPageEntity
from RLEnvForApp.usecase.targetPage.mapper import TargetPageEntityMapper


class testCreateTargetPageUseCase(unittest.TestCase):
    def set_up(self) -> None:
        self._repository = InMemoryTargetPageRepository()

    def test_create_target_page(self):
        target_page_url = "./register.html"
        root_url = "./"
        create_target_page_use_case = CreateTargetPageUseCase.CreateTargetPageUseCase(
            repository=self._repository)
        create_target_page_input = CreateTargetPageInput.CreateTargetPageInput(
            target_page_url=target_page_url, root_url=root_url, app_event_dt_os=[])
        create_target_page_output = CreateTargetPageOutput.CreateTargetPageOutput()
        create_target_page_use_case.execute(
            create_target_page_input, create_target_page_output)

        target_page_entity: TargetPageEntity = self._repository.find_by_id(
            create_target_page_output.get_id())
        target_page = TargetPageEntityMapper.mapping_target_page_from(
            target_page_entity=target_page_entity)

        self.assertEqual(target_page.get_id(), create_target_page_output.get_id())

    def test_create_target_page_with_app_event(self):
        target_page_url = "./register.html"
        root_url = "./"
        app_event_dto = AppEventDTO.AppEventDTO(
            xpath="/HTML[1]/BODY[1]/DIV[1]/FORM[1]/DIV[4]/DIV[2]/P[1]/A[2]", value="")

        create_target_page_use_case = CreateTargetPageUseCase.CreateTargetPageUseCase(
            repository=self._repository)
        create_target_page_input = CreateTargetPageInput.CreateTargetPageInput(
            target_page_url=target_page_url, root_url=root_url, app_event_dt_os=[app_event_dto])
        create_target_page_output = CreateTargetPageOutput.CreateTargetPageOutput()

        create_target_page_use_case.execute(
            create_target_page_input, create_target_page_output)

        target_page_entity: TargetPageEntity = self._repository.find_by_id(
            create_target_page_output.get_id())
        target_page = TargetPageEntityMapper.mapping_target_page_from(
            target_page_entity=target_page_entity)
        self.assertEqual(
            target_page.get_app_events()[0].get_xpath(),
            "/HTML[1]/BODY[1]/DIV[1]/FORM[1]/DIV[4]/DIV[2]/P[1]/A[2]")

    def test_create_target_page_for_ai_guide(self):
        target_page_url = "./register.html"
        root_url = "./"
        app_event_dto = AppEventDTO.AppEventDTO(
            xpath="/HTML[1]/BODY[1]/DIV[1]/FORM[1]/DIV[4]/DIV[2]/P[1]/A[2]", value="")
        task_id = "testTaskID"
        original_code_coverage_dto = CodeCoverageDTO(
            code_coverage_type="statement", code_coverage_vector=[
                1, 0, 1, 0, 1, 0, 1, 0, 1, 0])
        code_coverage_dto = CodeCoverageDTO(
            code_coverage_type="statement", code_coverage_vector=[
                1, 1, 1, 1, 1, 0, 0, 0, 0, 0])
        directive_dto = DirectiveDTO(
            app_event_dt_os=[app_event_dto],
            code_coverage_dt_os=[code_coverage_dto])

        create_target_page_use_case = CreateTargetPageUseCase.CreateTargetPageUseCase(
            repository=self._repository)
        create_target_page_input = CreateTargetPageInput.CreateTargetPageInput(target_page_url=target_page_url,
                                                                            root_url=root_url,
                                                                            app_event_dt_os=[
                                                                                app_event_dto],
                                                                            task_id=task_id,
                                                                            basic_code_coverage=original_code_coverage_dto,
                                                                            directive_dt_os=[directive_dto])
        create_target_page_output = CreateTargetPageOutput.CreateTargetPageOutput()
        create_target_page_use_case.execute(
            create_target_page_input, create_target_page_output)

        target_page_entity: TargetPageEntity = self._repository.find_by_id(
            create_target_page_output.get_id())
        self.assertEqual(len(target_page_entity.get_directive_entities()), 1)

        target_page = TargetPageEntityMapper.mapping_target_page_from(
            target_page_entity=target_page_entity)
        self.assertEqual(
            target_page.get_app_events()[0].get_xpath(),
            "/HTML[1]/BODY[1]/DIV[1]/FORM[1]/DIV[4]/DIV[2]/P[1]/A[2]")
        self.assertEqual(target_page.get_root_url(), root_url)
        self.assertEqual(target_page.get_target_url(), target_page_url)
        self.assertEqual(target_page.get_task_id(), task_id)
        self.assertEqual(
            target_page.get_basic_code_coverage_dto().get_code_coverage_vector(), [
                1, 0, 1, 0, 1, 0, 1, 0, 1, 0])
        self.assertEqual(len(target_page.get_directives()), 1)
        directive: Directive = target_page.get_directives()[0]
        self.assertEqual(
            directive.get_code_coverages()[0].get_code_coverage_type(),
            directive_dto.get_code_coverage_dt_os()[0].get_code_coverage_type())
        self.assertEqual(
            directive.get_code_coverages()[0].get_code_coverage_vector(),
            directive_dto.get_code_coverage_dt_os()[0].get_code_coverage_vector())
        self.assertEqual(
            directive.get_app_events()[0].get_xpath(),
            app_event_dto.get_xpath())
        self.assertEqual(
            directive.get_app_events()[0].get_value(),
            app_event_dto.get_value())
