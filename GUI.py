from tkinter import *
from User import User
from DataBase import *


class GUI():

    def __init__(self):
        root = Tk()  # creating a blank window
        create_widgets(root,User)
        root.mainloop()


def create_widgets(root,User):
    button1 = Button(root, text="Create User")
    button1.grid(row=20, column=10)




