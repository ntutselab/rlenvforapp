from abc import abstractmethod, ABC


class Builder(ABC):
    """
    Interface for model builders.
    """
    @abstractmethod
    def reset(self):
        """
        Reset the builder.
        :return:
        """

    @abstractmethod
    def set_template(self):
        """
        Set the template.
        :return: None
        """

    @abstractmethod
    def set_llm_model(self, model_name: str, model_path: str):
        """
        Set the LLM model.
        :return: None
        """

    @abstractmethod
    def set_verbalizer(self):
        """
        Set the verbalizer.
        :return: None
        """
