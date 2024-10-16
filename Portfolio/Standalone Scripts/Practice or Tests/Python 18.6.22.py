import tkinter as tk
import random
#Task 1

def increase():
    value = int(lbl_value["text"])

    lbl_value["text"] = f"{value + 1}"

    print("Value increased to",lbl_value["text"]+"!")


def decrease():
    value = int(lbl_value["text"])

    lbl_value["text"] = f"{value - 1}"

    print("Value decreased to",lbl_value["text"]+"!")

    
window = tk.Tk()


window.rowconfigure(0, minsize=50, weight=1)

window.columnconfigure([0, 1, 2], minsize=50, weight=1)


btn_decrease = tk.Button(master=window, text="-", command=decrease)

btn_decrease.grid(row=0, column=0, sticky="nsew")


lbl_value = tk.Label(master=window, text="0")

lbl_value.grid(row=0, column=1)


btn_increase = tk.Button(master=window, text="+", command=increase)

btn_increase.grid(row=0, column=2, sticky="nsew")


window.mainloop()


#Task 2

def roll():
    number = random.randint(1,6)
    lbl_num["text"] = str(number)
    print("The dice roll is:",lbl_num["text"])

window = tk.Tk()

window.rowconfigure([0, 1], minsize=50)
window.columnconfigure(0, minsize=150)

btn_roll = tk.Button(master=window, text="Roll", command=roll)
btn_roll.grid(row=0, column=0, sticky="nsew")

lbl_num = tk.Label(master=window, text="0")
lbl_num.grid(row=1, column=0)

window.mainloop()


#Task 3

def temp():
    print(f"Temperature entered is: {ent_temperature.get()} \N{DEGREE FAHRENHEIT}")
    fahrenheit = ent_temperature.get()
    celsius = (5 / 9) * (float(fahrenheit) - 32)
    lbl_result["text"] = f"{round(celsius, 2)} \N{DEGREE CELSIUS}"

window = tk.Tk()

window.title("Temperature Converter")
window.resizable(width=True, height=False)

frm_entry = tk.Frame(master=window)

ent_temperature = tk.Entry(master=frm_entry, width=10)
lbl_temp = tk.Label(master=frm_entry, text="\N{DEGREE FAHRENHEIT}")
ent_temperature.grid(row=0, column=0, sticky="e")
lbl_temp.grid(row=0, column=1, sticky="w")

btn_convert = tk.Button(
    master=window,
    text="\N{RIGHTWARDS BLACK ARROW}",
    command=temp
)

lbl_result = tk.Label(master=window, text="\N{DEGREE CELSIUS}")

frm_entry.grid(row=0, column=0, padx=10)
btn_convert.grid(row=0, column=1, pady=10)
lbl_result.grid(row=0, column=2, padx=10)

window.mainloop()


#Task 4

from tkinter.filedialog import askopenfilename, asksaveasfilename

def open_file():
    filepath = askopenfilename(
        filetypes=[("Text Files", "*.txt"),("Pictures", "*.png"), ("All Files", "*.*")]
    )
    if not filepath:
        return
    txt_edit.delete("1.0", tk.END)
    with open(filepath, mode="r", encoding="utf-8") as input_file:
        try:
            text = input_file.read()
            txt_edit.insert(tk.END, text)
        except:
            print("Error opening file")
    window.title(f"Simple Text Editor - {filepath}")

def save_file():
    filepath = asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
    )
    if not filepath:
        return
    with open(filepath, mode="w", encoding="utf-8") as output_file:
        text = txt_edit.get("1.0", tk.END)
        output_file.write(text)
    window.title(f"Simple Text Editor - {filepath}")

window = tk.Tk()

window.title("Simple Text Editor")

window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(1, minsize=800, weight=1)

txt_edit = tk.Text(window)
frm_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)
btn_open = tk.Button(frm_buttons, text="Open", command=open_file)
btn_save = tk.Button(frm_buttons, text="Save As...", command=save_file)

btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky="ew", padx=5)

frm_buttons.grid(row=0, column=0, sticky="ns")
txt_edit.grid(row=0, column=1, sticky="nsew")

window.mainloop()
