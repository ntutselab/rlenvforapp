from RLEnvForApp.domain.llmService.ILlmService import ILlmService

class LlmServiceContainer(ILlmService):
    instance: ILlmService = None

    def set_instance(self, instance: ILlmService) -> None:
        self.instance = instance

    def get_instance(self, instance: ILlmService) -> None:
        return self.instance
    
    def set_system_prompt(self, system_prompt: str, *args) -> None:
        self.get_instance()._set_system_prompt(system_prompt, *args)
    
    def get_system_prompt(self) -> str:
        return self.get_instance().system_prompt

    def get_response(self, prompt: str, system_prompt: str=None) -> str:
        return self.get_instance().get_response(self, prompt, system_prompt)


llm_service_instance:LlmServiceContainer = LlmServiceContainer()
llm_service:ILlmService = llm_service_instance
