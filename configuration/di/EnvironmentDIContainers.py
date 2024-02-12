from dependency_injector import containers, providers

from configuration.di.DIConfiguration import DIConfiguration


class EnvironmentDIContainers(containers.DeclarativeContainer):
    config = DIConfiguration.config

    # repository
    targetPageRepository = providers.Singleton(
        DIConfiguration.get_class_name(
            config.Environment.target_page_repository())
    )

    episodeHandlerRepository = providers.Singleton(
        DIConfiguration.get_class_name(
            config.Environment.episode_handler_repository()),
        sizeLimit=2
    )

    applicationUnderTestRepository = providers.Singleton(
        DIConfiguration.get_class_name(
            config.Environment.application_under_test_repository())
    )

    # service
    observationService = providers.Factory(
        DIConfiguration.get_class_name(
            config.Environment.observation_service())
    )

    actionCommandFactory = providers.Factory(
        DIConfiguration.get_class_name(
            config.Environment.action_command_factory())
    )

    rewardCalculatorService = providers.Factory(
        DIConfiguration.get_class_name(
            config.Environment.reward_calculator_service())
    )

    directiveRuleService = providers.Factory(
        DIConfiguration.get_class_name(
            config.Environment.directive_rule_service())
    )

    targetPageQueueManagerService = providers.Factory(
        DIConfiguration.get_class_name(
            config.Environment.target_page_queue_manager()),
        repository=targetPageRepository
    )

    # other
    episodeHandler = providers.Factory(
        DIConfiguration.get_class_name(config.Environment.episode_handler()),
        episodeStep=int(config.Global.episode_step())
    )

    applicationHandler = providers.Factory(
        DIConfiguration.get_class_name(
            config.Environment.application_handler()),
        serverFolder="RLEnvForApp/application/serverInstance"
    )
