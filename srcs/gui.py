from tkinter import *

root = Tk()

e = Entry(root, width=50)
e.pack()

def myClick():
	c_label = Label(root, text=e.get())
	print(e.get())

myButton = Button(root, text="Enter your name", command=myClick)
myButton.pack()

root.mainloop()