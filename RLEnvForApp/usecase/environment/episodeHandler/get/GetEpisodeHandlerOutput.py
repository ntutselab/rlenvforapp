from RLEnvForApp.usecase.environment.episodeHandler.dto.EpisodeHandlerDTO import \
    EpisodeHandlerDTO


class GetEpisodeHandlerOutput:
    def __init__(self):
        self._episodeHandlerDTO: EpisodeHandlerDTO = None

    def set_episode_handler_dto(self, episodeHandlerDTO: EpisodeHandlerDTO):
        self._episodeHandlerDTO = episodeHandlerDTO

    def get_episode_handler_dto(self) -> EpisodeHandlerDTO:
        return self._episodeHandlerDTO
