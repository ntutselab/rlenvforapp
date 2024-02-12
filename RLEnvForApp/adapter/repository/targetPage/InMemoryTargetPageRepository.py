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
            if each.getId() == targetPageEntity.getId():
                index = self._targetPageEntities.index(each)
                self._targetPageEntities[index] = targetPageEntity

    def deleteById(self, id):
        self._targetPageEntities.remove(self.findById(id=id))

    def findById(self, id):
        targetTargetPageEntity: TargetPageEntity = None
        for targetPageEntity in self._targetPageEntities:
            if targetPageEntity.getId() == id:
                targetTargetPageEntity = targetPageEntity
        return targetTargetPageEntity

    def findAll(self) -> [TargetPageEntity]:
        return self._targetPageEntities
