def calcHours(file):
    for line in file:
        line = line.strip()
        newLine = line.split(" ")
        hours = 0
        for i in range(len(newLine)):
            if i > 1:
                hours += float(newLine[i])
        print(newLine[1], "ID:", newLine[0], "Hours:", hours, "Per day:", hours/5)

def Add1(x,y): 
    """
    PreC: x and y are lists of numbers with len(x)==len(y) """
    z = []
    for k in range(len(x)):
        s = x[k]+y[k]
        z.append(s) 
    return z

def Add2(x,y): 
    """
    PreC: x and y are lists of numbers with len(x)==len(y) """
    for k in range(len(x)):
        x[k] = x[k]+y[k]
    return x

def Reverse(x): 
    """
    Returns a list that is the same as x except that the order of its entries is reversed.

    PreC: x is a list of numbers
    """
    y = [] 
    for i in range(len(x)):
        y.append(x[len(x)-i-1])
    return y


if __name__ == "__main__":
    x = [1,2,4,3,5,9,8,3,1]
    print(Reverse(x))



