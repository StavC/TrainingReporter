from tkinter import *
from tkinter import messagebox
from tkinter import Scrollbar
from tkinter import font
from User import User
from DataBase import *
import matplotlib.pyplot as plt



class GUI():

    def __init__(self, master):

        self.conn = create_connection("D:\SQLlite\\UsersData.db")
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
        self.full_report_button = Button(self.frame, text="דוח התקדמות מלא", state="disabled",
                                         command=self.print_full_report_button_function)
        self.full_report_button.grid(column=2, row=0, sticky=S)
        self.search = StringVar()
        self.search_field = Entry(self.frame, width=20, textvariable=self.search)
        self.search_field.grid(column=3, row=0, sticky=(S, E))
        self.search_button = Button(self.frame, text="חיפוש", width=10, command=self.search_user_button_function)
        self.search_button.grid(column=4, row=0, sticky=(S, E))
        self.personal_info_label = Label(self.frame, text="פרטים אישיים ", font="Helvetica 12 underline")
        self.id_label = Label(self.frame, text=":תז")
        self.fname_label = Label(self.frame, text=":שם פרטי")
        self.lname_label = Label(self.frame, text=":שם משפחה")
        self.age_label = Label(self.frame, text=":גיל")
        self.gender_label = Label(self.frame, text=":מין")
        self.height_label = Label(self.frame, text=":גובה")
        self.weight_label = Label(self.frame, text=":משקל")
        self.personal_info_label.grid(column=10, row=1, sticky=(E, S))
        self.id_label.grid(column=10, row=2, sticky=(E, S))
        self.fname_label.grid(column=10, row=3, sticky=(E, S))
        self.lname_label.grid(column=10, row=4, sticky=(E, S))
        self.age_label.grid(column=10, row=5, sticky=(E, S))
        self.gender_label.grid(column=10, row=6, sticky=(E, S))
        self.height_label.grid(column=10, row=7, sticky=(E, S))
        self.weight_label.grid(column=10, row=8, sticky=(E, S))
        self.single_report_button=Button(self.frame,text="הפקת דוח יחיד",command=self.single_report_function)
        self.single_report_button.grid(column=2,row=2)
        for child in self.frame.winfo_children(): child.grid_configure(padx=10, pady=5)

        #exercises label and listbox with scroller%
        exercises = []
        scrollbar = Scrollbar(self.frame)
        scrollbar.grid(column=1, row=2, sticky=(N, S))
        self.exercises_list = Listbox(self.frame, listvariable=exercises, height=5, yscrollcommand=scrollbar.set)
        self.exercises_label = Label(self.frame, text="תרגילים ", font="Helvetica 12 underline")
        scrollbar.config(command=self.exercises_list.yview)
        self.exercises_label.grid(column=0, row=1)
        self.exercises_list.grid(column=0, row=2, rowspan=6, sticky=(W, S, N, E))



    def load_user_button_function(self):
        self.curr_user = User.read_csv_create_or_load_user()
        self.running_user_id = self.curr_user.id
        # stav.plot_exercise()
        if check_if_need_to_create(self.conn, self.curr_user.id):
            print("new user created")
            create_new_user(self.conn, self.curr_user)  # new user in DB
        add_exercises_records_to_DB(self.conn, self.curr_user)  # add his exercises to DB
        self.full_report_button.config(state="normal")
        plot_exercises_from_db(self.conn, self.curr_user)
        self.add_personal_info_to_labels()

    def print_full_report_button_function(self):

        if self.running_user_id == "":
            print("load user first no id in ")
        else:
            plot_exercises_from_db(self.conn, self.curr_user)

    def search_user_button_function(self):
        try:
            input_from_search_field = int(self.search.get())
            user_id = search_user(self.conn, input_from_search_field)
            if user_id:
                self.running_user_id = user_id
                self.running_user_id = self.running_user_id[0][0]
                print(self.running_user_id)
                print("User Found!")
                curr = self.conn.cursor()
                curr.execute("SELECT * FROM Users WHERE Id=?", (self.running_user_id,))
                row = curr.fetchall()
                print(row)
                self.curr_user = User(self.running_user_id, row[0][1], row[0][2], row[0][3], row[0][4], row[0][5],
                                      row[0][6])
                self.full_report_button.config(state="normal")
                self.add_personal_info_to_labels()
            else:
                print("User doesnt exist")
                messagebox.showerror("Error", "User dosent exist in DataBase")
                self.curr_user = ""
                self.full_report_button.config(state="disabled")
                self.delete_personal_info_from_labels()
        except ValueError:
            messagebox.showerror("Error", "Enter only numbers (ID)")
            self.curr_user = ""
            self.full_report_button.config(state="disabled")
            self.delete_personal_info_from_labels()
            print("ValueError")

    def add_personal_info_to_labels(self):

        temp = self.curr_user.id
        temp = str(temp)
        self.id_label.config(text="תז: " + temp)
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


        cur = self.conn.cursor()#adding exercises to listbox
        cur.execute("SELECT ExerciseName FROM Exercises WHERE Id=? ", (self.running_user_id,))
        rows = cur.fetchall()
        exercises=[]
        for row in rows:
            exercises.append(row[0])
        self.exercises_list.delete('0','end') #removing old exercises they will be added anyway
        exercises=list(set(exercises))
        for i in exercises:
            self.exercises_list.insert(END,i)


    def delete_personal_info_from_labels(self):
        self.id_label.config(text="תז: ")
        self.fname_label.config(text="שם פרטי: ")
        self.lname_label.config(text="שם משפחה: ")
        self.height_label.config(text="גובה: ")
        self.weight_label.config(text="משקל: ")
        self.gender_label.config(text="מין: ")
        self.age_label.config(text="גיל: ")
        self.exercises_list.delete('0','end')

    def single_report_function(self):
        if self.exercises_list.get(ANCHOR):
            selected=self.exercises_list.get(ANCHOR)
            print(selected)
            curr=self.conn.cursor()
            curr.execute("SELECT Date,Weight FROM Exercises WHERE Id=? AND ExerciseName=?",(self.curr_user.id,selected,))
            rows=curr.fetchall()
            #print(rows)
            temp_list=[]
            dates_list=[]
            weights_list=[]
            for row in rows:
               temp_record=Record(row[1],row[0])
               temp_list.append(temp_record)
            temp_list.sort(key=lambda date: datetime.strptime(date.date, "%d/%m/%Y"))
            for record in temp_list:
                weights_list.append(record.weight)
                dates_list.append(record.date)
            plt.plot(dates_list, weights_list, zorder=1)
            plt.scatter(dates_list, weights_list, s=300,
                        color='red', zorder=2)
            plt.suptitle(selected[::-1])
            plt.show()
        else:
            messagebox.showinfo("select an exercise","please select an exercise from the list")


