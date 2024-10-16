#Python Theory
import random
#Task 1
"""playerScore = 0
highScore = 89
playerScore = int(input("Please enter your score: "))
if playerScore < 1 or playerScore > 100:
    print("Invalid score entered")
elif playerScore > highScore:
    print("New high score, well done!")
elif playerScore < highScore:
    print("You did not beat the high score")
else:
    print("You equalled the high score!")
"""

#Task 2
"""guestName = input("What is your name? ")
guestRating = int(input("What do you rate our services? "))
if guestRating <= 2:
    print("We'll try to be better next time!")
elif guestRating > 5:
    print("INVALID rating entered")
else:
    print("Thanks for giving us a good rating!")
"""

#Task 3
"""mark = int(input("Enter your mark: "))
if mark < 50:
    print("FAIL")
elif 50 <= mark <= 64:
    print("Pass")
elif 65<= mark <= 79:
    print("Merit")
else:
    print("Distinction")
"""

#Task 4
"""minutes = int(input("How many minutes have you played computer games for today? "))
if minutes > 120:
    print("You have played games for too long today!")
else:
    print("You are under your time limit!")
"""

#Task 5
"""for roll in range(5):
    CPUroll = random.randint(1, 6)
    userRoll = int(input("Enter a number (1-6): "))
    if userRoll == CPUroll:
        userScore += 10
print("You scored",userScore)
"""    

