# AI powered translator

# Import the NLTK library
import nltk, re
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    print("Downloading required NLTK data...")
    nltk.download('punkt_tab')
    nltk.download('punkt')
    nltk.download('wordnet')
    print("NLTK data downloaded successfully!")

lemmatizer = WordNetLemmatizer()
instruction_synonyms = {"INPUT": ['enter', 'type', 'key', 'typeset', 'set' 'keyboard', 'key in', 'record',
                                  'log', 'register', 'write', 'index', 'post', 'insert', 'copy', 'put in',
                                  'list', 'catalog', 'catalogue', 'note', 'document', 'inscribe', 'docket',
                                  'file', 'schedule', 'report', 'chronicle', 'tabulate', 'make an inventory of',
                                  'transcribe', 'mark down', 'commit to paper', 'slate', 'jot down',
                                  'put in writing' 'put on record', 'put down', 'diarize', 'note down',
                                  'detail', 'enroll', 'put down on paper', 'set down', 'take down', 'enrol',
                                  'book', 'show', 'put on file', 'write down', 'enumerate', 'indicate',
                                  'introduce', 'put on paper', 'make a note of', 'minute', 'write in chart',
                                  'inject', 'mark', 'load', 'store', 'capture', 'submit', 'commit', 'feed in code',
                                  'enter data', 'table', 'process', 'type in', 'lodge'],
                        "MULTIPLY": ["multiply", "times"], "OUTPUT": ["output", "print"],
                        "SET": ["set", "assign"], "IF": ["if", "when"], "THEN": ["then", "next"], "ELSE": ["else", "otherwise"],
                        "SELECT": ["select", "choose"], "END": ["end", "finish"], "FOR": ["for", "each"], "REPEAT": ["repeat", "again"],
                        "READ": ["read", "get"], "DO": ["do", "perform"], "WHILE": ["while", "until"]}

def get_synonyms(word):
    synonyms = instruction_synonyms.values()

    return synonyms

def preprocess_input(text):
    """Enhanced preprocessing for natural language input"""
    # Handle common variations and synonyms
    synonyms = {
        'make': 'create', 'build': 'create', 'generate': 'create',
        'display': 'print', 'show': 'print', 'output': 'print',
        'calculate': 'compute', 'find': 'compute',
        'iterate': 'loop', 'repeat': 'loop',
        'condition': 'if', 'check': 'if'
    }

    for old, new in synonyms.items():
        text = text.replace(old, new)

    return text

def extract_entities(text):
    """Extract key entities like variable names, values, operations"""
    import re

    # Extract numbers
    numbers = re.findall(r'\b\d+(?:\.\d+)?\b', text)

    # Extract quoted strings
    strings = re.findall(r'"([^"]*)"', text)

    # Extract variable-like words
    variables = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', text)

    return {
        'numbers': numbers,
        'strings': strings,
        'variables': [v for v in variables if v not in ['create', 'print', 'if', 'for', 'while']]
    }

def advanced_pattern_matching(text):
    """Advanced pattern matching for complex English structures"""
    patterns = {
        # Mathematical operations
        r'add (\w+) and (\w+)': r'\1 + \2',
        r'subtract (\w+) from (\w+)': r'\2 - \1',
        r'multiply (\w+) by (\w+)': r'\1 * \2',
        r'divide (\w+) by (\w+)': r'\1 / \2',

        # Control structures
        r'if (\w+) is greater than (\w+)': r'if \1 > \2:',
        r'if (\w+) equals (\w+)': r'if \1 == \2:',
        r'for each (\w+) in (\w+)': r'for \1 in \2:',
        r'while (\w+) is less than (\w+)': r'while \1 < \2:',

        # Data structures
        r'create a list called (\w+)': r'\1 = []',
        r'create a dictionary called (\w+)': r'\1 = {}',
        r'add (\w+) to (\w+)': r'\2.append(\1)',

        # Input/Output
        r'ask user for (\w+)': r'\1 = input("Enter \1: ")',
        r'display (\w+)': r'print(\1)',
    }

    for pattern, replacement in patterns.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    return text

