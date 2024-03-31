from openprompt.plms import load_plm
from openprompt.prompts import ManualTemplate, PrefixTuningTemplate
from RLEnvForApp.adapter.agent.model.builder.Builder import Builder


class PromptModelBuilder(Builder):
    """
    Builder for PromptModel of OpenPrompt.
    """

    def __init__(self):
        self.template = None
        self.plm = None
        self.tokenizer = None
        self.model_config = None
        self.WrapperClass = None

    def reset(self):
        if self.__result is not None:
            self.__result = None

    def set_template(self, template_type: str, template_text: str):
        """
        Set the template. Before setting the template, the LLM model should be set.
        :param template_type:
        :param template_text:
        :return:
        """
        if template_type == "manual":
            self.template = ManualTemplate(tokenizer=self.tokenizer, text=template_text)
        elif template_type == "prefix":
            self.template = PrefixTuningTemplate(model=self.plm, tokenizer=self.tokenizer)
        else:
            raise NotImplementedError

    def set_llm_model(self, model_name: str, model_path: str):
        """
        Set the LLM model.
        :param model_name:
        :param model_path:
        :return:
        """
        self.plm, self.tokenizer, self.model_config, self.WrapperClass = load_plm(model_name, model_path)

    def set_verbalizer(self):
        pass