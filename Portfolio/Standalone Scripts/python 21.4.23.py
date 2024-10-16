import tkinter as tk

class QuestionWindow(tk.Tk):
    def __init__(self):
        super().__init__() #uses the super construcor for 'Tk'

        #set the window attributes up
        self.geometry('2000x500')
        self.title('Questions')
        self.configure(bg="#12AAE6")

questionWin = QuestionWindow()
