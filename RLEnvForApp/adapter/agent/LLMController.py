import torch
from dependency_injector.wiring import inject
from RLEnvForApp.adapter.agent.model.builder.PromptModelBuilder import PromptModelBuilder
from RLEnvForApp.adapter.agent.model.builder.PromptModelDirector import PromptModelDirector
from RLEnvForApp.adapter.targetPagePort.factory.TargetPagePortFactory import TargetPagePortFactory


class LLMController:

    @inject
    def __init__(self):
        self.__server_name = "timeoff_management_with_coverage"
        self.__application_ip = "127.0.0.1"
        self.__application_port = 3100
        self._code_coverage_type = "statement coverage"
        self.__target_page_port = TargetPagePortFactory().createAIGuideTargetPagePort(javaIp="127.0.0.1",
                                                                                      pythonIp="127.0.0.1",
                                                                                      javaPort=2700, pythonPort=2701,
                                                                                      serverName=self.__server_name,
                                                                                      rootUrl=f"http://{self.__application_ip}:{self.__application_port}/",
                                                                                      codeCoverageType=self._code_coverage_type)
        self.__target_page_port.connect()
        self.__target_page_port.waitForTargetPage()

    def play(self):
        prompt_model_builder = PromptModelBuilder()
        prompt_model = PromptModelDirector().make_my_research(prompt_model_builder)
        # check cuda
        if torch.cuda.is_available():
            prompt_model = prompt_model.cuda()
