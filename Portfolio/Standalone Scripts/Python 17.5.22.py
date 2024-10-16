#Q1
number = 0
while (number < 1) or (number > 10):
    print("Enter a positive whole number: ")
    number = int(input())
    if number > 10:
        print("Number too large.")
    elif number < 1:
        print("Not a positive number.")
c = 1
for k in range(0, number):
    print(" "+str(c),end="")
    c = (c * (number-1-k)) // (k + 1)
