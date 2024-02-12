from stable_baselines.common.vec_env import DummyVecEnv

from configuration.di.AgentDIContainers import AgentDIContainers


class GymEnvironmentFactory:
    def __init__(self):
        pass

    def create_environment(self) -> DummyVecEnv:
        return DummyVecEnv([lambda: AgentDIContainers.environment()])
