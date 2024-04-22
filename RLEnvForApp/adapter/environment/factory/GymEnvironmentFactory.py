from stable_baselines3.common.vec_env import DummyVecEnv

from configuration.di.AgentDIContainers import AgentDIContainers


class GymEnvironmentFactory:
    def __init__(self):
        pass

    def createEnvironment(self) -> DummyVecEnv:
        return DummyVecEnv([lambda: AgentDIContainers.environment()])
