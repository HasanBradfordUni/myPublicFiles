from tkinter import *
from tkinter import ttk
from time import sleep

def retrieve():
    index = l.curselection()
    item = l.get(index)
    Label(root, text=item).grid(column=1, row=1)

def close():
    global closed
    root.destroy()
    closed = True
    
def selected_item():
    for i in listbox.curselection():
        print(listbox.get(i))

root = Tk()
l = Listbox(root, height=5)
l.grid(column=0, row=0, sticky=(N,W,E,S))
s = ttk.Scrollbar(root, orient=VERTICAL, command=l.yview)
s.grid(column=1, row=0, sticky=(N,S))
l['yscrollcommand'] = s.set
ttk.Button(root, text="Click here", command=retrieve).grid(column=0, row=1, sticky=(W,E))
Button(root, text="Close", command = close).grid(column=2, row=1)
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
for i in range(1,101):
    l.insert('end', 'Line %d of 100' % i)
root.mainloop()

root = Tk()
root.geometry('180x200')
 
listbox = Listbox(root, width=40, height=10, selectmode=MULTIPLE)
 
listbox.insert(1, "Data Structure")
listbox.insert(2, "Algorithm")
listbox.insert(3, "Data Science")
listbox.insert(4, "Machine Learning")
listbox.insert(5, "Blockchain")

btn = Button(root, text='Print Selected', command=selected_item)
 
btn.pack(side='bottom')
listbox.pack()
 
root.mainloop()
