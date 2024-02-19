from dependency_injector import containers, providers

from .DIConfiguration import DIConfiguration


class AgentDIContainers(containers.DeclarativeContainer):
    config = DIConfiguration.config

    #policy
    cnnExtractor = providers.Callable(
        DIConfiguration.get_class_name(config.Agent.cnn_extractor())
    )

    environment = DIConfiguration.get_class_name(config.Agent.environment())
