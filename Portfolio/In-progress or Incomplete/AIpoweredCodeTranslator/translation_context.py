import re
from translation import advanced_pattern_matching

class TranslationContext:
    def __init__(self):
        self.variables = {}
        self.functions = []
        self.imports = set()
        self.current_scope = 0

    def add_variable(self, name, var_type):
        self.variables[name] = var_type

    def get_indentation(self):
        return "    " * self.current_scope

    def enter_scope(self):
        self.current_scope += 1

    def exit_scope(self):
        self.current_scope = max(0, self.current_scope - 1)

def context_aware_translate(instructions, context):
    """Translate with awareness of context and scope"""
    result = []

    for instruction in instructions:
        # Check if we need imports
        if 'random' in instruction.lower():
            context.imports.add('import random')
        if 'math' in instruction.lower():
            context.imports.add('import math')

        # Process instruction with context
        translated = advanced_pattern_matching(instruction)

        # Add proper indentation
        if translated.strip():
            result.append(context.get_indentation() + translated)

    # Add imports at the beginning
    if context.imports:
        result = list(context.imports) + [''] + result

    return result

def smart_type_inference(code_str, param_name):
    """Smarter type inference based on multiple factors"""
    # Check for explicit type hints
    if f"{param_name}: int" in code_str:
        return "int"
    elif f"{param_name}: float" in code_str:
        return "float"
    elif f"{param_name}: str" in code_str:
        return "str"
    elif f"{param_name}: list" in code_str:
        return "list"

    # Infer from usage patterns
    usage_patterns = {
        r'int\(' + param_name + r'\)': "int",
        r'float\(' + param_name + r'\)': "float",
        r'len\(' + param_name + r'\)': "list",
        param_name + r'\.append': "list",
        param_name + r'\.split': "str",
        param_name + r'\s*[\+\-\*\/]\s*\d+': "int",
        param_name + r'\s*==\s*\d+': "int",
        param_name + r'\s*>\s*\d+': "int",
    }

    for pattern, data_type in usage_patterns.items():
        if re.search(pattern, code_str):
            return data_type

    return "str"  # Default fallback

def interactive_learning():
    """Allow the system to learn from user corrections"""
    corrections_file = "user_corrections.json"

    def save_correction(original, corrected):
        import json
        try:
            with open(corrections_file, 'r') as f:
                corrections = json.load(f)
        except FileNotFoundError:
            corrections = {}

        corrections[original] = corrected

        with open(corrections_file, 'w') as f:
            json.dump(corrections, f, indent=2)

    def load_corrections():
        import json
        try:
            with open(corrections_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    return save_correction, load_corrections