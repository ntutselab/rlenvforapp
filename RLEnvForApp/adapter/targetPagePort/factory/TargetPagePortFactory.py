from RLEnvForApp.adapter.targetPagePort import ITargetPagePort, AIGuideTargetPagePort, AIGuideHTMLLogTargetPagePort, AIGuideVerifyTargetPagePort


class TargetPagePortFactory:
    def __init__(self):
        pass

    def createAIGuideTargetPagePort(self, javaIp: str, pythonIp, javaPort: int, pythonPort: int, serverName: str,
                                    rootUrl: str = "127.0.0.1",
                                    codeCoverageType: str = "coverage") -> ITargetPagePort.ITargetPagePort:
        return AIGuideTargetPagePort.AIGuideTargetPagePort(javaIp=javaIp, pythonIp=pythonIp, javaPort=javaPort,
                                                           pythonPort=pythonPort, serverName=serverName,
                                                           rootUrl=rootUrl, codeCoverageType=codeCoverageType)

    def createAIGuideHTMLLogTargetPagePort(self, folderPath: str):
        return AIGuideHTMLLogTargetPagePort.AIGuideHTMLLogTargetPagePort(folderPath=folderPath)

    def createAIGuideVerifyTargetPagePort(self, javaIp: str, pythonIp, javaPort: int, pythonPort: int, serverName: str,
                                          rootUrl: str = "127.0.0.1",
                                          codeCoverageType: str = "coverage") -> ITargetPagePort.ITargetPagePort:
        return AIGuideVerifyTargetPagePort.AIGuideVerifyTargetPagePort(javaIp=javaIp, pythonIp=pythonIp, javaPort=javaPort,
                                                                       pythonPort=pythonPort, serverName=serverName,
                                                                       rootUrl=rootUrl, codeCoverageType=codeCoverageType)
