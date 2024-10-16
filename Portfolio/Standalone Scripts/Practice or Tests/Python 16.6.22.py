import tkinter as tk
#Task 1
"""
border_effects = {

    "flat": tk.FLAT,

    "sunken": tk.SUNKEN,

    "raised": tk.RAISED,

    "groove": tk.GROOVE,

    "ridge": tk.RIDGE,

}


window = tk.Tk()


for relief_name, relief in border_effects.items():

    frame = tk.Frame(master=window, relief=relief, borderwidth=5)

    frame.pack(side=tk.LEFT)

    label = tk.Label(master=frame, text=relief_name)

    label.pack()


window.mainloop()
"""

#Task 2
"""window = tk.Tk()

frame1 = tk.Frame(master=window, width=100, height=100, bg="red")
frame1.pack()

frame2 = tk.Frame(master=window, width=50, height=50, bg="yellow")
frame2.pack()

frame3 = tk.Frame(master=window, width=25, height=25, bg="blue")
frame3.pack()
"""

#Task 3
"""
window = tk.Tk()


frame = tk.Frame(master=window, width=150, height=150)

frame.pack()


button1 = tk.Button(master=frame, text="I'm at (0, 0)", bg="red")

button1.place(x=0, y=0)


button2 = tk.Button(master=frame, text="I'm at (75, 75)", bg="yellow")

button2.place(x=75, y=75)


window.mainloop()
"""

#Task 4
window = tk.Tk()

for i in range(3):
    window.columnconfigure(i, weight=1, minsize=75)
    window.rowconfigure(i, weight=1, minsize=50)

    for j in range(3):
        frame = tk.Frame(
            master=window,
            relief=tk.RAISED,
            borderwidth=1
        )
        frame.grid(row=i, column=j, padx=5, pady=5)
        button = tk.Button(master=frame, text=f"Row {i}\nColumn {j}")
        button.pack()

window.mainloop()
