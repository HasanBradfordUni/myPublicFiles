#Tuple test
tuple1 = (1, 2)
tuple2 = (100,50)

x = int(input("Enter an x-coord: "))
y = int(input("Enter an y-coord: "))

try:
    if tuple1[0] < x < tuple2[0] and tuple1[1] < y < tuple2[1]:
        print("Within range!")
    else:
        print("Out of range")
except:
    print("Invalid!")
