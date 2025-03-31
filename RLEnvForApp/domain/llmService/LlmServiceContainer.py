from RLEnvForApp.domain.llmService.ILlmService import ILlmService

class LlmServiceContainer(ILlmService):
    instance: ILlmService = None

    def set_instance(self, instance: ILlmService) -> None:
        self.instance = instance

    def get_instance(self) -> ILlmService:
        return self.instance
    
    def set_prompt(self, prompt: str, *args) -> None:
        self.get_instance().set_prompt(prompt, *args)

    def set_system_prompt(self, system_prompt: str, *args) -> None:
        self.get_instance().set_system_prompt(system_prompt, *args)
    
    def get_prompt(self) -> str:
        return self.get_instance().prompt

    def get_system_prompt(self) -> str:
        return self.get_instance().system_prompt

    def get_response(self, prompt: str = None, system_prompt: str = None) -> str:
        if prompt is None:
            prompt = self.get_prompt()
        if system_prompt is None:
            system_prompt = self.get_system_prompt()
        return self.get_instance().get_response(prompt, system_prompt)

llm_service_instance:LlmServiceContainer = LlmServiceContainer()
llm_service:ILlmService = llm_service_instance