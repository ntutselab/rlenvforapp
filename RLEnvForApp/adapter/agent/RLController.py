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
        self._environment_factory = GymEnvironmentFactory()

    def learn_model(self, totalTimesteps: int, model_dir: str,
                   modelSeriesName: str, tensorboardPath: str = "model/log"):
        environment = self._environment_factory.create_environment()
        model_controller = ModelController()
        model_controller.set_model(
            ModelFactory().create_model(algorithm=self._algorithm, policy=self._policy, environment=environment,
                                       tensorboardPath="model/log"))
        model_controller.learn(totalTimeSteps=totalTimesteps)
        model_name = modelSeriesName + "_" + str(totalTimesteps) + "step"

        model_controller.save(os.path.join(model_dir, model_name))
        environment.close()

    def learn_model_by_exited_model(self, totalTimesteps: int, model_dir: str,
                                modelSeriesName: str, model_path: str):
        environment = self._environment_factory.create_environment()
        model_controller = ModelController()
        model_controller.set_model(
            ModelFactory().load_model(
                algorithm=self._algorithm,
                model_path=model_path,
                environment=environment))
        model_controller.learn(totalTimeSteps=totalTimesteps)
        model_name = modelSeriesName + "_" + str(totalTimesteps) + "step"

        model_controller.save(os.path.join(model_dir, model_name))
        environment.close()

    def iterate_learn_model(self, timestepsPerIteration: int, iterationTimes: int,
                          model_dir: str, modelSeriesName: str, tensorboardPath: str = "model/log"):
        environment = self._environment_factory.create_environment()
        model_controller = ModelController().set_model(
            ModelFactory().create_model(algorithm=self._algorithm, policy=self._policy, environment=environment,
                                       tensorboardPath="model/log"))
        for i in range(iterationTimes):
            model_controller.learn(totalTimeSteps=timestepsPerIteration)
            model_name = modelSeriesName + "_" + \
                str(timestepsPerIteration * (i + 1)) + "step"

            model_controller.save(os.path.join(model_dir, model_name))

    def verify_model(self, model_path: str, verifyTimes: int):
        episode_reward_list = []
        environment = self._environment_factory.create_environment()
        model_controller = ModelController()
        model_controller.set_model(
            ModelFactory().load_model(algorithm=self._algorithm, model_path=model_path, environment=environment))
        for i in range(verifyTimes):
            reward = model_controller.play(environment=environment)
            episode_reward_list.append(reward)
        environment.close()
        return episode_reward_list

    def verify_model_by_time(self, model_path: str, timeLimit: int = 0,
                          exploration_episode_esp=0, exploration_step_esp=0):
        episode_reward_list = []
        environment = self._environment_factory.create_environment()
        model_controller = ModelController()
        model_controller.set_model(
            ModelFactory().load_model(
                algorithm=self._algorithm,
                model_path=model_path,
                environment=environment))
        total_time = 0
        is_done = True
        while is_done:
            initialTime = time.time()
            reward = model_controller.play_with_exploration(
                environment=environment,
                exploration_episode_esp=exploration_episode_esp,
                exploration_step_esp=exploration_step_esp)
            total_time += time.time() - initialTime
            episode_reward_list.append(reward)
            is_done = (total_time < timeLimit) or (timeLimit == 0)
            Logger().info(total_time)
        environment.close()
        return episode_reward_list

    def verify_model_by_total_step(self, model_path: str, totalStep,
                               exploration_episode_esp=0, exploration_step_esp=0):
        episode_reward_list = []
        environment = self._environment_factory.create_environment()
        model_controller = ModelController()
        model_controller.set_model(
            ModelFactory().load_model(algorithm=self._algorithm, model_path=model_path, environment=environment))
        model_controller.play_by_total_step(
            environment=environment,
            totalStep=totalStep,
            exploration_episode_esp=exploration_episode_esp,
            exploration_step_esp=exploration_step_esp)
        environment.close()
        return episode_reward_list

    def play_model(self):
        pass
