import os
import time

from dependency_injector.wiring import inject
from RLEnvForApp.adapter.agent.model.ModelController import ModelController
from RLEnvForApp.adapter.agent.model.ModelFactory import ModelFactory
from RLEnvForApp.adapter.environment.factory.GymEnvironmentFactory import \
    GymEnvironmentFactory
from RLEnvForApp.logger.logger import Logger


class RLController:
    @inject
    def __init__(self, algorithm, policy):
        Logger().info(f"Algorithm: {algorithm}")
        self._algorithm = algorithm
        self._policy = policy
        self._environmentFactory = GymEnvironmentFactory()

    def learn_model(self, totalTimesteps: int, modelDir: str,
                   modelSeriesName: str, tensorboardPath: str = "model/log"):
        environment = self._environmentFactory.create_environment()
        modelController = ModelController()
        modelController.set_model(
            ModelFactory().create_model(algorithm=self._algorithm, policy=self._policy, environment=environment,
                                       tensorboardPath="model/log"))
        modelController.learn(totalTimeSteps=totalTimesteps)
        modelName = modelSeriesName + "_" + str(totalTimesteps) + "step"

        modelController.save(os.path.join(modelDir, modelName))
        environment.close()

    def learn_model_by_exited_model(self, totalTimesteps: int, modelDir: str,
                                modelSeriesName: str, modelPath: str):
        environment = self._environmentFactory.create_environment()
        modelController = ModelController()
        modelController.set_model(
            ModelFactory().load_model(
                algorithm=self._algorithm,
                modelPath=modelPath,
                environment=environment))
        modelController.learn(totalTimeSteps=totalTimesteps)
        modelName = modelSeriesName + "_" + str(totalTimesteps) + "step"

        modelController.save(os.path.join(modelDir, modelName))
        environment.close()

    def iterate_learn_model(self, timestepsPerIteration: int, iterationTimes: int,
                          modelDir: str, modelSeriesName: str, tensorboardPath: str = "model/log"):
        environment = self._environmentFactory.create_environment()
        modelController = ModelController().set_model(
            ModelFactory().create_model(algorithm=self._algorithm, policy=self._policy, environment=environment,
                                       tensorboardPath="model/log"))
        for i in range(iterationTimes):
            modelController.learn(totalTimeSteps=timestepsPerIteration)
            modelName = modelSeriesName + "_" + \
                str(timestepsPerIteration * (i + 1)) + "step"

            modelController.save(os.path.join(modelDir, modelName))

    def verify_model(self, modelPath: str, verifyTimes: int):
        episodeRewardList = []
        environment = self._environmentFactory.create_environment()
        modelController = ModelController()
        modelController.set_model(
            ModelFactory().load_model(algorithm=self._algorithm, modelPath=modelPath, environment=environment))
        for i in range(verifyTimes):
            reward = modelController.play(environment=environment)
            episodeRewardList.append(reward)
        environment.close()
        return episodeRewardList

    def verify_model_by_time(self, modelPath: str, timeLimit: int = 0,
                          explorationEpisodeEsp=0, explorationStepEsp=0):
        episodeRewardList = []
        environment = self._environmentFactory.create_environment()
        modelController = ModelController()
        modelController.set_model(
            ModelFactory().load_model(
                algorithm=self._algorithm,
                modelPath=modelPath,
                environment=environment))
        totalTime = 0
        isDone = True
        while isDone:
            initialTime = time.time()
            reward = modelController.play_with_exploration(
                environment=environment,
                explorationEpisodeEsp=explorationEpisodeEsp,
                explorationStepEsp=explorationStepEsp)
            totalTime += time.time() - initialTime
            episodeRewardList.append(reward)
            isDone = (totalTime < timeLimit) or (timeLimit == 0)
            Logger().info(totalTime)
        environment.close()
        return episodeRewardList

    def verify_model_by_total_step(self, modelPath: str, totalStep,
                               explorationEpisodeEsp=0, explorationStepEsp=0):
        episodeRewardList = []
        environment = self._environmentFactory.create_environment()
        modelController = ModelController()
        modelController.set_model(
            ModelFactory().load_model(algorithm=self._algorithm, modelPath=modelPath, environment=environment))
        modelController.play_by_total_step(
            environment=environment,
            totalStep=totalStep,
            explorationEpisodeEsp=explorationEpisodeEsp,
            explorationStepEsp=explorationStepEsp)
        environment.close()
        return episodeRewardList

    def play_model(self):
        pass
