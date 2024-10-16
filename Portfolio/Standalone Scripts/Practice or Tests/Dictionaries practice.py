#Dictionaries practice
"""
class Dictionary(object):
    def __init__(self):
        self.dictionary = {}

    def Insert(self, key, value):
        self.dictionary[key] = value

    def Find(self, key):
        print(self.dictionary[key])

    def Delete(self, key):
        self.dictionary[key] = None

    def return_dictionary(self):
        print(self.dictionary)

#main
dict1 = Dictionary()
dict1.Insert("1","A")
dict1.return_dictionary()
dict1.Find("1")
dict1.Delete("1")
dict1.return_dictionary()
dict1.Find("1")
"""
"""
WordBank = {}
file = open("song.txt", 'r')

for line in file:
    data = line.strip().split(" ")

    for item in data:

        if item in WordBank.keys():
            WordBank[item] = WordBank[item] + 1

        else:
            WordBank[item] = 1

file.close()

items = WordBank.items()

for item in items:
    print(item, end=",")
"""

lettersDict = {"A": 1, "B": 3, "C": 3, "D": 2, "E": 1, "F": 4, "G": 2, "H": 4, "I": 1,
               "J": 8, "K": 5, "L": 1, "M": 3, "N": 1, "O": 1, "P": 3, "Q": 10, "R": 1,
               "S": 1, "T": 1, "U": 1, "V": 4, "W": 4, "X": 8, "Y": 4, "Z": 10}

print("Welcome to the official scrabble word score calculator")
word = input("Enter a word to calculate score of: ")

score = 0
for letter in word:
    char = letter.upper()
    score += lettersDict[char]

print("Your score is:",score)
    
