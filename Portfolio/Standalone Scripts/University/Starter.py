def loop1():
    i = 0
    word = "Hello"
    while i < len(word):
        print(word[i])
        if word[i] == "e" or word[i] == "o":
            i = i + 1
            continue
        print("Returned letter", word[i])
        i += 1

def loop2():
    p = 16
    sum = 0
    count = 0

    while p > 0:
        count = count + 1
        f = int(input("Enter the number: "))
        sum = sum + f
        p = p - 1
    average = sum / count
    print("result:", average)

def loop3():
    num = 0
    sum = 0

    while num <= 1001:
        sum += num
        num += 1
    return sum

if __name__ == "__main__":
    print(loop3())
