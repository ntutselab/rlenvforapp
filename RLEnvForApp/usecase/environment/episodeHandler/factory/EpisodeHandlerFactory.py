
from configuration.di.EnvironmentDIContainers import EnvironmentDIContainers
from RLEnvForApp.domain.environment.episodeHandler.IEpisodeHandler import \
    IEpisodeHandler


class EpisodeHandlerFactory:
    def __init__(self):
        pass

    def create_episode_handler(
            self, id: str, episodeIndex: int) -> IEpisodeHandler:
        return EnvironmentDIContainers.episode_handler(
            id=id, episodeIndex=episodeIndex)
