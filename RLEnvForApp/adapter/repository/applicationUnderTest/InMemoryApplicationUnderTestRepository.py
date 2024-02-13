from RLEnvForApp.usecase.applicationUnderTest.entity.ApplicationUnderTestEntity import \
    ApplicationUnderTestEntity
from RLEnvForApp.usecase.repository.ApplicationUnderTestRepository import \
    ApplicationUnderTestRepository


class InMemoryApplicationUnderTestRepository(ApplicationUnderTestRepository):
    def __init__(self):
        super().__init__()
        self._auts: [ApplicationUnderTestEntity] = []

    def add(self, aut_entity: ApplicationUnderTestEntity):
        self._auts.append(aut_entity)

    def delet_by_id(self, id):
        self._auts.remove(self.find_by_id(id))

    def find_by_id(self, id):
        target_aut: ApplicationUnderTestEntity = None
        for aut_entity in self._auts:
            if aut_entity.get_id() == id:
                target_aut = aut_entity
        return target_aut

    def find_all(self) -> [ApplicationUnderTestEntity]:
        return self._auts
