from RLEnvForApp.usecase.environment.episodeHandler.dto.EpisodeHandlerDTO import \
    EpisodeHandlerDTO


class GetEpisodeHandlerOutput:
    def __init__(self):
        self._episode_handler_dto: EpisodeHandlerDTO = None

    def set_episode_handler_dto(self, episode_handler_dto: EpisodeHandlerDTO):
        self._episode_handler_dto = episode_handler_dto

    def get_episode_handler_dto(self) -> EpisodeHandlerDTO:
        return self._episode_handler_dto
