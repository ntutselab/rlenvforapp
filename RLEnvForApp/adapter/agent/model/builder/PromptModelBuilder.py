import torch
from openprompt import PromptForClassification
from openprompt.plms import load_plm
from openprompt.prompts import ManualTemplate, PrefixTuningTemplate, SoftTemplate, ManualVerbalizer
from RLEnvForApp.adapter.agent.model.builder.builder import Builder


class PromptModelBuilder(Builder):
    """
    Builder for PromptModel of OpenPrompt.
    1. set llm model
    2. set template
    3. set verbalizer
    4. set state dict
    """

    def __init__(self):
        self.state_dict_path = None
        self.__result = None
        self.verbalizer = None
        self.template = None
        self.plm = None
        self.tokenizer = None
        self.model_config = None
        self.wrapper_class = None

    def reset(self):
        """
        Reset the builder.
        :return: None
        """
        if self.__result is not None:
            self.__result = None

    def get_result(self):
        """
        Get the result of the builder.
        :return: PromptModel
        """
        if self.__check_parameters():
            self.__result = PromptForClassification(
                template=self.template,
                plm=self.plm,
                verbalizer=self.verbalizer,
                freeze_plm=True,
                plm_eval_mode=False
            )
            # TODO: Cann't lock into pipfile.lock when I install torch. May need to install torch manually.
            # Please add map_location=torch.device('cpu') if you want to load the model on CPU.
            self.__result.load_state_dict(torch.load(self.state_dict_path))
        return self.__result

    def set_template(self, template_type: str, template_text: str):
        """
        Set the template. Before setting the template, the LLM model should be set.
        :param template_type: Type of template.
        :param template_text: Text of the template.
        :return:
        """
        if self.plm is None:
            raise ValueError("LLM model is not set. Please set the LLM model first.")

        # TODO: Add more template types.
        if template_type == "manual":
            self.template = ManualTemplate(tokenizer=self.tokenizer, text=template_text)
        elif template_type == "prefix":
            self.template = PrefixTuningTemplate(model=self.plm, tokenizer=self.tokenizer)
        elif template_type == "soft":
            self.template = SoftTemplate(model=self.plm, tokenizer=self.tokenizer, text=template_text)
        else:
            raise NotImplementedError

    def set_llm_model(self, model_name: str, model_path: str):
        """
        Set the LLM model.
        :param model_name: Name of the model.
        :param model_path: Path to the model.
        :return:
        """
        self.plm, self.tokenizer, self.model_config, self.wrapper_class = (
            load_plm(model_name, model_path))

    def set_verbalizer(self, verbalizer_type:str, labels_list: list, labels_word_file_path: str):
        """
        Set the verbalizer.
        Load the predefined label words from verbalizer file.
        Currently, support three types of file format:
        1. a .jsonl or .json file, in which is a single verbalizer
        in dict format.
        2. a .jsonal or .json file, in which is a list of verbalizers in dict format
        3. a .txt or a .csv file, in which is the label words of a class are listed in line,
        separated by commas. Begin a new verbalizer by an empty line.
        This format is recommended when you don't know the name of each class.
        :param verbalizer_type: Type of verbalizer.
        :param labels_list: List of class labels.
        :param labels_word_file_path: Path to the file containing the class labels.
        :return:
        """
        if verbalizer_type == "manual":
            self.verbalizer = (ManualVerbalizer(tokenizer=self.tokenizer, classes=labels_list)
                               .from_file(labels_word_file_path))
        else:
            raise NotImplementedError

    def set_state_dict(self, state_dict_path: str):
        """
        Set the state_dict of the model.
        :param state_dict_path: Path to the state_dict.
        :return:
        """
        self.state_dict_path = state_dict_path

    def get_tokenizer(self):
        """
        Get the tokenizer.
        :return: Tokenizer
        """
        if self.tokenizer is None:
            raise ValueError("Tokenizer is not set. Please set the LLM model first.")
        return self.tokenizer

    def get_template(self):
        """
        Get the template.
        :return: Template
        """
        if self.template is None:
            raise ValueError("Template is not set. Please set the template first.")
        return self.template

    def get_wrapper_class(self):
        """
        Get the wrapper class.
        :return: Wrapper class
        """
        if self.wrapper_class is None:
            raise ValueError("Wrapper class is not set. Please set the LLM model first.")
        return self.wrapper_class

    def __check_parameters(self):
        if self.template is None:
            raise ValueError("Template is not set.")
        elif self.verbalizer is None:
            raise ValueError("Verbalizer is not set.")
        elif self.plm is None:
            raise ValueError("LLM model is not set.")
        elif self.state_dict_path is None:
            raise ValueError("State dict is not set.")
        else:
            return True
