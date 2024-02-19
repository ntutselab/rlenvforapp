import os
import sys

from RLEnvForApp.adapter.agent.RLController import RLController
from RLEnvForApp.adapter.environment.gym import *
from RLEnvForApp.adapter.environment.gym import AIGuideEnvironment
from RLEnvForApp.usecase.applicationUnderTest.start.StartApplicationUnderTestUserCase import \
    StartApplicationUnderTestUserCase
from RLEnvForApp.usecase.applicationUnderTest.stop.StopApplicationUnderTestUseCase import \
    StopApplicationUnderTestUseCase
from RLEnvForApp.usecase.environment.episodeHandler.get.GetEpisodeHandlerUseCase import GetEpisodeHandlerUseCase
from RLEnvForApp.usecase.targetPage.ITargetIndicationService.GUIDEIndicationService import GUIDEIndicationService
from RLEnvForApp.usecase.targetPage.create import *
from RLEnvForApp.usecase.environment.executeAction import *
from RLEnvForApp.usecase.environment.initiateEnvironment import *
from RLEnvForApp.usecase.environment.resetEnvironment import *
from RLEnvForApp.usecase.targetPage.get.GetAllTargetPageUseCase import GetAllTargetPageUseCase
from RLEnvForApp.usecase.targetPage.get.GetTargetPageUseCase import GetTargetPageUseCase
from RLEnvForApp.usecase.targetPage.remove.RemoveTargetPageUseCase import RemoveTargetPageUseCase
from RLEnvForApp.usecase.targetPage.update.UpdateTargetPageUseCase import UpdateTargetPageUseCase
from configuration.di.AgentDIContainers import AgentDIContainers
from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers
from RLEnvForApp.logger.logger import Logger


def setDIContainer():
    envContainer = EnvironmentDIContainers()
    agentContainer = AgentDIContainers()
    envContainer.wire(
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
    agentContainer.wire(
        modules=[sys.modules[__name__], RLController])


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

        setDIContainer()
        # controller = RLController(algorithm="DQN", policy=DQNCustomPolicy)
        controller = RLController(algorithm="Monkey", policy=None)

        # =======training phase=======
        # controller.learnModel(totalTimesteps=toTalTimeStep, modelDir=modelDir, modelSeriesName=modelName)
        # verifyModel(modelPath=os.path.join(modelDir, modelName + "_" + str(toTalTimeStep) + "step.zip"), verifyTimes=74)

        # =======verify phase=======
        controller.verifyModelByTotalStep(modelPath=os.path.join(modelDir, modelName),
                                          totalStep=toTalTimeStep, explorationEpisodeEsp=explorationEpisodeEsp, explorationStepEsp=explorationStepEsp)

        # =======final verify phase=======
        # controller.verifyModelByTime(modelPath=os.path.join(modelDir, modelName),
        #                              timeLimit=int(verifyTime * 3600),
        #                              explorationEpisodeEsp=explorationEpisodeEsp, explorationStepEsp=explorationStepEsp)

        Logger._instance = None
