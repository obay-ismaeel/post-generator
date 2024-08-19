def read_file(file_path: str):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return f"Error: The file at path {file_path} was not found."
    except IOError as e:
        return f"Error reading file at path {file_path}: {e}"