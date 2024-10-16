from tkinter import *

class Window(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry('300x100')
        self.title('Toplevel Window')

        Button(self,text='Close',command=self.destroy).pack(expand=True)

class App(Tk):
    def __init__(self):
        super().__init__()

        self.geometry('300x200')
        self.title('Main Window')

        label1 = Label(self, text="This is a window")
        label1.pack()
        
        Button(self,text='New window',command=self.open_window).pack(expand=True)

    def open_window(self):
        window = Window(self)
        window.grab_set()


if __name__ == "__main__":
    app = App()
    app.mainloop()
