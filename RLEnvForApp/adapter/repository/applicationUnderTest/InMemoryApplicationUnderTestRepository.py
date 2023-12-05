from RLEnvForApp.usecase.applicationUnderTest.entity.ApplicationUnderTestEntity import ApplicationUnderTestEntity
from RLEnvForApp.usecase.repository.ApplicationUnderTestRepository import ApplicationUnderTestRepository


class InMemoryApplicationUnderTestRepository(ApplicationUnderTestRepository):
    def __init__(self):
        super().__init__()
        self._auts: [ApplicationUnderTestEntity] = []

    def add(self, autEntity: ApplicationUnderTestEntity):
        self._auts.append(autEntity)

    def deletById(self, id):
        self._auts.remove(self.findById(id))

    def findById(self, id):
        targetAut: ApplicationUnderTestEntity = None
        for autEntity in self._auts:
            if autEntity.getId() == id:
                targetAut = autEntity
        return targetAut

    def findAll(self) -> [ApplicationUnderTestEntity]:
        return self._auts
