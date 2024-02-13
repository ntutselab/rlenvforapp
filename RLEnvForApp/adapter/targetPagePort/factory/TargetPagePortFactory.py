from RLEnvForApp.adapter.targetPagePort import (AIGuideHTMLLogTargetPagePort,
                                                AIGuideTargetPagePort,
                                                AIGuideVerifyTargetPagePort,
                                                ITargetPagePort)


class TargetPagePortFactory:
    def __init__(self):
        pass

    def create_ai_guide_target_page_port(self, javaIp: str, pythonIp, javaPort: int, pythonPort: int, serverName: str,
                                    root_url: str = "127.0.0.1",
                                    code_coverage_type: str = "coverage") -> ITargetPagePort.ITargetPagePort:
        return AIGuideTargetPagePort.AIGuideTargetPagePort(javaIp=javaIp, pythonIp=pythonIp, javaPort=javaPort,
                                                           pythonPort=pythonPort, serverName=serverName,
                                                           root_url=root_url, code_coverage_type=code_coverage_type)

    def create_ai_guide_html_log_target_page_port(self, folder_path: str):
        return AIGuideHTMLLogTargetPagePort.AIGuideHTMLLogTargetPagePort(
            folder_path=folder_path)

    def create_ai_guide_verify_target_page_port(self, javaIp: str, pythonIp, javaPort: int, pythonPort: int, serverName: str,
                                          root_url: str = "127.0.0.1",
                                          code_coverage_type: str = "coverage") -> ITargetPagePort.ITargetPagePort:
        return AIGuideVerifyTargetPagePort.AIGuideVerifyTargetPagePort(javaIp=javaIp, pythonIp=pythonIp, javaPort=javaPort,
                                                                       pythonPort=pythonPort, serverName=serverName,
                                                                       root_url=root_url, code_coverage_type=code_coverage_type)
