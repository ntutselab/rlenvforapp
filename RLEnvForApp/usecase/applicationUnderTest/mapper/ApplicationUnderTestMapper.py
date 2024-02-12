from RLEnvForApp.domain.applicationUnderTest import ApplicationUnderTest

from ..entity import ApplicationUnderTestEntity


def mappingApplicationUnderTestEntityFrom(aut: ApplicationUnderTest.ApplicationUnderTest):
    autEntity = ApplicationUnderTestEntity.ApplicationUnderTestEntity(id=aut.getId(),
                                                                      applicationName=aut.getApplicationName(),
                                                                      ip=aut.getIP(), port=aut.getPort())
    return autEntity


def mappingApplicationUnderTestFrom(
        autEntity: ApplicationUnderTestEntity.ApplicationUnderTestEntity):
    aut: ApplicationUnderTest.ApplicationUnderTest = ApplicationUnderTest.ApplicationUnderTest(id=autEntity.getId(),
                                                                                               applicationName=autEntity.getapplicationName(),
                                                                                               ip=autEntity.getIP(), port=autEntity.getPort())
    return aut
