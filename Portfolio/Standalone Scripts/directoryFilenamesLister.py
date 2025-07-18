import os
import pyperclip

def list_filenames_without_extension(directory_path):
    try:
        filenames = os.listdir(directory_path)
        filenames_without_extension = [os.path.splitext(filename)[0] for filename in filenames]
        filenames_string = "\n".join(filenames_without_extension)
        pyperclip.copy(filenames_string)
        print("Filenames copied to clipboard:")
        print(filenames_string)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    directory_path = input("Enter the path of the directory: ")
    list_filenames_without_extension(directory_path)