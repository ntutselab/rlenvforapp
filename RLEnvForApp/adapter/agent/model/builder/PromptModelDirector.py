from openprompt import PromptModel, PromptDataLoader
from openprompt.data_utils import InputExample

from RLEnvForApp.adapter.agent.model.builder.PromptModelBuilder import PromptModelBuilder


class PromptModelDirector:
    classes = [
        "first name",
        "last name",
        "email",
        "gender",
        "string",
        "user name",
        "full name",
        "postal code",
        "store name",
        "phone number",
        "street address",
        "city",
        "state",
        "province",
        "region",
        "number",
        "country",
        "display name",
        "address",
        "suburb",
        "company name",
        "card number",
        "expiration date",
        "CVV",
        "date",
    ]

    @staticmethod
    def make_my_research(builder: PromptModelBuilder) -> PromptModel:
        builder.reset()
        builder.set_llm_model("t5-lm", "google/t5-large-lm-adapt")
        builder.set_template("soft", 'The {"placeholder":"text_a"} label from web forms. The label belong to category {"mask"}.')
        builder.set_verbalizer("manual", PromptModelDirector.classes, "manual_verbalizer.txt")
        builder.set_state_dict("C:\\Users\\ligii\IdeaProjects\\rlenvforapp\\2747455425.ckpt")
        return builder.get_result()

    @staticmethod
    def make_fake_prompt_model(builder: PromptModelBuilder) -> PromptModel:
        builder.reset()
        builder.set_llm_model("t5-lm", "google/t5-large-lm-adapt")
        builder.set_template("soft", 'The {"placeholder":"text_a"} label from web forms. If I want to make the web through a error, The label belong to what category is best one? {"mask"}')
        builder.set_verbalizer("manual", PromptModelDirector.classes, "manual_verbalizer.txt")
        builder.set_state_dict("C:\\Users\\ligii\IdeaProjects\\rlenvforapp\\7649063101.ckpt")
        return builder.get_result()

    @staticmethod
    def get_prompt_data_loader(builder: PromptModelBuilder, input_example: InputExample) -> PromptDataLoader:
        return PromptDataLoader(
            dataset=[input_example],
            tokenizer=builder.get_tokenizer(),
            template=builder.get_template(),
            tokenizer_wrapper_class=builder.get_wrapper_class(),
            max_seq_length=480,
            decoder_max_length=3,
            batch_size=1, shuffle=False,
            teacher_forcing=False,
            predict_eos_token=False,
            truncate_method="tail"
        )
