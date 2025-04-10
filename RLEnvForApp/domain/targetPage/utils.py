
import difflib



def get_diff_elements(before_action_elements, after_action_elements) -> str:
    diff = difflib.SequenceMatcher()
    diff.set_seq1(before_action_elements)
    diff.set_seq2(after_action_elements)
    opcodes = diff.get_opcodes()
    diff_str = "" 
    for opcode in opcodes:
        tag, _, _, j1, j2 = opcode
        if tag == 'insert':
            diff_str += f"{after_action_elements[j1:j2]} is inserted at {before_action_elements[j1:j2]}\n"
        elif tag == 'replace':
            diff_str += f"{before_action_elements[j1:j2]} is replaced by {after_action_elements[j1:j2]}\n"
        elif tag == 'delete':
            diff_str += f"{before_action_elements[j1:j2]} is deleted\n"
    return diff_str

def get_new_elements(before_action_elements, after_action_elements):
    diff = difflib.SequenceMatcher()
    diff.set_seq1(before_action_elements)
    diff.set_seq2(after_action_elements)
    # print(before_action_elements)
    opcodes = diff.get_opcodes()
    new_elements = "" 
    for opcode in opcodes:
        # print(opcode)
        tag, _, _, j1, j2 = opcode
        if tag == 'insert':
            # diff_str += f"{after_action_elements[j1:j2]}\n"
            new_elements += f"{after_action_elements[j1:j2]} is inserted at {before_action_elements[j1:j2]}\n"
        elif tag == 'replace':
            new_elements += f"{before_action_elements[j1:j2]} is replaced by {after_action_elements[j1:j2]}\n"
    return new_elements
