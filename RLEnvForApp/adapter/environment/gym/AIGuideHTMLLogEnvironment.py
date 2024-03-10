import gym
import numpy
from dependency_injector.wiring import Provide, inject

from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers
from RLEnvForApp.adapter.environment.autOperator.crawler.HTMLLogCrawler import HTMLLogCrawler
from RLEnvForApp.adapter.targetPagePort.factory.TargetPagePortFactory import TargetPagePortFactory
from RLEnvForApp.logger.logger import Logger
from RLEnvForApp.usecase.environment.autOperator.AIGUIDEOperator import AIGUIDEOperator
from RLEnvForApp.usecase.environment.executeAction import (ExecuteActionInput, ExecuteActionOutput,
                                                           ExecuteActionUseCase)
from RLEnvForApp.usecase.environment.initiateEnvironment import (InitiateEnvironmentInput,
                                                                 InitiateEnvironmentOutput,
                                                                 InitiateEnvironmentUseCase)
from RLEnvForApp.usecase.environment.resetEnvironment import (ResetEnvironmentInput,
                                                              ResetEnvironmentOutput,
                                                              ResetEnvironmentUseCase)
from RLEnvForApp.usecase.repository.EpisodeHandlerRepository import EpisodeHandlerRepository


class AIGuideHTMLLogEnvironment(gym.Env):
    @inject
    def __init__(self, episodeHandlerRepository: EpisodeHandlerRepository = Provide[EnvironmentDIContainers.episodeHandlerRepository]):
        self._logger = Logger()
        self._logger.info('Init environment.Env')
        self._application_ip = "127.0.0.1"
        self._application_port = 3100

        self._episode_handler_repository = episodeHandlerRepository

        self._crawler = HTMLLogCrawler()
        self._aut_operator = AIGUIDEOperator(crawler=self._crawler)

        self._target_page_port = TargetPagePortFactory().createAIGuideHTMLLogTargetPagePort(
            folderPath="htmlSet/GUIDE_HTML_SET")

        self._target_page_id = ""
        self._episode_handler_id = ""
        self._episode_index = 0
        self._step_number = 1
        self._total_step = 1
        self._episode_reward = 0
        self._steps_information = ""
        self._original_observation = {}

        initiate_env_use_case = InitiateEnvironmentUseCase.InitiateEnvironmentUseCase()
        initiate_env_input = InitiateEnvironmentInput.InitiateEnvironmentInput()
        initiate_env_output = InitiateEnvironmentOutput.InitiateEnvironmentOutput()
        initiate_env_use_case.execute(input=initiate_env_input, output=initiate_env_output)

        self._observation_shape = initiate_env_output.getObservationSize()

        self.action_space = gym.spaces.Discrete(initiate_env_output.getActionSpaceSize())
        self.observation_space = gym.spaces.Box(low=-numpy.inf,
                                                high=numpy.inf,
                                                shape=self._observation_shape,
                                                dtype=numpy.float32)

        self._target_page_port.connect()
        self._target_page_port.waitForTargetPage()

    def step(self, action):
        if self._aut_operator.getFocusedAppElement() is None:
            focus_element_xpath = ""
        else:
            focus_element_xpath = self._aut_operator.getFocusedAppElement().getXpath()

        execute_action_use_case = ExecuteActionUseCase.ExecuteActionUseCase(
            autOperator=self._aut_operator)
        execute_action_input = ExecuteActionInput.ExecuteActionInput(actionNumber=int(action),
                                                                     episodeHandlerId=self._episode_handler_id)
        execute_action_output = ExecuteActionOutput.ExecuteActionOutput()
        execute_action_use_case.execute(input=execute_action_input, output=execute_action_output)

        self._steps_information = "total_step:" + f"{self._total_step:4}" + \
                                 "\tStep:" + f"{self._step_number:2}" + \
                                 "\tEpisode:" + str(self._episode_index) + \
                                 "\tAction:" + f"{int(action):2}" + \
                                 "\tReward:" + f"{execute_action_output.getReward(): 4.3f}" + \
                                 "\tFocusElement: " + str(self._original_observation).ljust(64) + \
                                 "\tXpath: " + focus_element_xpath + \
                                  "\tCodeCoverage:" + str(execute_action_output.getCodeCoverageDict())
        observation = numpy.array(execute_action_output.getObservation())
        observation.resize(self._observation_shape)
        self._episode_reward += execute_action_output.getReward()
        self._step_number += 1
        self._total_step += 1

        self._logger.info(self._steps_information)

        self._original_observation = execute_action_output.getOriginalObservation()
        self._original_observation = self._stripDictionaryContents(self._original_observation)
        return observation, execute_action_output.getReward(), execute_action_output.getIsDone(), {
            "Reward": execute_action_output.getReward()}

    def reset(self):
        self._logger.info("Episode reward:" + f"{self._episode_reward:3}")
        self._steps_information = ""
        self._episode_reward = 0

        self._logger.info("\n\n=======================Reset environment.Env=======================")
        self._episode_index += 1
        self._step_number = 1

        reset_env_use_case = ResetEnvironmentUseCase.ResetEnvironmentUseCase(
            operator=self._aut_operator)
        reset_env_use_input = ResetEnvironmentInput.ResetEnvironmentInput(
            episodeIndex=self._episode_index)
        reset_env_use_output = ResetEnvironmentOutput.ResetEnvironmentOutput()
        reset_env_use_case.execute(input=reset_env_use_input, output=reset_env_use_output)

        self._logger.info("Episode Handler Amount:" +
                          f"{len(self._episode_handler_repository.findAll()):2}")
        self._logger.info("Target page url is: " + reset_env_use_output.getTargetPageUrl())
        self._logger.info("==========================================================\n\n")

        self._episode_handler_id = reset_env_use_output.getEpisodeHandlerId()
        self._target_page_id = reset_env_use_output.getTargetPageId()
        observation = numpy.array(reset_env_use_output.getObservation())
        observation.resize(self._observation_shape)

        self._original_observation = reset_env_use_output.getOriginalObservation()
        self._original_observation = self._stripDictionaryContents(self._original_observation)
        return observation

    def close(self):
        self._crawler.close()
        self._logger.info("close environment.Env")

    def render(self):
        pass

    def _stripDictionaryContents(self, dictionary: dict):
        for key in dictionary:
            dictionary[key] = str(dictionary[key]).strip()

        return dictionary
