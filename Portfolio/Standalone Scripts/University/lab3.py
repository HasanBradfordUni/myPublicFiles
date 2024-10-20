def f(B1,B2,B3):
    if B1:
        value = 1
    elif B2:
        value = 2
    elif B3:
        value = 3
    else:
        value = 4
    return value

def  MyCount(x,S):
   """Returns an int that is the number of times x occurs in S
    x  is  a  character  and  S  is  a  string """
   N = 0
   for  c  in  S:
       if x==c:
           N = N+1
   return N

def new(S):
    k = 0
    T = '' # The empty string
    for c in S:
        if k%2==0:
            T = c + T
        k = k+1
    print(T)

#print(MyCount("a","I have an apple"))
              
#new('abcde')

for num in range(5):
    number = num + 1
    for i in range(number):
        print(i+1, end=" ")
    print()
