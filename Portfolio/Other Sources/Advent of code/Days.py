#Day 2
#scores = {"Y": 2, "X": 1, "Z": 3}
"""
def readFile():
    output = []
    file = open('Input2.txt', 'r')
    for line in file:
        output.append(line)
    return output

output = readFile()
score = 0
for item in output:
    choice = item[2]
    loss = False
    draw = False
    win = False
    if (item[0] == "A" and choice == "Z") or (item[0] == "B" and choice == "X") or (item[0] == "C" and choice == "Y"):
        loss = True
    if (item[0] == "C" and choice == "Z") or (item[0] == "A" and choice == "X") or (item[0] == "B" and choice == "Y"):
        draw = True
    if (item[0] == "B" and choice == "Z") or (item[0] == "C" and choice == "X") or (item[0] == "A" and choice == "Y"):
        win = True
    if win:
        score += 6
    if draw:
        score += 3
    if loss:
        score += 0
    score += scores[choice]
print(score)

def readFile():
    output = []
    file = open('Input2.txt', 'r')
    for line in file:
        output.append(line)
    return output

output = readFile()
score = 0
for item in output:
    choice = item[2]
    loss = False
    draw = False
    win = False
    if choice == "X":
        loss = True
        score += 0
    if choice == "Y":
        draw = True
        score += 3
    if choice == "Z":
        win = True
        score += 6
    if win:
        if item[0] == "A":
            score += 2
        if item[0] == "B":
            score += 3
        if item[0] == "C":
            score += 1
    if draw:
        if item[0] == "A":
            score += 1
        if item[0] == "B":
            score += 2
        if item[0] == "C":
            score += 3
    if loss:
        if item[0] == "A":
            score += 3
        if item[0] == "B":
            score += 1
        if item[0] == "C":
            score += 2
print(score)
"""
#Day 5
stacks = []
stack0 = [" "]
stack1 = ["S","P","W","N","J","Z"]
stack2 = ["T","S","G"]
stack3 = ["H","L","R","Q","V"]
stack4 = ["D","T","S","V"]
stack5 = ["J","M","B","D","T","Z","Q"]
stack6 = ["L","Z","C","D","J","T","W","M"]
stack7 = ["J","T","G","W","M","P","L"]
stack8 = ["H","Q","F","B","T","M","G","N"]
stack9 = ["W","Q","B","P","C","G","D","R"]
stacks.append(stack0[::-1])
stacks.append(stack1[::-1])
stacks.append(stack2[::-1])
stacks.append(stack3[::-1])
stacks.append(stack4[::-1])
stacks.append(stack5[::-1])
stacks.append(stack6[::-1])
stacks.append(stack7[::-1])
stacks.append(stack8[::-1])
stacks.append(stack9[::-1])
print(stacks)

def readFile():
  output = []
  file = open('Input5.txt', 'r')
  for line in file:
    line = line.strip().split()
    output.append(line)
  return output    

def move(output, stacks):
    for line in output:
        toAppend = []
        numMoving = int(line[0])
        stackFromNum = int(line[1])
        stackToNum = int(line[2])
        stackFrom = stacks[stackFromNum]
        stackTo = stacks[stackToNum]
        for num in range(numMoving):
            try:
                thisItem = stackFrom.pop()
                toAppend.append(thisItem)
                toAppend = toAppend[::-1]
            except:
                print("")
        for item in toAppend:
            thatItem = item 
            stackTo.append(thatItem)
    return stacks

output = readFile()
for item in output:
    item.remove("move")
    item.remove("from")
    item.remove("to")

stacks = move(output, stacks)
first = ""
print(stacks)
for stack in stacks:
    first += stack[0]
print(first)

