"""A file that will allow the user to keep inputting structured English code until they press enter,
at which point the code will be translated into Python code using the saved model and then saved to a file.
The user can then run the Python code to see if it works as expected.
If there are any errors, the user can fix them and re-run the code."""

import joblib
import os
import pandas as pd
import nltk
from translation import translation_main, save_code
from Error_checker import error_checker_main, check_syntax

# Load the trained model
model = joblib.load('trained_model.pkl')

# Allow the user to input structured English code until they press enter
def get_user_input():
    print("Welcome to the AI-powered code translator!")
    print("You can input structured English code, and it will be translated to Python code.")
    print("Choose 1 of the following options:")
    print("1. Input structured English code (multiline input)")
    print("2. Enter structured English code command (single line input)")
    print("3. Exit")
    choice = input("Enter your choice (1/2/3): ")
    while choice not in ['1', '2', '3']:
        print("Invalid choice. Please try again.")
        choice = input("Enter your choice (1/2/3): ")
    if choice == '1':
        print("You chose to input structured English code (multiline input).")
        user_input = []
        print("Please enter structured English code (press enter to finish):")
        while True:
            line = input()
            if line == "":
                break
            user_input.append(line)
        return user_input
    elif choice == '2':
        print("You chose to enter structured English code command (single line input).")
        user_input = input("Please enter structured English code command: ")
        while user_input == "":
            print("Invalid input. Please try again.")
            user_input = input("Please enter structured English code command: ")
        return user_input
    else:
        print("Exiting the program.")
        return None

def translate_user_input(user_input):
    # Convert the user input to a DataFrame, handling both string and list inputs
    if isinstance(user_input, str):
        df = pd.DataFrame([user_input], columns=['code'])
    else:
        df = pd.DataFrame(user_input, columns=['code'])

    python_code = model.predict(df['code'])
    save_code(python_code, {"mode": "w", "filename": "translated_code1.py"})

    # Save the translated code to a file
    with open("Translated Code/translated_code1.py", "w") as file:
        print("Translated code:")
        for line in python_code:
            variables = []
            function_name = ""
            lines = line.split("/n")
            newLine = ""
            tabbedLines = ""
            for thisLine in lines:
                newLine = thisLine + "\n"
                if thisLine.startswith("def "):
                    function_name = thisLine.split("def ")[1].split("(")[0]
                    variables_part_start = thisLine.find("(")
                    variables_part_end = thisLine.find(")")
                    if variables_part_start != -1 and variables_part_end != -1:
                        variables_part = thisLine[variables_part_start + 1:variables_part_end]
                        if variables_part.find(",") != -1:
                            these_variables = variables_part.split(",")
                            for i in range(len(these_variables)):
                                variables.append(these_variables[i].strip())
                                user_inputs_section += f"{variables[i]} = input('Enter {variables[i]}: ')\n"
                        variables.append(variables_part)
                        user_inputs_section += f"{variables_part} = input('Enter {variables_part}: ')\n"
                    function_calls_section += f"{function_name}({[variable+", " for variable in variables]})\n"
                if newLine.startswith("/t"):
                    newLines = newLine.split("/t")
                    for thatLine in newLines:
                        tabbedLines += thatLine + "\t"
                    newLine = tabbedLines
                file.write(newLine)
        user_inputs = user_inputs_section.split("\n")
        function_calls = function_calls_section.split("\n")
        for line in user_inputs:
            main_section += "\t" + line + "\n"
        for line in function_calls:
            main_section += "\t" + line + "\n"
        file.write("\n" + main_section)
        print("Python code saved to translated_code1.py")

    return python_code

def main():
    user_input = get_user_input()
    if not user_input:
        print("No input provided. Exiting.")
        return

    # Translate the user input to Python code
    python_code = translate_user_input(user_input)

    print("Python code:")
    for line in python_code:
        print(line)

if __name__ == "__main__":
    main()