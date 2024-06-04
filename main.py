import os
import sys

from configuration.di.AgentDIContainers import AgentDIContainers
from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers
# from RLEnvForApp.adapter.agent.RLController import RLController
from RLEnvForApp.adapter.environment.gym import AIGuideEnvironment, AIGuideHTMLLogEnvironment
from RLEnvForApp.logger.logger import Logger
from RLEnvForApp.usecase.applicationUnderTest.start import StartApplicationUnderTestUserCase
from RLEnvForApp.usecase.applicationUnderTest.stop import StopApplicationUnderTestUseCase
from RLEnvForApp.usecase.environment.episodeHandler.get import GetEpisodeHandlerUseCase
from RLEnvForApp.usecase.environment.executeAction import ExecuteActionUseCase
from RLEnvForApp.usecase.environment.initiateEnvironment import InitiateEnvironmentUseCase
from RLEnvForApp.usecase.environment.resetEnvironment import ResetEnvironmentUseCase
from RLEnvForApp.usecase.targetPage.create import (CreateDirectiveUseCase, CreateTargetPageUseCase,
                                                   CreateFakeDirectiveUseCase)
from RLEnvForApp.usecase.targetPage.get import GetAllTargetPageUseCase
from RLEnvForApp.usecase.targetPage.get import GetTargetPageUseCase
from RLEnvForApp.usecase.targetPage.ITargetIndicationService import GUIDEIndicationService
from RLEnvForApp.usecase.targetPage.remove import RemoveTargetPageUseCase
from RLEnvForApp.usecase.targetPage.update import UpdateTargetPageUseCase
from RLEnvForApp.adapter.agent.LLMController import LLMController

# controller: RLController = None


def setDIContainer():
    from RLEnvForApp.adapter.agent import LLMController
    envContainer = EnvironmentDIContainers()
    agentContainer = AgentDIContainers()
    envContainer.wire(
        modules=[sys.modules[__name__],
                 AIGuideEnvironment,
                 AIGuideHTMLLogEnvironment,
                 GUIDEIndicationService,
                 CreateTargetPageUseCase,
                 RemoveTargetPageUseCase,
                 GetTargetPageUseCase,
                 GetAllTargetPageUseCase,
                 CreateDirectiveUseCase,
                 CreateFakeDirectiveUseCase,
                 InitiateEnvironmentUseCase,
                 ExecuteActionUseCase,
                 ResetEnvironmentUseCase,
                 UpdateTargetPageUseCase,
                 GetEpisodeHandlerUseCase,
                 StartApplicationUnderTestUserCase,
                 StopApplicationUnderTestUseCase,
                 LLMController])
    # agentContainer.wire(
    #     modules=[sys.modules[__name__], RLController])


def getAllFilePathInFolder(targetFolderPath: str):
    filePaths = []
    for dirPath, dirNames, fileNames in os.walk(targetFolderPath):
        for file in fileNames:
            filePaths.append(dirPath + "/" + file)
    return filePaths


def verifyModel(modelPath: str, verifyTimes):
    episodeRewardList = controller.verifyModel(modelPath, verifyTimes)
    successTimes = 0
    for i in episodeRewardList:
        if i > 100:
            successTimes += 1
    modelResult = modelPath + " model success times:" + str(successTimes)
    Logger().info(modelResult)
    return modelResult


def verifyAllModel(modelDir: str):
    modelResults = []
    for modelPath in getAllFilePathInFolder(modelDir):
        episodeRewardList = controller.verifyModel(modelPath, 10)
        successTimes = 0
        for i in episodeRewardList:
            if i > 100:
                successTimes += 1
        modelResult = modelPath + " model success times:" + str(successTimes)
        Logger().info(modelResult)
        modelResults.append(modelResult)

    Logger().info("====================")
    for result in modelResults:
        Logger().info(result)


if __name__ == '__main__':
    setDIContainer()
    verifyTime = 0.5

    # These two parameters determine whether the agent will choose actions randomly.
    # For details, refer to chapter 3.3.1 of "Jiun-Kai Huang - Training a Reinforcement Learning Agent to Support Crawling of Different Web Applications".
    # In my research, I don't care Code coverage, but focused on filling out the form successfully, so I set them to -1. by Chuang-chen chiu
    explorationEpisodeEsp = -1
    explorationStepEsp = -1

    toTalTimeStep = 10000
    modelDir = "model/model"

    modelNames = [""]

    for modelName in modelNames:
        comment = ''
        logger = Logger(f"{comment}_{modelName}.log")
        Logger().info(f"{comment}_{modelName}")

        llm_controller = LLMController()
        llm_controller.play()
        # controller = RLController(algorithm="DQN", policy=DQNCustomPolicy)
        # controller = RLController(algorithm="Monkey", policy=None)

        # =======training phase=======
        # controller.learnModel(totalTimesteps=toTalTimeStep, modelDir=modelDir, modelSeriesName=modelName)
        # verifyModel(modelPath=os.path.join(modelDir, modelName + "_" + str(toTalTimeStep) + "step.zip"), verifyTimes=74)

        # =======verify phase=======
        # controller.verifyModelByTotalStep(modelPath=os.path.join(modelDir, modelName),
        # totalStep=toTalTimeStep, explorationEpisodeEsp=explorationEpisodeEsp, explorationStepEsp=explorationStepEsp)

        # =======final verify phase=======
        # controller.verifyModelByTime(modelPath=os.path.join(modelDir, modelName),
        #                              timeLimit=int(verifyTime * 3600),
        #                              explorationEpisodeEsp=explorationEpisodeEsp, explorationStepEsp=explorationStepEsp)

        # Logger._instance = None
