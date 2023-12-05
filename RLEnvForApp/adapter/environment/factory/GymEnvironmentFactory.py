import gym
from stable_baselines.common.vec_env import DummyVecEnv

from dependency_injector.wiring import inject, Provide

from configuration.di.AgentDIContainers import AgentDIContainers


class GymEnvironmentFactory:
    def __init__(self):
        pass

    def createEnvironment(self) -> DummyVecEnv:
        return DummyVecEnv([lambda: AgentDIContainers.environment()])
