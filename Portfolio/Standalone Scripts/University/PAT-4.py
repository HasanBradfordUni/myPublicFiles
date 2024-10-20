#Tasks from pat4
def reverseDigits(num):
    numAsString = str(num)
    return int(numAsString[::-1])

def pattern1():
    num = 1
    string = "*"
    while num < 5:
        print(string*num)
        num += 1

def pattern2():
    nums = [1,3,5,3,1]
    index = 0
    string = "*"
    while index < 5:
        print(nums[index]*string)
        index += 1

def pattern3():
    i = 1
    j = 2
    while i>=1:
        a = " "*j+"*"*i+" "*j
        print(a)
        i = i+2
        j = j-1
        if i>5:
            break
    i = 3
    j = 1
    while i>=1:
        a = " "*j+"*"*i+" "*j
        print(a)
        i = i-2
        j = j+1

if __name__ == "__main__":
    pattern3()
