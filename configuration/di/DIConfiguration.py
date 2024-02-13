import os

from dependency_injector import providers

CONFIG_DIRECTORY_PATH = "configuration/config"
# configFilePath = "AIGUIDE_File_Environment.ini"
# configFilePath = "AIGUIDE_Web_Environment.ini"
# configFilePath = "AIGUIDE_File_Environment_No_Coverage.ini"
# configFilePath = "AIGUIDE_Web_Environment_No_Coverage.ini"
# configFilePath = "AIGUIDE_File_Environment_Cosine_Similarity.ini"
CONFIG_FILE_PATH = "AIGUIDE_Web_Environment_Cosine_Similarity.ini"
DEFAULT_MODEL_CONFIG_FILE_PATH = "default_model_config.ini"
DEFAULT_CONFIG_FILE_PATH = "default.ini"

MODEL_CONFIG_DIRECTORY_PATH = "configuration/model"
MODEL_CONFIG_FILE_PATH = "default_model_config.ini"


class DIConfiguration:
    model_config_path = os.path.join(
        MODEL_CONFIG_DIRECTORY_PATH,
        MODEL_CONFIG_FILE_PATH)
    default_config_path = os.path.join(
        CONFIG_DIRECTORY_PATH, DEFAULT_CONFIG_FILE_PATH)
    config_path = os.path.join(CONFIG_DIRECTORY_PATH, CONFIG_FILE_PATH)
    config = providers.Configuration()

    if os.path.isfile(config_path):
        config.from_ini(config_path)
    else:
        raise RuntimeError(config_path + " file is not exist.")

    @staticmethod
    def get_class_name(class_name_string: str):
        module_list = class_name_string.split('.')
        class_name = __import__(module_list[0])
        for module in module_list[1:]:
            class_name = getattr(class_name, module)
        return class_name
