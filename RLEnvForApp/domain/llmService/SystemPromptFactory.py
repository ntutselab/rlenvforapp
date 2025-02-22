class SystemPromptFactory:
    @staticmethod
    def get(selector) -> str:
        if selector == "is_submit_button":
            return "You are an AI web crawler assistant. Follow the user requirements carefully and The user will give you some web elements. Please answer it is a form submitting button. Please only say yes or no."
        elif selector == "is_form_submitted":
            return "You are an AI web crawler assistant. Follow the user requirements carefully and The user will prompt you for the DOM differences before and after submitting the web form. Please answer whether the form was submitted successfully. Please only say yes or no."
        raise ValueError(f"Invalid selector: {selector}")
