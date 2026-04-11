import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes provided content to file path relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to file that content will be written or overwritten"
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to be written to provided file path"
            )
        }
    )
)

def write_file(working_directory, file_path, content):
    abs_working = os.path.abspath(working_directory)
    abs_path = os.path.normpath(os.path.join(abs_working, file_path))

    if not os.path.commonpath([abs_working, abs_path]) == abs_working:
        return f"Error: Cannot write to \"{file_path}\" as it is outside the permitted working directory"

    if os.path.isdir(abs_path):
        return f"Error: Cannot write to \"{abs_path}\" as it is a directory"

    os.makedirs(os.path.dirname(abs_path), exist_ok=True)

    with open(abs_path, "w") as f:
        f.write(content)

    return f'Successfully wrote to "{abs_path}" ({len(content)} characters written)'
    
