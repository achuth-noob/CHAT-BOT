from Tkinter import *

# root = Tk()
# The_label = Label(root, text = "Too Easy")
# The_label.pack()
# root.mainloop()

# root = Tk()
# topframe = Frame(root)
# topframe.pack()
# bottomframe = Frame(root)
# bottomframe.pack(side = BOTTOM)
# button1 = Button(topframe, text="OK", fg = "black")
# button1.pack(side=RIGHT)
# root.mainloop()

root = Tk()
one = Label(root,text="One", bg = "red", fg = "white")
one.pack()
two = Label(root,text="Two", bg = "red", fg = "white")
two.pack(fill=X)
root.mainloop()