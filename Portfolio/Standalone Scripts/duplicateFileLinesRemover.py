print("Welcome to the official Akhtar Hasan Duplicate File Lines remover!")

filepath = input("Enter the path of the file to read: ")
fileContents = []

with open(filepath, 'r') as f:
    fileContents = f.readlines()

text = []
for line in fileContents:
    if line not in text:
        text.append(line)
    else:
        print("Duplicate line!")

outputPath = input("Enter the path of file to save: ")
overwrite = False
sameFile = False

if outputPath == filepath:
    sameFile = True
    print(f"Are you sure you want to overwrite {filepath}?")
    overwrite = input("Enter Y or N: ")
    if overwrite.lower() == "Y":
        overwrite = True

if not sameFile or overwrite:
    with open(outputPath, 'w') as f:
        for line in text:
            f.write(line)

print("Thanks for using the Akhtar Hasan Duplicate File Lines remover!")
                        
