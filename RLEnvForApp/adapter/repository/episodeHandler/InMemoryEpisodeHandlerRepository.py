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
        if self._is_over_the_size_limit():
            firstEpisodeHandlerEntity: EpisodeHandlerEntity = self._episodeHandlerEntities[0]
            self.delete_by_id(firstEpisodeHandlerEntity.get_id())

    def delete_by_id(self, id):
        self._episodeHandlerEntities.remove(self.find_by_id(id=id))

    def find_by_id(self, id):
        targetEpisodeHandlerEntity: EpisodeHandlerEntity = None
        for episodeHandlerEntity in self._episodeHandlerEntities:
            if episodeHandlerEntity.get_id() == id:
                targetEpisodeHandlerEntity = episodeHandlerEntity
        return targetEpisodeHandlerEntity

    def find_all(self) -> [EpisodeHandlerEntity]:
        return self._episodeHandlerEntities

    def update(self, episodeHandlerEntity: EpisodeHandlerEntity):
        for each in self._episodeHandlerEntities.copy():
            if episodeHandlerEntity.get_id() == each.get_id():
                index = self._episodeHandlerEntities.index(each)
                self._episodeHandlerEntities[index] = episodeHandlerEntity

    def _is_over_the_size_limit(self):
        if super().get_size_limit() <= 0:
            return False
        return super().get_size_limit() < len(self._episodeHandlerEntities)
