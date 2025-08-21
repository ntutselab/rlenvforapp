import os
from importlib import import_module
from dependency_injector import providers

configDirectoryPath = "configuration/config"
# configFilePath = "AIGUIDE_File_Environment.ini"
# configFilePath = "AIGUIDE_Web_Environment.ini"
# configFilePath = "AIGUIDE_File_Environment_No_Coverage.ini"
# configFilePath = "AIGUIDE_Web_Environment_No_Coverage.ini"
# configFilePath = "AIGUIDE_File_Environment_Cosine_Similarity.ini"
# configFilePath = "LLM.ini"

# feedback vs no feedback
configFilePath = "LLM_exp_feedback_enabled.ini"
# configFilePath = "LLM_exp_feedback_disabled.ini"


# LLM generate text vs LLM select data faker vs mixed
# llm only is also the exp2 feedback enable
# configFilePath = "LLM_exp_input_llm_only.ini"
# configFilePath = "LLM_exp_input_datafaker_select.ini"
# Also mixed is the exp4 my method
# configFilePath = "LLM_exp_input_mixed.ini"

# Check required field before filling the field vs fill the field directly
# configFilePath = "LLM_exp_check_field_required.ini"
# configFilePath = "LLM_exp_fill_all_field.ini"

# page compare by only LLM vs page compare by similarity assisted by LLM
# configFilePath = "LLM_exp_judge_llm_only.ini"
# configFilePath = "LLM_exp_judge_similarity_assisted.ini"

# Different LLM
# configFilePath = "LLM_exp_GeminiPro.ini"

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
