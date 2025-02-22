class ILlmService:
    system_prompt: str = ""
    
    def set_system_prompt(self, system_prompt: str, *args) -> None:
        self.system_prompt = system_prompt
        self._set_system_prompt(system_prompt, *args)
    
    def get_system_prompt(self) -> str:
        return self.system_prompt

    def _set_system_prompt(self, system_prompt: str, *args):
        pass

    def get_response(self, prompt: str, system_prompt: str=None) -> str:
        raise NotImplementedError("This method must be implemented by the subclass.")
