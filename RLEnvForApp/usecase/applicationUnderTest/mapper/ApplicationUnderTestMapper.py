from RLEnvForApp.domain.applicationUnderTest import ApplicationUnderTest

from ..entity import ApplicationUnderTestEntity


def mapping_application_under_test_entity_from(
        aut: ApplicationUnderTest.ApplicationUnderTest):
    aut_entity = ApplicationUnderTestEntity.ApplicationUnderTestEntity(id=aut.get_id(),
                                                                      applicationName=aut.get_application_name(),
                                                                      ip=aut.get_ip(), port=aut.get_port())
    return aut_entity


def mapping_application_under_test_from(
        aut_entity: ApplicationUnderTestEntity.ApplicationUnderTestEntity):
    aut: ApplicationUnderTest.ApplicationUnderTest = ApplicationUnderTest.ApplicationUnderTest(id=aut_entity.get_id(),
                                                                                               applicationName=aut_entity.getapplication_name(),
                                                                                               ip=aut_entity.get_ip(), port=aut_entity.get_port())
    return aut
