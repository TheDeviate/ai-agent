import os
import argparse
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_files_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function
from config import MAX_ATTEMPTS

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("API key not found in .env")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    model_name = "gemini-2.5-flash"
    available_functions = types.Tool(
        function_declarations=[schema_get_files_info, schema_get_files_content, schema_run_python_file, schema_write_file],
    )

    for _ in range(MAX_ATTEMPTS):
        response = client.models.generate_content(
            model=model_name,
            contents=messages,
            config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt, temperature=0)
            )

        if not response.usage_metadata:
            raise RuntimeError("Response metadata does not exist")

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        candidates = response.candidates
        for candidate in candidates:
            messages.append(candidate.content)

        function_results = []

        print(f"Response:")
        if response.function_calls:
            for function_call in response.function_calls:
                print(f"Calling function: {function_call.name}({function_call.args})")

                function_call_result = call_function(function_call)
                if not function_call_result.parts:
                    raise Exception("Function call results has empty parts list")
                
                if not function_call_result.parts[0].function_response:
                    raise Exception("Function response from first part does not exist")
                
                if not function_call_result.parts[0].function_response.response:
                    raise Exception("Rseponse does not exist")
                
                function_results.append(function_call_result.parts[0])

                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
        else:
            print(f"{response.text}")
            return

        messages.append(types.Content(role="user", parts=function_results))
    
    print(f"Model has not reached final response in {MAX_ATTEMPTS}")
    sys.exit(1)

main()