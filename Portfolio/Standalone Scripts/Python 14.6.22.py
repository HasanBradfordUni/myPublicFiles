import tkinter as tk
#Task 1
"""window = tk.Tk()
text_box = tk.Text()
text_box.pack()
"""

#Task 2
"""window = tk.Tk()

frame_a = tk.Frame()
frame_b = tk.Frame()

label_a = tk.Label(master=frame_a, text="I'm in Frame A")
label_a.pack()

label_b = tk.Label(master=frame_b, text="I'm in Frame B")
label_b.pack()

frame_a.pack()
frame_b.pack()

window.mainloop()
"""

#Task 3
window = tk.Tk()
entry = tk.Entry(bg="white", fg="black", width=40)
entry.pack()
entry.insert(0, "What is your name?")
