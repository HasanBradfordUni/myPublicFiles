#Question 5
def calc_mode(numbers):
    modes = 0
    mode = 0
    modeNum = 0
    FrequencyCount = {}
    numOfNumbers = len(numbers)
    for num in range(0,numOfNumbers):
        thisNum = numbers[num]
        if thisNum in FrequencyCount.keys():
            FrequencyCount[thisNum] = str(int(FrequencyCount[thisNum]) + 1)
        else:
            FrequencyCount[thisNum] = '1'
    for item in FrequencyCount.items():
        if int(item[1]) >= modeNum:
            modeNum = int(item[1])
            mode = item[0]
            if int(item[1]) == modeNum:
                modes += 1
    if modes > 1:
        print("Data is multimodal")
    else:
        print("Mode of data is: ",mode)

numbers = []
digitsCount = int(input("How many digits do you wish to enter? "))
for num in range(0,digitsCount):
    digit = int(input("Enter a digit: "))
    numbers.append(digit)
calc_mode(numbers)
                  
