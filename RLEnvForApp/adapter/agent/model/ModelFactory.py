from stable_baselines import DQN, PPO2

from configuration.di.ModelDIContainers import ModelDIContainers
from RLEnvForApp.adapter.agent.model.MonkeyAdapter import MonkeyAdapter


class ModelFactory:
    def __init__(self):
        self._configPath = ""
        self._config = None

    def createModel(self, algorithm, policy, environment, tensorboardPath):
        self._checkAlgorithm(algorithm=algorithm)

        if algorithm == "DQN":
            return DQN(policy, environment,
                       gamma=ModelDIContainers.gamma,
                       learning_rate=ModelDIContainers.learning_rate,
                       verbose=ModelDIContainers.verbose,
                       prioritized_replay=ModelDIContainers.prioritized_replay,
                       tensorboard_log=tensorboardPath,
                       learning_starts=ModelDIContainers.learning_starts,
                       exploration_fraction=ModelDIContainers.exploration_fraction,
                       exploration_final_eps=ModelDIContainers.exploration_final_eps,
                       exploration_initial_eps=ModelDIContainers.exploration_initial_eps,
                       buffer_size=ModelDIContainers.buffer_size,
                       batch_size=ModelDIContainers.batch_size,
                       target_network_update_freq=ModelDIContainers.target_network_update_freq)
        if algorithm == "PPO2":
            return PPO2(policy, environment,
                        verbose=ModelDIContainers.verbose,
                        tensorboard_log=tensorboardPath,
                        nminibatches=ModelDIContainers.nminibatches,
                        n_steps=ModelDIContainers.n_steps)
        if algorithm == "Monkey":
            return MonkeyAdapter(policy=None, env=environment)

    def loadModel(self, algorithm, modelPath, environment=None, tensorboardPath=None):
        self._checkAlgorithm(algorithm=algorithm)

        model = None
        if algorithm == "DQN":
            model = DQN.load(modelPath, env=environment)
            # model.exploration_initial_eps=0.1
        if algorithm == "PPO2":
            model = PPO2.load(modelPath, env=environment)
        if algorithm == "Monkey":
            return MonkeyAdapter(policy=None, env=environment)

        model.tensorboard_log = tensorboardPath
        return model

    def _checkAlgorithm(self, algorithm):
        if algorithm not in ["DQN", "PPO2", "Monkey"]:
            raise RuntimeError("AlgorithmError: No such algorithm as " + algorithm)
