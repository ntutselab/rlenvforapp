from RLEnvForApp.usecase.applicationUnderTest.entity.ApplicationUnderTestEntity import \
    ApplicationUnderTestEntity
from RLEnvForApp.usecase.repository.ApplicationUnderTestRepository import \
    ApplicationUnderTestRepository


class InMemoryApplicationUnderTestRepository(ApplicationUnderTestRepository):
    def __init__(self):
        super().__init__()
        self._auts: [ApplicationUnderTestEntity] = []

    def add(self, autEntity: ApplicationUnderTestEntity):
        self._auts.append(autEntity)

    def delet_by_id(self, id):
        self._auts.remove(self.find_by_id(id))

    def find_by_id(self, id):
        targetAut: ApplicationUnderTestEntity = None
        for autEntity in self._auts:
            if autEntity.get_id() == id:
                targetAut = autEntity
        return targetAut

    def find_all(self) -> [ApplicationUnderTestEntity]:
        return self._auts
