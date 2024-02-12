from RLEnvForApp.usecase.repository.TargetPageRepository import \
    TargetPageRepository
from RLEnvForApp.usecase.targetPage.entity import TargetPageEntity


class InMemoryTargetPageRepository(TargetPageRepository):
    def __init__(self):
        super().__init__()
        self._targetPageEntities: [TargetPageEntity] = []

    def add(self, targetPageEntity: TargetPageEntity):
        self._targetPageEntities.append(targetPageEntity)

    def update(self, targetPageEntity: TargetPageEntity):
        for each in self._targetPageEntities:
            if each.get_id() == targetPageEntity.get_id():
                index = self._targetPageEntities.index(each)
                self._targetPageEntities[index] = targetPageEntity

    def delete_by_id(self, id):
        self._targetPageEntities.remove(self.find_by_id(id=id))

    def find_by_id(self, id):
        targetTargetPageEntity: TargetPageEntity = None
        for targetPageEntity in self._targetPageEntities:
            if targetPageEntity.get_id() == id:
                targetTargetPageEntity = targetPageEntity
        return targetTargetPageEntity

    def find_all(self) -> [TargetPageEntity]:
        return self._targetPageEntities
