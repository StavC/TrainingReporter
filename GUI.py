from tkinter import *
from User import User
from DataBase import *


class GUI():

    def __init__(self, master):


        frame=Frame(master)
        frame.pack()
        self.button1 = Button(frame, text="Create User",command=self.load_user_button_function )
        self.button1.pack(side=LEFT)
        self.quit_button=Button(frame,text="Quit", command=frame.quit)
        self.quit_button.pack(side=LEFT)



    def load_user_button_function(self):
        curr_user = User.read_csv_create_or_load_user()
        conn = create_connection("D:\SQLlite\\UsersData.db")
        # stav.plot_exercise()
        if check_if_need_to_create(conn, curr_user.id):
            print("new user created")
            create_new_user(conn, curr_user)  # new user in DB
        add_exercises_records_to_DB(conn, curr_user)  # add his exercises to DB
        plot_exercises_from_db(conn, curr_user)