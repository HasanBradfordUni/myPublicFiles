# -*- coding: utf-8 -*-
"""Labs-3.1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1pbk6VGBFMwDr5-mq5qM1AHtVx1winHPV

# Python tuples practice
"""

"""Creating a menu to manipulate tuples, methods should include the following:
1. Create an Empty Tuple
2. Create Tuple with Homogeneous Elements
3. Create Tuple with Heterogeneous Elements
4. Create Tuple with Single Element
5. Modify Elements of Tuple
6. Accessing Elements of Tuple – From the Front
7. Accessing Elements of Tuple – From the Back
8. Search Within a Tuple
9. Add Elements to a Tuple
10. Delete an Element from a Tuple
11. Iterate Over a Tuple
12. Concatenation of Tuples
13. Identify Length of a Tuple
14. Slice a Tuple
15. Count the Number of Elements in a Tuple
16. Identify the Index of an Element in a Tuple"""

class TuplePractice:
    def __init__(self):
      self.tuple = ()
      self.menuOptions = {1: "1. Create an Empty Tuple", 2: "2. Create Tuple with Homogeneous Elements", 3: "3: Create Tuple with Heterogeneous Elements", 4: "4. Create Tuple with Single Element", 5: "5. Modify Elements of Tuple",
                     6: "6. Accessing Elements of Tuple – From the Front", 7: "7. Accessing Elements of Tuple – From the Back", 8: "8. Search Within a Tuple", 9: "9. Add Elements to a Tuple",
                     10: "10. Delete an Element from a Tuple", 11: "11. Iterate Over a Tuple", 12: "12. Concatenation of Tuples", 13: "13. Identify Length of a Tuple", 14: "14. Slice a Tuple",
                     15: "15. Count the Number of Elements in a Tuple", 16: "16. Identify the Index of an Element in a Tuple", 17: "17. Exit"}

    def displayMenu(self):
      print("Welcome to the Tuple manipulator, Below are the main menu options\n")
      for option in self.menuOptions.values():
        print(option)

    def getChoice(self):
      print("\nEnter your choice from the options above: ")
      choice = 0
      while choice not in self.menuOptions.keys():
        try:
          choice = int(input("Enter your choice: "))
        except ValueError:
          print("Invalid input. Please enter a number.")
      return choice

    def handleChoice(self, choice):
      print()
      match choice:
        case 1:
          self.createEmptyTuple()
          return False
        case 2:
          self.createHomogeneousTuple()
          return False
        case 3:
          self.createHeterogeneousTuple()
          return False
        case 4:
          self.createSingleElementTuple()
          return False
        case 5:
          self.modifyTuple()
          return False
        case 6:
          self.accessTupleFromFront()
          return False
        case 7:
          self.accessTupleFromBack()
          return False
        case 8:
          self.searchTuple()
          return False
        case 9:
          self.addElementToTuple()
          return False
        case 10:
          self.deleteElementFromTuple()
          return False
        case 11:
          self.iterateOverTuple()
          return False
        case 12:
          self.concatenateTuples()
          return False
        case 13:
          self.identifyLengthOfTuple()
          return False
        case 14:
          self.sliceTuple()
          return False
        case 15:
          self.countNumberOfElements()
          return False
        case 16:
          self.identifyIndexOfElement()
          return False
        case 17:
          self.quit()
          return True
        case _:
          print("Invalid choice. Please try again.")
          return False

    def createEmptyTuple(self):
      self.tuple = ()
      print("Empty tuple created successfully.")

    def createHomogeneousTuple(self):
      self.tuple = (1, 2, 3, 4, 5)
      print("Homogeneous tuple created successfully.")

    def createHeterogeneousTuple(self):
      self.tuple = (1, "apple", 3.14, True)
      print("Heterogeneous tuple created successfully.")

    def createSingleElementTuple(self):
      element = input("Enter the element for the single element tuple: ")
      self.tuple = (element,)
      print("Single element tuple created successfully.")

    def modifyTuple(self):
      if not self.tuple:
        print("Tuple is empty. Cannot modify.")
        return
      else:
        index = int(input("Enter the index of the element to modify: "))
        if index < 0 or index >= len(self.tuple):
          print("Invalid index. Cannot modify.")
        else:
          element = input("Enter the new element: ")
          self.tuple = self.tuple[:index] + (element,) + self.tuple[index+1:]
          print("Element modified successfully.")

    def accessTupleFromFront(self):
      if not self.tuple:
        print("Tuple is empty. Cannot access.")
        return
      else:
        print("Elements of the tuple are as follows:\n")
        for element in self.tuple:
          print(element,end=', ')

    def accessTupleFromBack(self):
      if not self.tuple:
        print("Tuple is empty. Cannot access.")
        return
      else:
        print("Elements of the tuple are as follows:\n")
        for element in reversed(self.tuple):
          print(element,end=', ')

    def searchTuple(self):
      if not self.tuple:
        print("Tuple is empty. Cannot search.")
        return
      else:
        element = input("Enter the element to search for: ")
        if element in self.tuple:
          print("Element found in the tuple.")
          for index in range(len(self.tuple)):
            if self.tuple[index] == element:
              print("Element found at index", index)
          else:
            print("Element not found in the tuple.")

    def addElementToTuple(self):
      element = input("Enter the element to add to the tuple: ")
      self.tuple += (element,)
      print("Element added to the tuple successfully.")

    def deleteElementFromTuple(self):
      if not self.tuple:
        print("Tuple is empty. Cannot delete.")
        return
      else:
        element = input("Enter the element to delete from the tuple: ")
        if element in self.tuple:
          self.tuple = tuple(item for item in self.tuple if item != element)
          print("Element deleted from the tuple successfully.")
        else:
          print("Element not found in the tuple.")

    def iterateOverTuple(self):
      if not self.tuple:
        print("Tuple is empty. Cannot iterate over.")
        return
      else:
        print("Elements of the tuple are as follows:\n")
        for element in self.tuple:
          print(element)

    def concatenateTuples(self):
      tuple1 = (1, 2, 3)
      tuple2 = (4, 5, 6)
      concatenated_tuple = tuple1 + tuple2
      print("Concatenated tuple:", concatenated_tuple)

    def identifyLengthOfTuple(self):
      if not self.tuple:
        print("Tuple is empty. Cannot identify length.")
        return
      else:
        length = len(self.tuple)
        print("Length of the tuple:", length)

    def sliceTuple(self):
      if not self.tuple:
        print("Tuple is empty. Cannot slice.")
        return
      else:
        start = int(input("Enter the starting index: "))
        end = int(input("Enter the ending index: "))
        sliced_tuple = self.tuple[start:end]
        print("Sliced tuple:", sliced_tuple)

    def countNumberOfElements(self):
      if not self.tuple:
        print("Tuple is empty. Cannot count elements.")
        return
      else:
        count = len(self.tuple)
        print("Number of elements in the tuple:", count)

    def identifyIndexOfElement(self):
      if not self.tuple:
        print("Tuple is empty. Cannot identify index.")
        return
      else:
        element = input("Enter the element to identify the index of: ")
        if element in self.tuple:
          index = self.tuple.index(element)
          print("Index of the element:", index)
        else:
          print("Element not found in the tuple.")

    def quit(self):
      print("Thank you for using the Tuple manipulator. Goodbye!")
      exit()

"""## Tests"""

#Main method to run the tuple practice class in a loop

practice = TuplePractice()

practice.displayMenu()

while True:
  choice = practice.getChoice()
  if practice.handleChoice(choice):
    break
  practice.displayMenu()