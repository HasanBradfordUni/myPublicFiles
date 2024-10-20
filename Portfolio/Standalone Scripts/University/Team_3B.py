"""A program dealing with problem 8 in the coursework
that use merge sort (modified version) to sort the cards
after the user has entered them and they are sorted
in reverse order as per the problem specification"""

#Beginning of the code simply creating the merge_sort function
def merge_sort(cards):
    if len(cards) <= 1: #checks if the length of cards is less than or equal to 1
        return cards #if it is, doesn't need to sort so returns the Cards as they are
    
    mid = len(cards) // 2 #calculates the middle index of the Cards list

    #recursively calls the merge_sort function for the left side of the list and then the right side of the list
    left = merge_sort(cards[:mid]) 
    right = merge_sort(cards[mid:]) 
    
    return merge(left, right) #returns the result of the merge function (below)

#The merge function which will linearly merge the elements of the list together in sorted order 
def merge(left, right): 
    result = []
    i = j = 0 

    while i < len(left) and j < len(right):
        if left[i] < right[j]: 
            result.append(left[i]) 
            i += 1 
        else: 
            result.append(right[j]) 
            j += 1

    result.extend(left[i:]) 
    result.extend(right[j:])

    return result

#The function that will sort the cards and call the merge_sort function to do this
def sort_cards(cards):
 sortedCards = merge_sort(cards) #stores the result of the merge_sort method as sortedCards

 return sortedCards #returns ths result to the main part of the program

cards = [] #initialises cards list
more_cards = True #initialising a boolean vraiable to control the loop
#a while loop for the user to continue entering cards as integers until they enter False
while more_cards: 
    card = int(input("Enter card: ")) #prompts the user to enter a card
    cards.append(card) #appends the card to the cards list
    #prompts the user to enter a boolean as the loop variable
    more_cards = input("Do you wish to add more cards (True/False)? ")
    if more_cards.lower() == "true":
        more_cards = True
    else:
        more_cards = False

#sorting the cards in reverse order to begin with
cards.sort(reverse=True)

#calling the sort_cards method that follows the specification
sorted_cards = sort_cards(cards)

#outputs the original cards (reverse order cards) and sorted cards to the shell
print("Original cards:",cards)
print("Sorted cards:",sorted_cards)

