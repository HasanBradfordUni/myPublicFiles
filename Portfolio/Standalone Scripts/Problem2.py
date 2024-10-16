from random import randint

def select_numbers(numbers):
    a = numbers[randint(0, len(numbers)-1)]
    b = numbers[randint(0, len(numbers)-1)]
    while a==b:
        b = numbers[randint(0, len(numbers)-1)]
    numbers.remove(a)
    numbers.remove(b)
    return numbers, abs(a-b)

def generate_numbers(n):
    numbers = []
    for num in range(1, n+1):
        numbers.append(num)
    return numbers

def main():
    numbers = generate_numbers(50)
    for i in range(49):
        numbers, newNum = select_numbers(numbers)
        numbers.append(newNum)
        print(numbers)

if __name__ == "__main__":
    main()
    
