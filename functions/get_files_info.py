import os

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