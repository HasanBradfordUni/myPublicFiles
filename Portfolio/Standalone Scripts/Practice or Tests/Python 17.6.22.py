import tkinter as tk
#Task 1
"""
window = tk.Tk()
window.title("Address Entry Form")

window.rowconfigure([0,1,2,3,4,5,6,7], minsize=50)
window.columnconfigure([0, 1], minsize=30)

frm_form = tk.Frame(relief=tk.SUNKEN, borderwidth=3)
frm_form.pack()

first_name = tk.Label(master=frm_form, text="First name:")
ent_first_name = tk.Entry(master=frm_form, width=50)

first_name.grid(row=0, column=0, sticky="e")
ent_first_name.grid(row=0, column=1)

lbl_last_name = tk.Label(master=frm_form, text="Last Name:")
ent_last_name = tk.Entry(master=frm_form, width=50)

lbl_last_name.grid(row=1, column=0, sticky="e")
ent_last_name.grid(row=1, column=1)

lbl_address1 = tk.Label(master=frm_form, text="Address Line 1:")
ent_address1 = tk.Entry(master=frm_form, width=50)

lbl_address1.grid(row=2, column=0, sticky="e")
ent_address1.grid(row=2, column=1)

lbl_address2 = tk.Label(master=frm_form, text="Address Line 2:")
ent_address2 = tk.Entry(master=frm_form, width=50)

lbl_address2.grid(row=3, column=0, sticky=tk.E)
ent_address2.grid(row=3, column=1)

lbl_city = tk.Label(master=frm_form, text="City:")
ent_city = tk.Entry(master=frm_form, width=50)

lbl_city.grid(row=4, column=0, sticky=tk.E)
ent_city.grid(row=4, column=1)

lbl_state = tk.Label(master=frm_form, text="State/Province:")
ent_state = tk.Entry(master=frm_form, width=50)

lbl_state.grid(row=5, column=0, sticky=tk.E)
ent_state.grid(row=5, column=1)

lbl_postal_code = tk.Label(master=frm_form, text="Postal Code:")
ent_postal_code = tk.Entry(master=frm_form, width=50)

lbl_postal_code.grid(row=6, column=0, sticky=tk.E)
ent_postal_code.grid(row=6, column=1)

lbl_country = tk.Label(master=frm_form, text="Country:")
ent_country = tk.Entry(master=frm_form, width=50)

lbl_country.grid(row=7, column=0, sticky=tk.E)
ent_country.grid(row=7, column=1)

frm_buttons = tk.Frame()
frm_buttons.pack(fill=tk.X, ipadx=5, ipady=5)

btn_submit = tk.Button(master=frm_buttons, text="Submit")
btn_submit.pack(side=tk.RIGHT, padx=10, ipadx=10)

btn_clear = tk.Button(master=frm_buttons, text="Clear")
btn_clear.pack(side=tk.RIGHT, ipadx=10)

window.mainloop()
"""
#Task 2
window = tk.Tk()

def handle_keypress(event):
    print(event.char)

window.bind("<Key>", handle_keypress)

def handle_click(event):
    print("The button was clicked!")

button = tk.Button(text="Click me!")
button.pack()

button.bind("<Button-1>", handle_click)


window.mainloop()
