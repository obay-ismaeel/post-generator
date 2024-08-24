from typing import Literal

def read_file(file_path: str):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return f"Error: The file at path {file_path} was not found."
    except IOError as e:
        return f"Error reading file at path {file_path}: {e}"
    
def get_pov_text(type:Literal['FirstPersonSingular', 'FirstPersonPlural', 'SecondPerson', 'ThirdPerson']):
    if type == 'FirstPersonSingular':
        return 'First person singular(I, me, mine, my)'
    if type == 'FirstPersonPlural':
        return 'First person plural(We, us, our, ours)'
    if type == 'SecondPerson':
        return 'Second Person(you, your, yours)'
    if type == 'ThirdPerson':
        return 'Third Person(he, she, it, they)'