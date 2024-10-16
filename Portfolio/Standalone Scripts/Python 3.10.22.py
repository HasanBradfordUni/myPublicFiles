string = input("Enter something: ")
gg = string.upper()
print(gg)
for num in range(0,len(gg)):
    gg_num = ord(gg[num])-65
    print(gg_num)
