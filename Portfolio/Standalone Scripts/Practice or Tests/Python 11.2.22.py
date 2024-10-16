#2D array practice
import random

def menu():
    print("""1. Play game
2. Quit""")

def menuChoice():
    choice = input("Which option do you choose? ")
    return choice

def grid():
    grid = [["empty","empty","empty","empty","empty","empty","empty","empty"],
            ["empty","empty","empty","empty","empty","empty","empty","empty"],
            ["empty","empty","empty","empty","empty","empty","empty","empty"],
            ["empty","empty","empty","empty","empty","empty","empty","empty"],
            ["empty","empty","empty","empty","empty","empty","empty","empty"],
            ["empty","empty","empty","empty","empty","empty","empty","empty"],
            ["empty","empty","empty","empty","empty","empty","empty","empty"],
            ["empty","empty","empty","empty","empty","empty","empty","start"]]
    print(str(grid).replace(' [', '').replace('[', '').replace(']', ''))
    for x in range(10):
        row = random.randint(0,7)
        column = random.randint(0,7)
        grid[row][column] = "chest"
    for x in range(5):
        row = random.randint(0,7)
        column = random.randint(0,7)
        if grid[row][column] == "empty":
            grid[row][column] = "bandit"
        else:
            row = random.randint(0,7)
            column = random.randint(0,7)
            grid[row][column] = "bandit"

menu()
choice = menuChoice()

while True:
    if choice == "1":
        grid()
        menu()
        choice = menuChoice()
    elif choice == "2":
        print("Program terminating...")
        break
    else:
        print("Invalid choice")
        choice = menuChoice()
