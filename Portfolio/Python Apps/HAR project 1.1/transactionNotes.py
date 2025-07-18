class TransactionNotes(object):
    def __init__(self):
        self.notes = []

    def addNote(self, transactionID):
        note = input("\nCreate a new note here for the current transaction: ")
        self.notes.append((transactionID, note))
        print("\nThe note has been created!\n")

    def __displayNotes(self):
      counter = 1
      for note in self.notes:
        transactionPart = note[0]
        notePart = note[1]
        print(f"{counter}. Transaction ID: {transactionPart}, Note: {notePart}")

    def deleteNote(self):
      if len(self.notes) < 1:
        print("\nPlease make a note first!\n")
        self.__displayNotes()
        print("\nPlease delete a note from the list (1 -",len(self.notes),"): ")
        while True:
          try:
            choice = int(input("Enter your choice: "))
            if 1 <= choice <= len(self.notes):
              break
            else:
              print("\nInvalid input. Please enter a number between 1 and",len(self.notes),".\n")
              self.__displayNotes()
              print("\nPlease delete a note from the list (0 -",len(self.notes),"): ")
          except ValueError:
            print("\nInvalid input. Please enter a number.\n")
            self.__displayNotes()
            print("\nPlease delete a note from the list (0 -",len(self.notes),"): ")
        self.notes.pop(choice-1)
        print("\nThe note has been deleted!\n")

      def returnNotes(self):
        return self.notes

      def updateNote(self, transactionID):
        if len(self.notes) < 1:
          print("\nPlease make a note first!\n")
        else:
          print("Note with transaction ID", transactionID, "will be updated!")
          for note in self.notes:
            if note[0] == transactionID:
              print("\nThe note is currently:",note[1])
              newNote = input("Enter the updated note: ")
              note[1] = newNote
              print("Note updated!\n")

      def updateNotes(self, newNotes):
        self.notes = newNotes

      def hasNotes(self, transactionID):
        for note in self.notes:
          if note[0] == transactionID:
            return True
        return False

transactionNotes = TransactionNotes()