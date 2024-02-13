from RLEnvForApp.usecase.environment.episodeHandler.entity.EpisodeHandlerEntity import \
    EpisodeHandlerEntity
from RLEnvForApp.usecase.repository.EpisodeHandlerRepository import \
    EpisodeHandlerRepository


class InMemoryEpisodeHandlerRepository(EpisodeHandlerRepository):
    def __init__(self, sizeLimit: int = -1):
        super().__init__(sizeLimit=sizeLimit)
        self._episode_handler_entities: [EpisodeHandlerEntity] = []

    def add(self, episode_handler_entity: EpisodeHandlerEntity):
        self._episode_handler_entities.append(episode_handler_entity)
        if self._is_over_the_size_limit():
            firstEpisodeHandlerEntity: EpisodeHandlerEntity = self._episode_handler_entities[0]
            self.delete_by_id(firstEpisodeHandlerEntity.get_id())

    def delete_by_id(self, id):
        self._episode_handler_entities.remove(self.find_by_id(id=id))

    def find_by_id(self, id):
        target_episode_handler_entity: EpisodeHandlerEntity = None
        for episode_handler_entity in self._episode_handler_entities:
            if episode_handler_entity.get_id() == id:
                target_episode_handler_entity = episode_handler_entity
        return target_episode_handler_entity

    def find_all(self) -> [EpisodeHandlerEntity]:
        return self._episode_handler_entities

    def update(self, episode_handler_entity: EpisodeHandlerEntity):
        for each in self._episode_handler_entities.copy():
            if episode_handler_entity.get_id() == each.get_id():
                index = self._episode_handler_entities.index(each)
                self._episode_handler_entities[index] = episode_handler_entity

    def _is_over_the_size_limit(self):
        if super().get_size_limit() <= 0:
            return False
        return super().get_size_limit() < len(self._episode_handler_entities)
