import os
from dependency_injector import providers
from configuration.di.DIConfiguration import DIConfiguration


class ModelDIContainers:
    modelConfigPath = DIConfiguration.model_config_path
    config = providers.Configuration()
    if os.path.isfile(modelConfigPath):
        config.from_ini(modelConfigPath)
    else:
        raise RuntimeError(modelConfigPath + " file is not exist.")

    # Global
    verbose = int(config.Global.verbose())

    # DQN
    gamma = float(config.DQN.gamma())
    learning_rate = float(config.DQN.learning_rate())
    prioritized_replay = bool(config.DQN.prioritized_replay())
    learning_starts = int(config.DQN.learning_starts())
    exploration_fraction = float(config.DQN.exploration_fraction())
    exploration_final_eps = float(config.DQN.exploration_final_eps())
    exploration_initial_eps = int(config.DQN.exploration_initial_eps())
    buffer_size = int(config.DQN.buffer_size())
    batch_size = int(config.DQN.batch_size())
    target_network_update_freq = int(config.DQN.target_network_update_freq())

    # PPO2
    nminibatches = int(config.PPO2.nminibatches())
    n_steps = int(config.PPO2.n_steps())
