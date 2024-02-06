from RLEnvForApp.usecase.environment.episodeHandler.entity.EpisodeHandlerEntity import EpisodeHandlerEntity


class EpisodeHandlerRepository:
    def __init__(self, sizeLimit: int):
        self._sizeLimit = sizeLimit

    def getSizeLimit(self):
        return self._sizeLimit

    def add(self, episodeHandlerEntity: EpisodeHandlerEntity):
        pass

    def deleteById(self, id: str):
        pass

    def findById(self, id: str):
        pass

    def findAll(self) -> [EpisodeHandlerEntity]:
        pass

    def update(self, episodeHandlerEntity: EpisodeHandlerEntity):
        pass
