import sys
import openai
import os
import re

def setup_openai():
    openai.api_key = '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'  # Fetch API key from environment variable

def generate_response(kotlin_code, test_folder, lang, className, custom_prompt=None,action='t'):
    # Default conversation for generating test cases
    conversationTest = [
        {"role": "system", "content": "You are a Kotlin test case generator."},
        {"role": "user", "content": f"Here is a Kotlin class. Generate test cases for this code:\n\n{kotlin_code}"},
        {"role": "user", "content": f"Create test cases for the class in a pure {lang} class named {className}."},
        {"role": "user", "content": "Generate the output in a code block without comments or explanations, and include assert test cases for the methods."},
        {"role": "user","content":" use the mockk library from Kotlin wherever possible."},
         {"role": "user","content":"Allow user to input the additional class name which also he needs to do mock."},
    ]

    conversationForMock = [
         {"role": "user","content":"Generate a kotlin class using mockk library to mock all methods of the given class.Ensure the generated class contains only the necessary mock setup and no additional comments or extra code  "},
        {"role": "user", "content": "Generate the output in a code block without comments or explanations"},
        {"role": "user","content":" use the mockk library from Kotlin wherever possible."},
        {"role": "user","content":"Generate a kotlin class with in a pure {lang} class named {className}.  using mockk library to mock all methods of the given class.Ensure the generated class contains only the necessary mock setup and no additional comments or extra code  "},
   
    ]
    
    if action=='t':
         conversation = conversationTest
    elif action=='m':
        conversation = conversationForMock
    # If the user provided a custom prompt, append it to the conversation
    if custom_prompt:
        conversation.append({"role": "user", "content": custom_prompt})

    # Make the API call to ChatGPT
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        max_tokens=2000
    )
    

    # Debugging: print the whole response to check what is returned
    print("API Response:", response)

    test_cases = response['choices'][0]['message']['content']
    
    # Update regex to handle possible formatting issues
    code_match = re.search(r'```(?:kotlin|java)?\n(.*?)```', test_cases, re.DOTALL)

    if code_match:
        test_code = code_match.group(1).strip()

        # Print the extracted test code for debugging
        print("Extracted Test Code:\n", test_code)

        # Determine file extension based on language
        extension = "kt" if lang.lower() == "kotlin" else "java"
        file_name = f"{className}Test.{extension}"
        file_path = os.path.join(test_folder, file_name)

        # Debug: Print the file path where the test cases will be saved
        print(f"Saving test cases to: {file_path}")

        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as file:
                file.write(test_code)
            print(f"Test cases saved to {file_path}")
        except PermissionError:
            print(f"Error: Permission denied while writing to '{file_path}'.")
        except Exception as e:
            print(f"Error: An unexpected error occurred while writing to '{file_path}' - {str(e)}")
    else:
        print("No code found in the response. Ensure the API is returning a valid code block.")

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error: An unexpected error occurred - {str(e)}")
        return None

def main():
    if len(sys.argv) != 5:
        print("Usage: python script.py <kotlin_file_path> <language> <test_folder> <class_name>")
        sys.exit(1)

    kotlin_file_path = sys.argv[1]
    lang = sys.argv[2]
    test_folder = sys.argv[3]
    className = sys.argv[4]

    # Ensure the test folder exists
    if not os.path.exists(test_folder):
        print(f"Error: Test folder '{test_folder}' does not exist.")
        sys.exit(1)

    setup_openai()
    
    while True:
        user_input = input("Press 'T' to generate the test cases,press 'M' to generate mock class, 'p' to add a custom prompt, or anything else to quit: ")
        if user_input.lower() == 't':
            kotlin_code = read_file(kotlin_file_path)
            if kotlin_code:
                generate_response(kotlin_code, test_folder, lang, className,'t')
        elif user_input.lower() == 'p':
            custom_prompt = input("Enter your custom prompt: ")
            kotlin_code = read_file(kotlin_file_path)
            if kotlin_code and custom_prompt:
                generate_response(kotlin_code, test_folder, lang, className, custom_prompt,'p')
        elif user_input.lower() == 'm':
            kotlin_code = read_file(kotlin_file_path)
            generate_response(kotlin_code, test_folder, lang, className,'m')
        else:
            print("Exiting... Thank you!")
            break

if __name__ == "__main__":
    main()