def read_this_file(filename):
    """Read the contents of a file and return as a list of lines"""
    try:
        with open(filename, 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
        return []

def check_synonyms(instruction):
    words = word_tokenize(instruction)
    words = [lemmatizer.lemmatize(word) for word in words]
    code = ""
    for word in words:
        if word in instruction_synonyms:
            code += instruction_synonyms[word] + "\n"
        else:
            synonyms = get_synonyms(word)
            for synonym in synonyms:
                if synonym in instruction_synonyms:
                    code += instruction_synonyms[synonym] + "\n"
    print(code)
    return code

# Read the English instructions from a file
def read_file(file):
    with open(file, 'r') as f:
        data = f.readlines()
    thisQuery = ''
    for i in range(len(data)):
        thisQuery += data[i]
    queries = thisQuery.split("\n\n")
    return queries

def infer_param_types(code_str, func_name, param_list):
    # Try to infer types from type hints or usage in the function body
    types = {}
    # Check for type hints in the function definition
    func_def_pattern = re.compile(rf"def\s+{func_name}\s*\(([^)]*)\):")
    match = func_def_pattern.search(code_str)
    if match:
        params = match.group(1).split(",")
        for param in params:
            param = param.strip()
            if ":" in param:
                name, type_hint = [x.strip() for x in param.split(":")]
                types[name] = type_hint
    # If no type hint, look for usage in the function body
    func_body_pattern = re.compile(rf"def\s+{func_name}\s*\([^\)]*\):([\s\S]+?)(?=^def\s|\Z)", re.MULTILINE)
    body_match = func_body_pattern.search(code_str)
    if body_match:
        body = body_match.group(1)
        for param in param_list:
            if re.search(rf"{param}\s*[\+\-\*/]", body):
                types[param] = "int"  # Default to int for arithmetic
    return types

def save_code(code, options):
    """Save the translated code to a file"""
    inputs = ""
    function_calls = ""
    current_contents = []
    new_contents = ""
    code_str = "\n".join(code)

    # Regex to find function definitions
    func_pattern = re.compile(r"def\s+(\w+)\s*\(([^)]*)\):")
    matches = func_pattern.findall(code_str)

    for func_name, params in matches:
        param_list = [p.strip().split(":")[0] for p in params.split(",") if p.strip()]
        param_types = infer_param_types(code_str, func_name, param_list)
        for idx, param in enumerate(param_list, 1):
            dtype = param_types.get(param, "str")
            if dtype in ("int", "float", "list"):
                if dtype == "list":
                    inputs += f"{param} = input('Enter {param.replace('_', ' ')} (comma separated): ').split(',')\n"
                else:
                    inputs += f"{param} = {dtype}(input('Enter {param.replace('_', ' ')}: '))\n"
            elif param == "numbers":
                inputs += "numbers = [int(x) for x in input('Enter numbers (comma separated): ').split(',')]\n"
            else:
                inputs += f"{param} = input('Enter {param.replace('_', ' ')}: ')\n"
        # Generate function call
        call = f"print({func_name}({', '.join(param_list)}))\n"
        function_calls += call

    if options["mode"] == 'a':
        current_contents = read_this_file(options["filename"])
        this_index = -1
        inputs_index = -1
        for line in current_contents:
            if line.startswith("if __name__ =="):
                this_index = current_contents.index(line)
            if line.find("Function calls") != -1:
                inputs_index = current_contents.index(line) - 1
        if this_index != -1:
            start_index = this_index
        else:
            start_index = len(current_contents) - 1
        function_calls_index = len(current_contents)
        print(function_calls_index)

        for line in code:
            current_contents.insert(start_index, line)
            start_index += 1
            inputs_index += 1
            function_calls_index += 1
        current_contents.insert(start_index, "\n")
        start_index += 1
        inputs_index += 1
        function_calls_index += 1
        for line in inputs.split("\n"):
            if line.strip() != "":
                this_line = "\t" + line + "\n"
                current_contents.insert(inputs_index, this_line)
                inputs_index += 1
                function_calls_index += 1
        for line in function_calls.split("\n"):
            if line.strip() != "":
                that_line = "\t" + line + "\n"
                current_contents.insert(function_calls_index, that_line)
                function_calls_index += 1

        new_contents = "".join(current_contents)

    else:
        start_index = 0
        inputs_index = 3
        function_calls_index = 6

        for line in code:
            current_contents.append(line+"\n")
            start_index += 1
            inputs_index += 1
            function_calls_index += 1
        current_contents.append('if __name__ == "__main__":\n')
        current_contents.append('\t# User inputs\n')
        for line in inputs.split("\n"):
            if line.strip() != "":
                this_line = "\t" + line + "\n"
                current_contents.insert(inputs_index, this_line)
                inputs_index += 1
                function_calls_index += 1
        current_contents.append("\n")
        current_contents.append('\t# Function calls\n')
        for line in function_calls.split("\n"):
            if line.strip() != "":
                that_line = "\t" + line + "\n"
                current_contents.insert(function_calls_index, that_line)
                function_calls_index += 1

        new_contents = "".join(current_contents)

    with open(options["filename"], 'w') as file:
        file.write(new_contents)

    print(f"\nCode saved to {options['filename']}")
    return options["filename"]

# Mapping from English instructions to Python code snippets
instruction_to_code = {
    "INPUT hours worked": "hours = int(input('Enter hours: '))",
    "MULTIPLY hours worked by rate of pay": "pay = hours * rate",
    "OUTPUT pay": "print('Pay:', pay)",
    "SET hours worked to 40": "hours = 40",
    "IF error found": "if error:",
    'THEN OUTPUT "Error"': 'print("Error")',
    'ELSE OUTPUT "All Fine"': 'else:\n\tprint("All Fine")',
    "SELECT VALUE errorNumber": "match errorNumber:",
    '1: OUTPUT "Error Number 1"': 'case 1: print("Error Number 1")',
    '3: OUTPUT "Error Number 3"': 'case 3: print("Error Number 3")',
    '5: OUTPUT "That\'s a bad miss"': 'case 5: print("That\'s a bad miss")',
    "END SELECT": "\n",
    "FOR EACH employee": "for employee in employees:",
    "REPEAT UNTIL no more employee records": "while count < len(Employees):",
    "READ next employee record": "employee = Employees[count]\n\tcount += 1",
    "READ hours worked": "hours = employee.hours",
    "READ pay rate": "rate = employee.rate",
    "MULTIPLY pay rate by hours worked": "pay = hours * rate",
    "DO WHILE more employee records to process": "while count < len(Employees):",
}

# Translate English instructions to Python code
def translate_instructions_to_code(instructions):
    codeCollection = []
    for instruction in instructions:
        # Tokenize the instruction into sentences
        sentences = nltk.sent_tokenize(instruction)
        # Translate each sentence to code
        code = ""
        for sentence in sentences:
            sentence = sentence.split("\n")
            for thisSentence in sentence:
                indented = False
                if thisSentence[:4] == "    ":
                    thisSentence = thisSentence[4:]
                    indented = True
                if thisSentence in instruction_to_code:
                    if indented:
                        code += "\t" + instruction_to_code[thisSentence] + "\n"
                    else:
                        code += instruction_to_code[thisSentence] + "\n"
                else:
                    print(f"Warning: Could not translate instruction: {thisSentence}")

        codeCollection.append(code)
    return codeCollection


def map_instructions_to_code(instruction):
    """Map a single instruction to its corresponding code"""
    # Preprocess the instruction
    processed_instruction = preprocess_input(instruction)

    # Apply advanced pattern matching
    code = advanced_pattern_matching(processed_instruction)

    # Check if the instruction exists in the direct mapping
    if instruction.strip() in instruction_to_code:
        return instruction_to_code[instruction.strip()]

    # If no direct match, try to find partial matches or synonyms
    for key, value in instruction_to_code.items():
        if key.lower() in instruction.lower() or instruction.lower() in key.lower():
            return value

    # Extract entities and try to build code dynamically
    entities = extract_entities(instruction)

    # If still no match, return the processed instruction as a comment
    if code == processed_instruction:
        return f"# {instruction.strip()}"

    return code

def translation_main():
    # Read English instructions from a file using the function read_file()
    data = read_file('Code.txt')

    # Translate instructions to code
    code = translate_instructions_to_code(data)

    # Write the translated code to a new file
    with open("Translated Code/translated_code.py", "w") as file:
        for line in code:
            file.write(line)


if __name__ == "__main__":
    # Read English instructions from a file using the function read_file()
    data = read_file('Code.txt')
    print(data)

    # Translate instructions to code
    code = translate_instructions_to_code(data)
    print("Code:", code)
    for instruction in data:
        code2 = map_instructions_to_code(instruction)
        print("Code 2:", code2)

    # Write the translated code to a new file
    with open("Translated Code/translated_code.py", "w") as file:
        for line in code:
            file.write(line)
