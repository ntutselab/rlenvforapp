class SystemPromptFactory:
    @staticmethod
    def get(selector) -> str:
        if selector == "is_submit_button":
            return "<<SYS>>You are an AI web crawler assistant. Follow the user requirements carefully and The user will give you some web elements. Please answer it is a form submitting button. Please only say yes or no.<<\SYS>>[INST]{prompt}[/INST]"
        elif selector == "is_form_submitted":
            return "<<SYS>>Please only say yes or no. The following sentences describe the changes that occurred before and after the form submission. Please determine whether the submission was successful based on these descriptions. Definition of successful submission: After the form submission, the webpage does not show any error messages or pop-up error windows, and the webpage content undergoes a change.<<\SYS>>[INST]{prompt}[/INST]"
        elif selector == "input_field_category_number":
            return "<<SYS>>The label from web form belong to which category. Please only say the index of the category. category: [ \"first name\", \"last name\", \"email\", \"gender\", \"string\", \"user name\", \"full name\", \"postal code\", \"store name\", \"phone number\", \"street address\", \"city\", \"state\", \"province\", \"region\", \"number\", \"country\", \"display name\", \"address\", \"suburb\", \"company name\", \"card number\", \"expiration date\", \"CVV\", \"date\", ]<<\SYS>>[INST]{prompt}[/INST]"
        elif selector == "select_option":
            return "<<SYS>> Please determine the most appropriate values for the select fields based on the form title, provided input fields with values, feedback, and alert. Selection Criteria:Choose values that best match the requirements of the form's select fields. Special Rule:If the select fields represent a website language selection, choose values that correspond to \"English\" or \"Chinese.\" Output Format: 1. Return the selected values as a string-formatted list, where each element represents the chosen option or value. 2. Maintain the same order as the given select fields. 3. Do NOT format the response as a Python code block. 4. Each element should contain only one selected value. 5. Example of the correct output format: `[\"US\", \"CA\", \"UK\"]`<<\SYS>>[INST]{prompt}[/INST]"
        raise ValueError(f"Invalid selector: {selector}")
