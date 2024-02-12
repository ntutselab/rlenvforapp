from RLEnvForApp.adapter.targetPagePort import (AIGuideHTMLLogTargetPagePort,
                                                AIGuideTargetPagePort,
                                                AIGuideVerifyTargetPagePort,
                                                ITargetPagePort)


class TargetPagePortFactory:
    def __init__(self):
        pass

    def create_ai_guide_target_page_port(self, javaIp: str, pythonIp, javaPort: int, pythonPort: int, serverName: str,
                                    rootUrl: str = "127.0.0.1",
                                    codeCoverageType: str = "coverage") -> ITargetPagePort.ITargetPagePort:
        return AIGuideTargetPagePort.AIGuideTargetPagePort(javaIp=javaIp, pythonIp=pythonIp, javaPort=javaPort,
                                                           pythonPort=pythonPort, serverName=serverName,
                                                           rootUrl=rootUrl, codeCoverageType=codeCoverageType)

    def create_ai_guide_html_log_target_page_port(self, folderPath: str):
        return AIGuideHTMLLogTargetPagePort.AIGuideHTMLLogTargetPagePort(
            folderPath=folderPath)

    def create_ai_guide_verify_target_page_port(self, javaIp: str, pythonIp, javaPort: int, pythonPort: int, serverName: str,
                                          rootUrl: str = "127.0.0.1",
                                          codeCoverageType: str = "coverage") -> ITargetPagePort.ITargetPagePort:
        return AIGuideVerifyTargetPagePort.AIGuideVerifyTargetPagePort(javaIp=javaIp, pythonIp=pythonIp, javaPort=javaPort,
                                                                       pythonPort=pythonPort, serverName=serverName,
                                                                       rootUrl=rootUrl, codeCoverageType=codeCoverageType)
