from RLEnvForApp.usecase.environment.episodeHandler.dto.EpisodeHandlerDTO import \
    EpisodeHandlerDTO


class GetEpisodeHandlerOutput:
    def __init__(self):
        self._episodeHandlerDTO: EpisodeHandlerDTO = None

    def setEpisodeHandlerDTO(self, episodeHandlerDTO: EpisodeHandlerDTO):
        self._episodeHandlerDTO = episodeHandlerDTO

    def getEpisodeHandlerDTO(self) -> EpisodeHandlerDTO:
        return self._episodeHandlerDTO
