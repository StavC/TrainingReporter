from tkinter import *
from User import User
from DataBase import *


class GUI():

    def __init__(self, master):

        self.conn=create_connection("D:\SQLlite\\UsersData.db")

        self.running_user_id = ""
        self.curr_user = ""

        ### GRID and buttons from here down
        frame=Frame(master)

        frame.grid()
        self.create_user_button = Button(frame, text="Load User",command=self.load_user_button_function )
        self.create_user_button.grid(column=0,row=0,sticky=(S,E))
        self.quit_button=Button(frame,text="Quit", command=frame.quit)
        self.quit_button.grid(column=3,row=0,sticky=(E,S))
        self.full_report_button=Button(frame,text="דוח התקדמות מלא", state="disabled",command=self.print_full_report_button_function)
        self.full_report_button.grid(column=2,row=0,sticky=S)
        self.search=StringVar()
        self.search_field=Entry(frame,width=20, textvariable=self.search)
        self.search_field.grid(column=4,row=0,sticky=(S,E))
        self.search_button=Button(frame,text="חיפוש" ,width=10,command=self.search_user_button_function)
        self.search_button.grid(column=5,row=0,sticky=(S,E))
        for child in frame.winfo_children(): child.grid_configure(padx=10, pady=5)

    def load_user_button_function(self):
        self.curr_user = User.read_csv_create_or_load_user()
        self.running_user_id=self.curr_user.id
        # stav.plot_exercise()
        if check_if_need_to_create(self.conn, self.curr_user.id):
            print("new user created")
            create_new_user(self.conn, self.curr_user)  # new user in DB
        add_exercises_records_to_DB(self.conn, self.curr_user)  # add his exercises to DB
        self.full_report_button.config(state="normal")
        plot_exercises_from_db(self.conn, self.curr_user)

    def print_full_report_button_function(self):

        if self.running_user_id=="":
            print("load user first no id in ")
        else:
            plot_exercises_from_db(self.conn,self.curr_user)

    def search_user_button_function(self):
        try:
            input_from_search_field=int(self.search.get())
            user_id=search_user(self.conn,input_from_search_field)
            if user_id:
                self.running_user_id=user_id
                self.running_user_id=self.running_user_id[0][0]
                print(self.running_user_id)
                print("User Found!")
                curr=self.conn.cursor()
                curr.execute("SELECT * FROM Users WHERE Id=?",(self.running_user_id,))
                row=curr.fetchall()
                print(row)
                self.curr_user=User(self.running_user_id,row[0][4],row[0][3],row[0][2],row[0][1],row[0][5])
                self.full_report_button.config(state="normal")
            else:
                print("User doesnt exist")
                self.curr_user=""
                self.full_report_button.config(state="disabled")
        except ValueError:
            print("ValueError")

