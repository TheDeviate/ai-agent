from functions.get_file_content import get_file_content

print(f"Result for \"main.py\":")
print(get_file_content("calculator", "main.py"))
print(f"Result for \"pkg/calculator.py\":")
print(get_file_content("calculator", "pkg/calculator.py"))
print(f"Result for \"/bin/cat\":")
print(get_file_content("calculator", "/bin/cat"))
print(f"Result for \"pkg/does_not_exist.py\":")
print(get_file_content("calculator", "pkg/does_not_exist.py"))