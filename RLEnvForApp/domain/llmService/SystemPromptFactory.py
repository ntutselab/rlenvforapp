class SystemPromptFactory:
    @staticmethod
    def get(selector) -> str:
        if selector == "is_submit_button":
            return "<<SYS>>You are an AI web crawler assistant. Follow the user requirements carefully and The user will give you some web elements. Please answer it is a form submitting button. Please only say yes or no.<<\SYS>>[INST]{prompt}[/INST]"
        elif selector == "is_form_submitted":
            return "<<SYS>>You are an AI web crawler assistant. Follow the user requirements carefully and The user will prompt you for the DOM differences before and after submitting the web form. Please answer whether the form was submitted successfully. Please only say yes or no.<<\SYS>>[INST]{prompt}[/INST]"
        elif selector == "input_field_category_number":
            return "<<SYS>>The label from web form belong to which category. Please only say the index of the category. category: [ \"first name\", \"last name\", \"email\", \"gender\", \"string\", \"user name\", \"full name\", \"postal code\", \"store name\", \"phone number\", \"street address\", \"city\", \"state\", \"province\", \"region\", \"number\", \"country\", \"display name\", \"address\", \"suburb\", \"company name\", \"card number\", \"expiration date\", \"CVV\", \"date\", ]<<\SYS>>[INST]{prompt}[/INST]"
        raise ValueError(f"Invalid selector: {selector}")
