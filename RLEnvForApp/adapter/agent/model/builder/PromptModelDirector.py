from openprompt import PromptModel

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
