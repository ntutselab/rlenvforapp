from dependency_injector import containers, providers
import RLEnvForApp

from RLEnvForApp.adapter.agent.policy.extractor import *
from RLEnvForApp.adapter.environment.gym import *
from configuration.di.DIConfiguration import DIConfiguration


class AgentDIContainers(containers.DeclarativeContainer):
    config = DIConfiguration.config

    # policy
    cnnExtractor = providers.Callable(
        DIConfiguration.get_class_name(config.Agent.cnn_extractor())
    )

    environment = DIConfiguration.get_class_name(config.Agent.environment())
