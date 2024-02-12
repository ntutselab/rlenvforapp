from RLEnvForApp.usecase.environment.episodeHandler.entity.EpisodeHandlerEntity import \
    EpisodeHandlerEntity
from RLEnvForApp.usecase.repository.EpisodeHandlerRepository import \
    EpisodeHandlerRepository


class InMemoryEpisodeHandlerRepository(EpisodeHandlerRepository):
    def __init__(self, sizeLimit: int = -1):
        super().__init__(sizeLimit=sizeLimit)
        self._episodeHandlerEntities: [EpisodeHandlerEntity] = []

    def add(self, episodeHandlerEntity: EpisodeHandlerEntity):
        self._episodeHandlerEntities.append(episodeHandlerEntity)
        if self._isOverTheSizeLimit():
            firstEpisodeHandlerEntity: EpisodeHandlerEntity = self._episodeHandlerEntities[0]
            self.deleteById(firstEpisodeHandlerEntity.getId())

    def deleteById(self, id):
        self._episodeHandlerEntities.remove(self.findById(id=id))

    def findById(self, id):
        targetEpisodeHandlerEntity: EpisodeHandlerEntity = None
        for episodeHandlerEntity in self._episodeHandlerEntities:
            if episodeHandlerEntity.getId() == id:
                targetEpisodeHandlerEntity = episodeHandlerEntity
        return targetEpisodeHandlerEntity

    def findAll(self) -> [EpisodeHandlerEntity]:
        return self._episodeHandlerEntities

    def update(self, episodeHandlerEntity: EpisodeHandlerEntity):
        for each in self._episodeHandlerEntities.copy():
            if episodeHandlerEntity.getId() == each.getId():
                index = self._episodeHandlerEntities.index(each)
                self._episodeHandlerEntities[index] = episodeHandlerEntity

    def _isOverTheSizeLimit(self):
        if super().getSizeLimit() <= 0:
            return False
        return super().getSizeLimit() < len(self._episodeHandlerEntities)
