import tkinter as tk
#Task 1
"""
window = tk.Tk()

label = tk.Label(text="Python rocks!")
label.pack()

button = tk.Button(text="Hasan", fg="#FF2233", bg="white", width=10, height=20)
button.pack()

window.mainloop()
"""
#Task 2
window = tk.Tk()

label = tk.Label(text="Name")
entry = tk.Entry(fg="yellow", bg="blue", width=50)
label.pack()
entry.pack()
name = entry.get()
print(name)
