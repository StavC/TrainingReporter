from tkinter import *
from tkinter import messagebox
from User import User
from DataBase import *


class GUI():

    def __init__(self, master):

        self.conn=create_connection("D:\SQLlite\\UsersData.db")
        self.frame = Frame(master)
        self.running_user_id = ""
        self.curr_user = ""
        self.create_widgets()



    def create_widgets(self):
        ### GRID and buttons from here down
        self.frame.grid()
        self.create_user_button = Button(self.frame, text="טעינת גילון משתמש", command=self.load_user_button_function)
        self.create_user_button.grid(column=0, row=0, sticky=(S, E))
        self.quit_button = Button(self.frame, text="יציאה", command=self.frame.quit)
        self.quit_button.grid(column=5, row=0, sticky=(E, S))
        self.full_report_button = Button(self.frame, text="דוח התקדמות מלא", state="disabled",                       command=self.print_full_report_button_function)
        self.full_report_button.grid(column=2, row=0, sticky=S)
        self.search = StringVar()
        self.search_field = Entry(self.frame, width=20, textvariable=self.search)
        self.search_field.grid(column=3, row=0, sticky=(S, E))
        self.search_button = Button(self.frame, text="חיפוש", width=10, command=self.search_user_button_function)
        self.search_button.grid(column=4, row=0, sticky=(S, E))
        self.id_label=Label(self.frame,text=":תז")
        self.fname_label=Label(self.frame,text=":שם פרטי")
        self.lname_label=Label(self.frame,text=":שם משפחה")
        self.age_label=Label(self.frame,text=":גיל")
        self.gender_label=Label(self.frame,text=":מין")
        self.height_label=Label(self.frame,text=":גובה")
        self.weight_label=Label(self.frame,text=":משקל")
        self.id_label.grid(column=10,row=2,sticky=(E,S))
        self.fname_label.grid(column=10,row=3,sticky=(E,S))
        self.lname_label.grid(column=10,row=4,sticky=(E,S))
        self.age_label.grid(column=10,row=5,sticky=(E,S))
        self.gender_label.grid(column=10,row=6,sticky=(E,S))
        self.height_label.grid(column=10,row=7,sticky=(E,S))
        self.weight_label.grid(column=10,row=8,sticky=(E,S))
        for child in self.frame.winfo_children(): child.grid_configure(padx=10, pady=5)




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
                self.curr_user=User(self.running_user_id,row[0][1],row[0][2],row[0][3],row[0][4],row[0][5],row[0][6])
                self.full_report_button.config(state="normal")
                self.add_personal_info_to_labels()
            else:
                print("User doesnt exist")
                messagebox.showerror("Error","User dosent exist in DataBase")
                self.curr_user=""
                self.full_report_button.config(state="disabled")
                self.delete_personal_info_from_labels()
        except ValueError:
            messagebox.showerror("Error","Enter only numbers (ID)")
            self.curr_user = ""
            self.full_report_button.config(state="disabled")
            self.delete_personal_info_from_labels()
            print("ValueError")

    def add_personal_info_to_labels(self):

        temp=self.curr_user.id
        temp=str(temp)
        self.id_label.config(text="תז: "+temp)
        temp = self.curr_user.first_name
        temp = str(temp)
        self.fname_label.config(text="שם פרטי: " + temp)
        temp = self.curr_user.last_name
        temp = str(temp)
        self.lname_label.config(text="שם משפחה: " + temp)
        temp = self.curr_user.height
        temp = str(temp)
        self.height_label.config(text="גובה: " + temp)
        temp = self.curr_user.weight
        temp = str(temp)
        self.weight_label.config(text="משקל: " + temp)
        temp = self.curr_user.gender
        temp = str(temp)
        self.gender_label.config(text="מין: " + temp)
        temp = self.curr_user.age
        temp = str(temp)
        self.age_label.config(text="גיל: " + temp)

    def delete_personal_info_from_labels(self):
        self.id_label.config(text="תז: ")
        self.fname_label.config(text="שם פרטי: " )
        self.lname_label.config(text="שם משפחה: ")
        self.height_label.config(text="גובה: ")
        self.weight_label.config(text="משקל: ")
        self.gender_label.config(text="מין: ")
        self.age_label.config(text="גיל: ")
