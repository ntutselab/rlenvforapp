from RLEnvForApp.usecase.repository.TargetPageRepository import \
    TargetPageRepository
from RLEnvForApp.usecase.targetPage.entity import TargetPageEntity


class InMemoryTargetPageRepository(TargetPageRepository):
    def __init__(self):
        super().__init__()
        self._target_page_entities: [TargetPageEntity] = []

    def add(self, target_page_entity: TargetPageEntity):
        self._target_page_entities.append(target_page_entity)

    def update(self, target_page_entity: TargetPageEntity):
        for each in self._target_page_entities:
            if each.get_id() == target_page_entity.get_id():
                index = self._target_page_entities.index(each)
                self._target_page_entities[index] = target_page_entity

    def delete_by_id(self, id):
        self._target_page_entities.remove(self.find_by_id(id=id))

    def find_by_id(self, id):
        target_target_page_entity: TargetPageEntity = None
        for target_page_entity in self._target_page_entities:
            if target_page_entity.get_id() == id:
                target_target_page_entity = target_page_entity
        return target_target_page_entity

    def find_all(self) -> [TargetPageEntity]:
        return self._target_page_entities
