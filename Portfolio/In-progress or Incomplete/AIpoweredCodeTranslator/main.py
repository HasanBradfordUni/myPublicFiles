import joblib
import pandas as pd
import nltk
import os
import re
import subprocess
import numpy
import random
from translation import read_file, translate_instructions_to_code, check_synonyms, save_code, translation_main
from Error_checker import error_checker_main, check_syntax

# Load the trained model
try:
    model = joblib.load('trained_model.pkl')
    model_loaded = True
except:
    print("Warning: Trained model not found. Only rule-based translation will be available.")
    model_loaded = False

def clean_file(file):
    """Clean up specific lines in the translated file"""
    if len(file) > 25:
        file[25] = ""
    if len(file) > 33:
        file[33] = ""
    return file

def clean_file2(file):
    """Clean up another set of lines in the translated file"""
    for num in range(min(5, len(file)), min(9, len(file))):
        if num < len(file):
            file[num] = ""
    return file

def get_user_input():
    """Get the structured English code input from the user"""
    print("\n===== AI-POWERED CODE TRANSLATOR =====")
    print("1. Input structured English code (multiline input)")
    print("2. Input single command (model-based translation)")
    print("3. Translate from file")
    print("4. Exit")

    choice = input("\nEnter your choice (1-4): ")

    if choice == '1':
        print("\nEnter your structured English code (press Enter on an empty line to finish):")
        lines = []
        while True:
            line = input()
            if line.strip() == "":
                break
            lines.append(line)
        return {"type": "multiline", "content": lines}

    elif choice == '2':
        if not model_loaded:
            print("Error: Model-based translation requires a trained model.")
            return get_user_input()
        command = input("\nEnter your structured English command: ")
        return {"type": "command", "content": command}

    elif choice == '3':
        filename = input("\nEnter the file path: ")
        if not os.path.exists(filename):
            print(f"Error: File {filename} not found.")
            return get_user_input()
        try:
            data = read_file(filename)
            return {"type": "file", "content": data, "filename": filename}
        except Exception as e:
            print(f"Error reading file: {e}")
            return get_user_input()

    elif choice == '4':
        return {"type": "exit"}

    else:
        print("Invalid choice. Please try again.")
        return get_user_input()

def get_save_options():
    """Get file saving options from the user"""
    print("\n===== SAVE OPTIONS =====")
    filename = input("Enter output filename (default: translated_code.py): ")
    filename = os.path.join("Translated Code", filename.strip())
    if not filename:
        filename = "Translated Code/translated_code.py"

    mode = input("Append or overwrite? (a/w, default: w): ").lower()
    if mode not in ['a', 'w']:
        mode = 'w'

    return {"filename": filename, "mode": mode}

def translate_from_file(filename):
    """Translate from file using the same logic as translation.py"""
    try:
        # Read the file using the same method as translation.py
        data = read_file(filename)

        # Translate instructions to code using the same method
        code = translate_instructions_to_code(data)

        # Return the translated code
        return code
    except Exception as e:
        print(f"Error during file translation: {e}")
        return [f"# Error translating file: {e}"]

def translate_with_model(input_text):
    """Translate using the trained machine learning model"""
    if isinstance(input_text, list):
        df = pd.DataFrame(input_text, columns=['code'])
    else:
        df = pd.DataFrame([input_text], columns=['code'])

    predictions = model.predict(df['code'])
    result = []

    for pred in predictions:
        # Process the model output to convert /n to actual newlines
        lines = pred.split("/n")
        formatted_code = "\n".join(line for line in lines)
        code_lines = formatted_code.split("/t")
        code = ""
        for line in code_lines:
            if not line.startswith("def"):
                code += "\t" + line
            else:
                code += line
        formatted_code = code
        result.append(formatted_code)

    return result

def translate_with_rules(input_text):
    """Translate using the rule-based system from translation.py"""
    if isinstance(input_text, list):
        joined_text = "\n".join(input_text)
        instructions = [joined_text]
    else:
        instructions = [input_text]

    try:
        # Try rule-based translation first
        code = translate_instructions_to_code(instructions)
        return code
    except:
        # If that fails, try synonym-based mapping
        try:
            code = check_synonyms(input_text)
            return [code]
        except:
            return ["# Translation failed. Please check your input."]

def run_error_checker(filename):
    """Run the error checker on the translated code"""
    print("\nChecking for errors...")

    # Ensure the file exists before checking
    if not os.path.exists(filename):
        print(f"Error: File {filename} not found for error checking.")
        return

    parsing_error = False
    errors = check_syntax(filename)
    more_errors = True

    while more_errors:
        has_errors = False
        for error in errors:
            if isinstance(error, str):
                error_lines = error.split("\n")
                for line in error_lines:
                    split_line = line.split(":")
                    if len(split_line) > 3 and (split_line[3] == " E0602" or split_line[3] == " E0601"):
                        has_errors = True
                        parsing_error = error_checker_main()
                        break
                if has_errors:
                    break

        if parsing_error:
            try:
                with open(filename, "r") as file:
                    new_file = clean_file(file.readlines())
                with open(filename, "w") as file:
                    for this_line in new_file:
                        file.write(this_line)
                parsing_error = False
            except Exception as e:
                print(f"Error during file cleaning: {e}")
                break
        elif not has_errors:
            more_errors = False
        else:
            more_errors = False

    # Final cleanup
    try:
        with open(filename, "r") as file:
            new_file = clean_file2(file.readlines())
        with open(filename, "w") as file:
            for this_line in new_file:
                file.write(this_line)
    except Exception as e:
        print(f"Error during final cleanup: {e}")

    print("Error checking complete!")

def main():
    while True:
        # Get user input
        user_input = get_user_input()

        if user_input["type"] == "exit":
            print("Exiting program. Goodbye!")
            break

        # Translate based on input type
        if user_input["type"] == "command" and model_loaded:
            translated_code = translate_with_model(user_input["content"])
        elif user_input["type"] == "file":
            # Use the dedicated file translation function
            translated_code = translate_from_file(user_input["filename"])
        else:
            # For multiline input or if model is not available
            translated_code = translate_with_rules(user_input["content"])

        # Print the translated code
        print("\n===== TRANSLATED CODE =====")
        for code in translated_code:
            print(code)

        # Get save options
        save_options = get_save_options()

        # Ensure the Translated Code directory exists
        os.makedirs("Translated Code", exist_ok=True)

        # Save the code
        saved_file = save_code(translated_code, save_options)

        # Ask if user wants to run error checker
        run_checker = input("\nRun error checker? (y/n, default: y): ").lower()
        if run_checker != 'n':
            run_error_checker(saved_file)

        # Ask if user wants to continue
        continue_translating = input("\nTranslate another code? (y/n, default: y): ").lower()
        if continue_translating == 'n':
            print("Exiting program. Goodbye!")
            break

if __name__ == "__main__":
    # Download NLTK resources if not already downloaded
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        print("Downloading NLTK resources...")
        nltk.download('punkt')
        nltk.download('wordnet')

    main()