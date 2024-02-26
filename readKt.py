import sys
import openai
import os
import re
# Set your OpenAI GPT-3 API key
openai.api_key = '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'
def generate_response1(kotlin_code,test_folder,lang,className):
    
    conversation.append({"role": "user", "content": f"Generate test cases in {lang} code for the following  {lang} code:\n\n{kotlin_code}"})
    if lang=="Kotlin":
        conversation.append({"role": "user", "content": f"Generate test cases in pure kotlin class with name {className} with mockk library and kotlinx:kotlinx-coroutines-test"})
    elif lang=="Java":
        conversation.append({"role": "user", "content": f"Generate test cases in pure java class with name {className} with mockito library and junit 4.13"})
    conversation.append({"role": "user", "content": f"we want the class without any comments or points and assert test case for the given code"})

    # Make the API call to ChatGPT
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        max_tokens=2000  # Adjust max_tokens as needed
    )
    print(response)
    test_cases = response['choices'][0]['message']['content']
   # Save the test cases to the specified filepath
    if lang=="Kotlin":
        kotlin_code_match = re.search(r'```kotlin(.*?)```', test_cases, re.DOTALL)
    if lang=="Java":
        kotlin_code_match  = re.search(r'```java(.*?)```', test_cases, re.DOTALL)
    if kotlin_code_match:
      kotlin_code_test = kotlin_code_match.group(1).strip()
      print(kotlin_code_test)
      file_path = os.path.join(test_folder, className)
      with open(file_path, 'w') as file:
        file.write(kotlin_code_test)
    else:
      print("No Kotlin code found.")
    # print(test_cases)
def read_kotlin_file(file_path):
    if len(sys.argv) != 5:
        print("Usage: python script.py <file_path> <test_folder>")
        sys.exit(1)
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            kotlin_code = file.read()
            print("Generating...")
            # print(kotlin_code)
            return kotlin_code
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error: An unexpected error occurred - {str(e)}")
        return None
# Check if the correct number of command line arguments is provided
if len(sys.argv) != 5:
    print("Usage: python script_name.py <path_to_kotlin_file>")
    sys.exit(1)
# Take the Kotlin source code file path from the command line argument
kotlin_file_path = sys.argv[1]
test_folder = sys.argv[2]
lang=sys.argv[3]
className=sys.argv[4]
# Call the function to read the Kotlin file content
conversation=[]
conversation.append({"role":"system","content":"you are a compiler"})
conversation.append({"role":"system","content":"perform indepth analysis of the given code"})

def main():
    while True:
        print("Press 'y' to generate the test cases, or anything to quit")
        user_input=input("Enter your choice")
        if(user_input=='y'):
            additional_input = input("Anything you want us to take care of ? :")
            conversation.append({"role":"system","content":f"{additional_input}"})
            kotlin_code = read_kotlin_file(kotlin_file_path)
            test_code = generate_response1(kotlin_code,test_folder,lang,className)
        else:
            print("Exiting..Thank you")
if __name__ == "__main__":
    main()



# if kotlin_code is not None:
#     print(kotlin_code)
#     # print("Kotlin test Code:")
#     # print(test_code)
