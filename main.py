import os
import sys

from configuration.di.AgentDIContainers import AgentDIContainers
from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers
from RLEnvForApp.adapter.agent.RLController import RLController
from RLEnvForApp.adapter.environment.gym import (AIGuideEnvironment,
                                                 AIGuideHTMLLogEnvironment)
from RLEnvForApp.logger.logger import Logger
from RLEnvForApp.usecase.applicationUnderTest.start.StartApplicationUnderTestUserCase import \
    StartApplicationUnderTestUserCase
from RLEnvForApp.usecase.applicationUnderTest.stop.StopApplicationUnderTestUseCase import \
    StopApplicationUnderTestUseCase
from RLEnvForApp.usecase.environment.episodeHandler.get.GetEpisodeHandlerUseCase import \
    GetEpisodeHandlerUseCase
from RLEnvForApp.usecase.environment.executeAction import ExecuteActionUseCase
from RLEnvForApp.usecase.environment.initiateEnvironment import \
    InitiateEnvironmentUseCase
from RLEnvForApp.usecase.environment.resetEnvironment import \
    ResetEnvironmentUseCase
from RLEnvForApp.usecase.targetPage.create import (CreateDirectiveUseCase,
                                                   CreateTargetPageUseCase)
from RLEnvForApp.usecase.targetPage.get.GetAllTargetPageUseCase import \
    GetAllTargetPageUseCase
from RLEnvForApp.usecase.targetPage.get.GetTargetPageUseCase import \
    GetTargetPageUseCase
from RLEnvForApp.usecase.targetPage.ITargetIndicationService.GUIDEIndicationService import \
    GUIDEIndicationService
from RLEnvForApp.usecase.targetPage.remove.RemoveTargetPageUseCase import \
    RemoveTargetPageUseCase
from RLEnvForApp.usecase.targetPage.update.UpdateTargetPageUseCase import \
    UpdateTargetPageUseCase

controller: RLController = None


def set_di_container():
    env_container = EnvironmentDIContainers()
    agent_container = AgentDIContainers()
    env_container.wire(
        modules=[sys.modules[__name__],
                 AIGuideEnvironment.AIGuideEnvironment,
                 AIGuideHTMLLogEnvironment.AIGuideHTMLLogEnvironment,
                 GUIDEIndicationService,
                 CreateTargetPageUseCase,
                 RemoveTargetPageUseCase,
                 GetTargetPageUseCase,
                 GetAllTargetPageUseCase,
                 CreateDirectiveUseCase,
                 InitiateEnvironmentUseCase,
                 ExecuteActionUseCase,
                 ResetEnvironmentUseCase,
                 UpdateTargetPageUseCase,
                 GetEpisodeHandlerUseCase,
                 StartApplicationUnderTestUserCase,
                 StopApplicationUnderTestUseCase])
    agent_container.wire(
        modules=[sys.modules[__name__], RLController])


def get_all_file_path_in_folder(targetFolderPath: str):
    file_paths = []
    for dir_path, dirNames, fileNames in os.walk(targetFolderPath):
        for file in fileNames:
            file_paths.append(dir_path + "/" + file)
    return file_paths


def verify_model(model_path: str, verifyTimes):
    episode_reward_list = controller.verify_model(model_path, verifyTimes)
    success_times = 0
    for i in episode_reward_list:
        if i > 100:
            success_times += 1
    model_result = model_path + " model success times:" + str(success_times)
    Logger().info(model_result)
    return model_result


def verify_all_model(MODEL_DIR: str):
    model_results = []
    for model_path in get_all_file_path_in_folder(MODEL_DIR):
        episode_reward_list = controller.verify_model(model_path, 10)
        success_times = 0
        for i in episode_reward_list:
            if i > 100:
                success_times += 1
        model_result = model_path + " model success times:" + str(success_times)
        Logger().info(model_result)
        model_results.append(model_result)

    Logger().info("====================")
    for result in model_results:
        Logger().info(result)


if __name__ == '__main__':
    VERIFY_TIME = 0.5

    # These two parameters determine whether the agent will choose actions randomly.
    # For details, refer to chapter 3.3.1 of "Jiun-Kai Huang - Training a Reinforcement Learning Agent to Support Crawling of Different Web Applications".
    # In my research, I don't care Code coverage, but focused on filling out
    # the form successfully, so I set them to -1. by Chuang-chen chiu
    EXPLORATION_EPISODE_ESP = -1
    EXPLORATION_STEP_ESP = -1

    TO_TAL_TIME_STEP = 10000
    MODEL_DIR = "model/model"

    modelNames = [""]

    for model_name in modelNames:
        COMMENT = ''
        logger = Logger(f"{comment}_{modelName}.log")
        Logger().info(f"{comment}_{modelName}")

        set_di_container()
        # controller = RLController(algorithm="DQN", policy=DQNCustomPolicy)
        controller = RLController(algorithm="Monkey", policy=None)

        # =======training phase=======
        # controller.learnModel(totalTimesteps=toTalTimeStep, modelDir=modelDir, modelSeriesName=modelName)
        # verifyModel(modelPath=os.path.join(modelDir, modelName + "_" + str(toTalTimeStep) + "step.zip"), verifyTimes=74)

        # =======verify phase=======
        controller.verify_model_by_total_step(model_path=os.path.join(MODEL_DIR, model_name),
                                          totalStep=TO_TAL_TIME_STEP, exploration_episode_esp=EXPLORATION_EPISODE_ESP, exploration_step_esp=EXPLORATION_STEP_ESP)

        # =======final verify phase=======
        # controller.verifyModelByTime(modelPath=os.path.join(modelDir, modelName),
        #                              timeLimit=int(verifyTime * 3600),
        # explorationEpisodeEsp=explorationEpisodeEsp,
        # explorationStepEsp=explorationStepEsp)

        Logger._instance = None
