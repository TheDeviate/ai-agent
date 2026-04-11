import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)"
            )
        }
    )
)

def get_files_info(working_directory, directory="."):
    abs_working = os.path.abspath(working_directory)
    abs_path = os.path.normpath(os.path.join(abs_working, directory))

    if not os.path.commonpath([abs_working, abs_path]) == abs_working:
        return f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory"
    
    if not os.path.isdir(abs_path):
        return f"{abs_path} is not a directory"

    items = []
    for file in os.listdir(abs_path):
        f = os.path.normpath(os.path.join(abs_path, file))
        items.append(f"{file}: file_size={os.path.getsize(f)} bytes, is_dir={os.path.isdir(f)}")

    return "\n".join(items)