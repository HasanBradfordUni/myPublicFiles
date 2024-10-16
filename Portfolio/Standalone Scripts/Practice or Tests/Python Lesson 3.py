#Task 6
temp = int(input("Enter the temperature: "))
humidity = int(input("Enter the humidity(%): "))
window = input("Is the window open or closed? ")
if window == "closed" and (temp > 25 or humidity > 50):
    print("Open the window")
if window == "open" and (temp < 10 or humidity < 50):
    print("Close the window")

