class FormElementOutput:
    def __init__(self, action_number, final_submit=False, execute_action_output_is_done=False):
        self.action_number = action_number
        self.final_submit = final_submit
        self.execute_action_output_is_done = execute_action_output_is_done

    def set_action_number(self, action_number):
        self.action_number = action_number
    
    def set_final_submit(self, final_submit):
        self.final_submit = final_submit

    def set_execute_action_output_is_done(self, execute_action_output_is_done):
        self.execute_action_output_is_done = execute_action_output_is_done
    
    def get_action_number(self):
        return self.action_number
    
    def get_final_submit(self):
        return self.final_submit
    
    def get_execute_action_output_is_done(self):
        return self.execute_action_output_is_done
    
    def to_dict(self):
        return {
            "action_number": self.action_number,
            "final_submit": self.final_submit,
            "execute_action_output_is_done": self.execute_action_output_is_done
        }
