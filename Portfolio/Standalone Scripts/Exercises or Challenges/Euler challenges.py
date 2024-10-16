#Euler challenges

#challenge 1
"""def getMults5(num):
    mults5 = []
    n = 1
    multOf5 = 5
    while multOf5 < num:
        mults5.append(n*5)
        n += 1
        multOf5 += 5
    return mults5

def getMults3(num):
    mults3 = []
    n = 1
    multOf3 = 3
    while multOf3 < num:
        mults3.append(n*3)
        n += 1
        multOf3 += 5
    return mults3

def sumThem(mults3, mults5):
    return sum(mults3)+sum(mults5)
    
mults3 = getMults3(1000)
mults5 = getMults5(1000)
print(sumThem(mults3, mults5))
"""

#challenge 2
"""def isEven(num):
    if num % 2 == 0:
        return True
    else:
        return False

def fibonnaci(num):
    nums = []
    thisNum = 2
    Num = 0
    while Num < num:
        if len(nums) == 0:
            nums.append(1)
            thatNum = 1
            Num = thatNum
        elif len(nums) == 1:
            nums.append(2)
            thatNum = 2
            Num = thatNum
        else:
            prevNum = nums[thisNum-1]
            prevPrevNum = nums[thisNum-2]
            thatNum = prevNum+prevPrevNum
            nums.append(thatNum)
            Num = thatNum
            thisNum += 1
    return nums

def sumEven(nums):
    evenNums = []
    for item in nums:
        if isEven(item):
            evenNums.append(item)
    return sum(evenNums)

nums = fibonnaci(4000000)
print(sumEven(nums))
"""

#challenge 3
"""def isPrime(n):
  for i in range(2,n):
    if (n%i) == 0:
      return False
  return True

def factors(num):
  factors = []
  for i in range(1,num):
    if num % i == 0:
      factors.append(i)
  return factors

def primeFactors(list):
  primeFactors = []
  for item in list:
    if isPrime(item):
      primeFactors.append(item)
  return primeFactors

factors = factors(600851475143)
primeFactors = primeFactors(factors)
print(primeFactors)
"""

#challenge 5
"""def divisible():
    divided = False
    n = 1
    while not divided:
        divided = True
        for num in range(1, 21):
            if n % num != 0:
                divided = False
        n += 1
    return n-1

print(divisible())
"""

#challenge 6
def square(num):
    return num * num

def sumNums(n):
    nums = []
    for h in range(1, n+1):
        nums.append(h)
    sumNums = sum(nums)
    return sumNums

def sumSquares(n):
    squareNums = []
    for i in range(1, n+1):
        num = square(i)
        squareNums.append(num)
    sumSquares = sum(squareNums)
    return sumSquares

def difference(num1, num2):
    return num1 - num2

sumSquared = square(sumNums(100))
sumSquares = sumSquares(100)
print(difference(sumSquared, sumSquares))
    
