import os
import time

from dependency_injector.wiring import inject

from RLEnvForApp.adapter.agent.model.ModelController import ModelController
from RLEnvForApp.adapter.agent.model.ModelFactory import ModelFactory
from RLEnvForApp.adapter.environment.factory.GymEnvironmentFactory import GymEnvironmentFactory
from RLEnvForApp.logger.logger import Logger

class RLController:
    @inject
    def __init__(self, algorithm, policy):
        Logger().info(f"Algorithm: {algorithm}")
        self._algorithm = algorithm
        self._policy = policy
        self._environmentFactory = GymEnvironmentFactory()

    def learnModel(self, totalTimesteps: int, modelDir: str, modelSeriesName: str, tensorboardPath: str="model/log"):
        environment = self._environmentFactory.createEnvironment()
        modelController = ModelController()
        modelController.setModel(
            ModelFactory().createModel(algorithm=self._algorithm, policy=self._policy, environment=environment,
                                       tensorboardPath="model/log"))
        modelController.learn(totalTimeSteps=totalTimesteps)
        modelName = modelSeriesName + "_" + str(totalTimesteps) + "step"

        modelController.save(os.path.join(modelDir, modelName))
        environment.close()

    def learnModelByExitedModel(self, totalTimesteps: int, modelDir: str, modelSeriesName: str, modelPath: str):
        environment = self._environmentFactory.createEnvironment()
        modelController = ModelController()
        modelController.setModel(ModelFactory().loadModel(algorithm=self._algorithm, modelPath=modelPath, environment=environment))
        modelController.learn(totalTimeSteps=totalTimesteps)
        modelName = modelSeriesName + "_" + str(totalTimesteps) + "step"

        modelController.save(os.path.join(modelDir, modelName))
        environment.close()

    def iterateLearnModel(self, timestepsPerIteration: int, iterationTimes: int, modelDir: str, modelSeriesName: str, tensorboardPath: str="model/log"):
        environment = self._environmentFactory.createEnvironment()
        modelController = ModelController().setModel(
            ModelFactory().createModel(algorithm=self._algorithm, policy=self._policy, environment=environment,
                                       tensorboardPath="model/log"))
        for i in range(iterationTimes):
            modelController.learn(totalTimeSteps=timestepsPerIteration)
            modelName = modelSeriesName + "_" + str(timestepsPerIteration * (i + 1)) + "step"

            modelController.save(os.path.join(modelDir, modelName))

    def verifyModel(self, modelPath: str, verifyTimes: int):
        episodeRewardList = []
        environment = self._environmentFactory.createEnvironment()
        modelController = ModelController()
        modelController.setModel(
            ModelFactory().loadModel(algorithm=self._algorithm, modelPath=modelPath, environment=environment))
        for i in range(verifyTimes):
            reward = modelController.play(environment=environment)
            episodeRewardList.append(reward)
        environment.close()
        return episodeRewardList

    def verifyModelByTime(self, modelPath: str, timeLimit: int = 0, explorationEpisodeEsp = 0, explorationStepEsp = 0):
        episodeRewardList = []
        environment = self._environmentFactory.createEnvironment()
        modelController = ModelController()
        modelController.setModel(ModelFactory().loadModel(algorithm=self._algorithm, modelPath=modelPath, environment=environment))
        totalTime = 0
        isDone = True
        while isDone:
            initialTime = time.time()
            reward = modelController.playWithExploration(environment=environment, explorationEpisodeEsp=explorationEpisodeEsp, explorationStepEsp=explorationStepEsp)
            totalTime += time.time() - initialTime
            episodeRewardList.append(reward)
            isDone = (totalTime < timeLimit) or (timeLimit == 0)
            Logger().info(totalTime)
        environment.close()
        return episodeRewardList

    def verifyModelByTotalStep(self, modelPath: str, totalStep, explorationEpisodeEsp = 0, explorationStepEsp = 0):
        episodeRewardList = []
        environment = self._environmentFactory.createEnvironment()
        modelController = ModelController()
        modelController.setModel(
            ModelFactory().loadModel(algorithm=self._algorithm, modelPath=modelPath, environment=environment))
        modelController.playByTotalStep(environment=environment, totalStep=totalStep, explorationEpisodeEsp=explorationEpisodeEsp, explorationStepEsp=explorationStepEsp)
        environment.close()
        return episodeRewardList

    def playModel(self):
        pass
