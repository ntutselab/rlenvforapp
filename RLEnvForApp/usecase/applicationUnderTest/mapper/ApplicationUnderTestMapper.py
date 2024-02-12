from RLEnvForApp.domain.applicationUnderTest import ApplicationUnderTest

from ..entity import ApplicationUnderTestEntity


def mapping_application_under_test_entity_from(
        aut: ApplicationUnderTest.ApplicationUnderTest):
    autEntity = ApplicationUnderTestEntity.ApplicationUnderTestEntity(id=aut.get_id(),
                                                                      applicationName=aut.get_application_name(),
                                                                      ip=aut.get_ip(), port=aut.get_port())
    return autEntity


def mapping_application_under_test_from(
        autEntity: ApplicationUnderTestEntity.ApplicationUnderTestEntity):
    aut: ApplicationUnderTest.ApplicationUnderTest = ApplicationUnderTest.ApplicationUnderTest(id=autEntity.get_id(),
                                                                                               applicationName=autEntity.getapplication_name(),
                                                                                               ip=autEntity.get_ip(), port=autEntity.get_port())
    return aut
