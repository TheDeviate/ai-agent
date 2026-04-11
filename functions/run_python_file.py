import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs python file at a specified file path relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Python file path to run, relative to the working directory"
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="List of arguments to pass to Python file",
                items=types.Schema(
                        type=types.Type.STRING,
                        description="Singular argument to be passed to Python file"
                    )
            )
        }
    )
)

def run_python_file(working_directory, file_path, args=None):
    try:
        abs_working = os.path.abspath(working_directory)
        abs_path = os.path.normpath(os.path.join(abs_working, file_path))

        if not os.path.commonpath([abs_working, abs_path]) == abs_working:
            return f"Error: Cannot execute \"{file_path}\" as it is outside the permitted working directory"
        
        if not os.path.exists(abs_path) or not os.path.isfile(abs_path):
            return f"Error: \"{file_path}\" does not exist or is not a regular file"
        
        if not abs_path.endswith(".py"):
            return f"Error: \"{file_path}\" is not a Python file"
        
        command = ["python", abs_path]

        if args:
            command.extend(args)

        completed_process = subprocess.run(command, text=True, timeout=30, capture_output=True)

        output = ""

        if completed_process.returncode != 0:
            output += f"Process exited with code {completed_process.returncode}"
        
        stdoutput = False

        if completed_process.stdout:
            stdoutput = True
            if not output:
                output += "\n"
            output += f"STDOUT: {completed_process.stdout}"

        if completed_process.stderr:
            stdoutput = True
            if not output:
                output += "\n"
            output += f"STDERR: {completed_process.stderr}"

        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"