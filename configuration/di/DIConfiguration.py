import os

from dependency_injector import providers

configDirectoryPath = "configuration/config"
# configFilePath = "AIGUIDE_File_Environment.ini"
# configFilePath = "AIGUIDE_Web_Environment.ini"
# configFilePath = "AIGUIDE_File_Environment_No_Coverage.ini"
# configFilePath = "AIGUIDE_Web_Environment_No_Coverage.ini"
# configFilePath = "AIGUIDE_File_Environment_Cosine_Similarity.ini"
configFilePath = "AIGUIDE_Web_Environment_Cosine_Similarity.ini"
defaultModelConfigFilePath = "default_model_config.ini"
defaultConfigFilePath = "default.ini"

modelConfigDirectoryPath = "configuration/model"
modelConfigFilePath = "default_model_config.ini"


class DIConfiguration:
    model_config_path = os.path.join(modelConfigDirectoryPath, modelConfigFilePath)
    default_config_path = os.path.join(configDirectoryPath, defaultConfigFilePath)
    config_path = os.path.join(configDirectoryPath, configFilePath)
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
