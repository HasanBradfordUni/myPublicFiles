#SQL statement generator
"""
Description:
This script generates a SQL statement by replacing placeholders in a template SQL statement
with values from a data table as input by the user.
"""

import pyperclip

def insertion_statement(temp_statement, data_table):
    # Replace placeholders in the template SQL statement with values from the data table
    first_row = data_table[0]
    for i in range(1, len(first_row) + 1):
        if first_row[i - 1].isdigit():
            temp_statement = temp_statement.replace(f"'[value-{i}]'", first_row[i - 1])
        else:
            temp_statement = temp_statement.replace(f"[value-{i}]", first_row[i - 1])
    for j in range(1, len(data_table)):
        temp_statement += ", ("
        for h in data_table[j]:
            if h.isdigit():
                temp_statement += h + ", "
            else:
                temp_statement += "'" + h + "', "
        temp_statement = temp_statement[:-2] + ")"
    print("\nThe generated SQL statement is:")
    print(temp_statement)
    return temp_statement

# Function to generate SQL statement
def generate_sql_statement(temp_statement, data_table):
    # Check if the SQL statement is of type INSERT
    if temp_statement.startswith("INSERT"):
        temp_statement = insertion_statement(temp_statement, data_table)
    else:
        print("Support for this type of SQL statement is coming soon!")
    return temp_statement

def process_statement():
    print("Welcome to the official Akhtar Hasan SQL Statement Generator")

    # Get the template SQL statement from the user
    temp_statement = input("Enter a template SQL statement: ")

    # Get the data rows from the user
    data_table = []

    while True:
        data = input("Enter a data row (Enter to finish): ")
        if not data:
            break
        data_row = data.split()
        data_table.append(data_row)
    statement = generate_sql_statement(temp_statement, data_table)

    print("Do you wish to copy the generated SQL statement to the clipboard?")
    copy = input("Enter 'Y' or 'N': ")
    if copy.upper() == 'Y':
        pyperclip.copy(statement)
        print("SQL statement copied to clipboard!")
    else:
        print("SQL statement not copied to clipboard!")
    print("Have a nice day and bye!")

# Generate the SQL statement
process_statement()

