import torch
from RLEnvForApp.adapter.agent.model.builder.PromptModelBuilder import PromptModelBuilder
from RLEnvForApp.adapter.agent.model.builder.PromptModelDirector import PromptModelDirector


class LLMController:
    def play(self):
        prompt_model_builder = PromptModelBuilder()
        prompt_model = PromptModelDirector().make_my_research(prompt_model_builder)
        # check cuda
        if torch.cuda.is_available():
            prompt_model = prompt_model.cuda()
