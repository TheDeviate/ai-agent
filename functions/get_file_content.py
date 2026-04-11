import os
from config import MAX_CHARS
from google.genai import types

schema_get_files_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the content of the file located at the provided path relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to get content from, relative to the working directory"
            )
        }
    )
)

def get_file_content(working_directory, file_path):
    abs_working = os.path.abspath(working_directory)
    abs_path = os.path.normpath(os.path.join(abs_working, file_path))

    if not os.path.commonpath([abs_working, abs_path]) == abs_working:
        return f"Error: Cannot read \"{file_path}\" as it is outside the permitted working directory"

    if not os.path.isfile(abs_path):
        return f"Error: File not found or is not a regular file: \"{abs_path}\""

    f = open(abs_path)

    content = f.read(MAX_CHARS)

    if f.read(1):
        content += f"[...File \"{file_path}\" truncated at {MAX_CHARS} characters]"

    return content
    
