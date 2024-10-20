#Goals challenge outcome calculator

def findHistory(currentGoals):
	#This function will search for a file called challengeHistory.txt and return the summary statistics
	try:
		file = open("challengeHistory.txt", 'r')
		#Read the file and split the contents into a list
		contents = file.read().split("\n")
		#Close the file
		file.close()
		#Create a list to store the contents of the file
		attempts = 1
		historicalTotals = []
		historicalAccuracies = []
		#Iterate through the contents of the file
		for line in contents:
			#Split the line into a list
			line = line.split(",")
			goals = int(line[0][7:])
			if goals == currentGoals:
				attempts += 1
				total = int(line[1][15:])
				bestTotal = int(line[2][13:])
				accuracy = float(total / bestTotal * 100)
				#Append the line to the history list
				historicalTotals.append(total)
				historicalAccuracies.append(accuracy)
		#Return the history list
		return attempts, historicalTotals, historicalAccuracies
	except FileNotFoundError:
		#If the file is not found return a message
		return 1, [], []

combos = {200000: [10,10,10,10,10,25,25,25,25,25,35,35,35,35,50], 100000: [8,8,8,9,9,9,10,10,10,10,10,10,10,11,11,11,11,11,11,11,12,12], 10000: [1,1,1,2,2,2,3,3,4,5], 20000: [2,2,2,2,2,3,3,3,3,3,4,4,4,4,4,5,5,5,5,5], 9000: [1,1,1,2,2,2,3,3,4,4], 7000: [1,1,1,2,2,2,2,3,3,4]}

print("""Choose a goals target for the challenge, possible targets are below:
	1. 7000 goals
	2. 9000 goals
	3. 10,000 goals
	4. 20,000 goals
	5. 100,000 goals
	6. 200,000 goals
Type the number of your choice, e.g. for 10,000 goals choose 3""")
choice = input()

if choice == "1":
	choice = 7000
	print("You chose 7000 goals!")
elif choice == "2":
	choice = 9000
	print("You chose 9000 goals!")
elif choice == "3":
	choice = 10000
	print("You chose 10,000 goals!")
elif choice == "4":
	choice = 20000
	print("You chose 20,000 goals!")
elif choice == "5":
	choice = 100000
	print("You chose 100,000 goals!")
else:
	choice = 200000
	print("You chose 200,000 goals!")

choiceCombos = combos[choice]

print("The following combos are associated with this target:\n")
totalGoals = []
playerGoalsMapping = {}
for combo in choiceCombos:
	print("The multiplier is:",str(combo))
	chosenPlayer = input("Enter the player chosen with this multiplier: ")
	chosenGoals = int(input("Enter the number of goals he has with the multiplier: "))
	goals = int(chosenGoals // combo)
	playerGoalsMapping[goals] = chosenPlayer
	totalGoals.append(goals)

normalOutcome = 0
bestOutcome = 0
worstOutcome = 0
for num in range(len(totalGoals)):
	normalOutcome += totalGoals[num]*choiceCombos[num]
#Order the total goals in ascending order
totalGoals.sort()
print("\nThe best possible result for the amount of goals for each combo are:\n")

for num in range(len(totalGoals)):
	print("Multiplier:",choiceCombos[num],"Goals:",totalGoals[num]*choiceCombos[num],"Player:",playerGoalsMapping[totalGoals[num]])
	bestOutcome += totalGoals[num]*choiceCombos[num]

#Order the total goals in descending order
totalGoals.sort(reverse=True)
print("\nThe worst possible result for the amount of goals for each combo are:\n")
for num in range(len(totalGoals)):
	print("Multiplier:",choiceCombos[num],"Goals:",totalGoals[num]*choiceCombos[num],"Player:",playerGoalsMapping[totalGoals[num]])
	worstOutcome += totalGoals[num]*choiceCombos[num]

#Output the results, best, worst and normal in one string
print("\nYour total goals for the challenge were",normalOutcome,"goals, the best possible outcome was",bestOutcome,"goals and the worst possible outcome was",worstOutcome,"goals.")
difference = bestOutcome - normalOutcome
accuracy = normalOutcome / bestOutcome * 100
attempts, historicalTotals, historicalAccuracies = findHistory(choice)
historicalTotals.sort(reverse=True)
historicalTotal = normalOutcome
attemptRank = 1
totalAccuracies = accuracy
for num in range(len(historicalTotals)):
	if normalOutcome > historicalTotals[num]:
		attemptRank = num + 1
		totalAccuracies += historicalAccuracies[num]
		historicalTotal += historicalTotals[num]
averageAccuracy = round(totalAccuracies / attempts, 1)
averageScore = round(historicalTotal / attempts, 1)
if accuracy > averageAccuracy:
	keyword = "above"
else:
	keyword = "below"
print(f"Your final score of {normalOutcome} goals ranks {attemptRank} out of {attempts} attempts, above the {keyword} score of {averageScore}.")
print(f"The best outcome would be {difference} goals higher meaning you scored {accuracy}% (average {averageAccuracy}%) accuracy.")
if normalOutcome > choice:
	print("Congratulations, you have achieved your target of",choice,"goals!")
else:
	print("Unfortunately you did not achieve your target of",choice,"goals.")
