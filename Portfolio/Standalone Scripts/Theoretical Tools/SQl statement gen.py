#SQL statement generator
import re

data_table = []
temp_statement = input("Enter a template SQL statement: ")
data = " "
while data != "":
    data = input("Enter a data row (Enter to finish): ")
    data_row = data.split()
    data_table.append(data_row)

if temp_statement.startswith("INSERT"):
    start_index = temp_statement.rfind("VALUES (")
    for num in range(int(temp_statement.count(",")/2)):
        pattern = r'.{' + str(start_index) + r'}([^,]*)'
        match = re.search(pattern, temp_statement)
        temp_statement.replace(match, data_table[0][num])
        start_index = temp_statement.rfind(match)
    print(temp_statement)
else:
    print("Not found")
