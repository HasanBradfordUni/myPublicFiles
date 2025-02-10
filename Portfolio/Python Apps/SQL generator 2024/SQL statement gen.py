#SQL statement generator
"""
Description:
This script generates a SQL statement by replacing placeholders in a template SQL statement
with values from a data table as input by the user.
"""

import pyperclip
from flask import Flask, render_template, request, jsonify

def insertion_statement(templ_statement, data_table):
    # Replace placeholders in the template SQL statement with values from the data table
    first_row = data_table[0]
    actual_statement = templ_statement
    for i in range(1, len(first_row) + 1):
        if first_row[i - 1].isdigit():
            actual_statement = actual_statement.replace(f"'[value-{i}]'", first_row[i - 1])
        else:
            actual_statement = actual_statement.replace(f"[value-{i}]", first_row[i - 1])
    for j in range(1, len(data_table)):
        actual_statement += ", ("
        for h in data_table[j]:
            if h.isdigit():
                actual_statement += h + ", "
            else:
                actual_statement += "'" + h + "', "
        actual_statement = actual_statement[:-2] + ")"
    print("\nThe generated SQL statement is:")
    print(actual_statement)
    return actual_statement

#Create a function similar to insertion_statement() for delete statements
#The template used should be: DELETE FROM `category` WHERE `category_id`='[value-1]'
def delete_statement(templ_statement, data_table):
    # Replace placeholders in the template SQL statement with values from the data table
    actual_statement = templ_statement
    for i in range(0, len(data_table)):
        if data_table[i][0].isdigit():
            actual_statement = actual_statement.replace(f"'[value-1]'", data_table[i][0])
        else:
            actual_statement = actual_statement.replace(f"[value-1]", data_table[i][0])
    print("\nThe generated SQL statement is:")
    print(actual_statement)
    return actual_statement

#Create a function similar to insertion_statement() to update statements
#The template used should be: UPDATE `category` SET `category_id`='[value-1]',`name`='[value-2]' WHERE 1
def update_statement(templ_statement, data_table):
    # Replace placeholders in the template SQL statement with values from the data table
    edited_statement = templ_statement
    actual_statement = edited_statement
    first_row = data_table[0]
    row_names = []
    if len(data_table) == 1:
        row_names.append(first_row[0])
        for i in range(1, len(first_row) + 1):
            if first_row[i - 1].isdigit():
                edited_statement = edited_statement.replace(f"'[value-{i}]'", first_row[i - 1])
                print("edited statement at this point: ", edited_statement)
            else:
                edited_statement = edited_statement.replace(f"[value-{i}]", first_row[i - 1])
                print("edited statement at this point: ", edited_statement)
        #Create a string that extracts the first column name after SET up until the first equals (=) sign
        actual_statement = edited_statement
    else:
        #format the previous template statement to be like this one
        """UPDATE table_nameSET column_value = CASE column_name
        WHEN ‘column_name1’ THEN column_value1
        WHEN ‘column_name2’ THEN column_value2
        ELSE column_value
        END
        WHERE column_name IN(‘column_name1’, ‘column_name2’)"""
        column_name = templ_statement[templ_statement.find("SET") + 4:templ_statement.find("=")]
        column_value = templ_statement[templ_statement.find("=") + 1:templ_statement.find("WHERE") - 1]
        templ_statement = templ_statement.replace(f"{column_name}='[value-1]'", f"{column_value} = CASE {column_name}\nWHEN 'column_name1' THEN column_value1\nWHEN 'column_name2' THEN column_value2\nELSE {column_value}\nEND\n")
        templ_statement = templ_statement.replace(f"WHERE 1", f"WHERE {column_name} IN('column_name1', 'column_name2')")
        actual_statement = templ_statement
        for i in range(1, len(data_table)):
            if data_table[i-1][0].isdigit():
                edited_statement = actual_statement.replace(f"'[column_name{i}]'", data_table[i-1][0])
            else:
                edited_statement = actual_statement.replace(f"[column_name{i}]", data_table[i-1][0])
            if data_table[i-1][1].isdigit():
                actual_statement = edited_statement.replace(f"'[column_value{i}]'", data_table[i-1][1])
            else:
                actual_statement = edited_statement.replace(f"[column_value{i}]", data_table[i-1][1])

    print("\nThe generated SQL statement is:")
    print(actual_statement)
    return actual_statement

# Function to generate SQL statement
def generate_sql_statement(temp_statement, data):

    data_table = []
    data = data.split('\n')
    for line in data:
        data_row = line.strip('\r').split('  ')
        data_table.append(data_row)

    print(data_table)

    # Check if the SQL statement is of type INSERT
    if temp_statement.startswith("INSERT"):
        temp_statement = insertion_statement(temp_statement, data_table)
    # Then Check if the SQL statement is of type UPDATE
    elif temp_statement.startswith("UPDATE"):
        temp_statement = update_statement(temp_statement, data_table)
    # Then Check if the SQL statement is of type DELETE
    elif temp_statement.startswith("DELETE"):
        temp_statement = delete_statement(temp_statement, data_table)
    else: #Otherwise go to the default output
        temp_statement = "Support for this type of SQL statement is coming soon!"
    return temp_statement

def process_statement():
    print("Welcome to the official Akhtar Hasan SQL Statement Generator")

    # Get the template SQL statement from the user
    temp_statement = input("Enter a template SQL statement: ")

    # Set up string to hold all data
    full_data = ""

    while True:
        data = input("Enter a data row (Enter to finish, Double space [  ] between columns): ")
        if data == " " or data == "":
            full_data = full_data[:-1]
            break
        else:
            full_data += data + "\n"
    statement = generate_sql_statement(temp_statement, full_data)

    print("Do you wish to copy the generated SQL statement to the clipboard?")
    copy = input("Enter 'Y' or 'N': ")
    if copy.upper() == 'Y':
        pyperclip.copy(statement)
        print("SQL statement copied to clipboard!")
    else:
        print("SQL statement not copied to clipboard!")
    print("Have a nice day and bye!")

#Add a Flask method that uses a template webpage to get user input from the webpage
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    template = request.form['template']
    data = request.form['data']
    # Process the inputs as needed
    output = generate_sql_statement(template, data)
    return jsonify({'output': output})

if __name__ == '__main__':
    while True:
        menu = """1. Normal App
2. Web App"""
        print(menu)
        choice = int(input("Enter your choice: "))
        if choice == 1:
            process_statement()
            break
        elif choice == 2:
            app.run('localhost', 6922)
            break
        else:
            print("Invalid choice. Please try again.")

