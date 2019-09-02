from tkinter import *
from tkinter import messagebox
from tkinter import Scrollbar
from tkinter import font
from User import User
from DataBase import *
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
import numpy as np



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
        self.date_label = Label(self.frame, text=":תאריך התחלה")
        self.current_weight_label = Label(self.frame, text=":משקל נוכחי")
        self.personal_info_label.grid(column=10, row=1, sticky=(E, S))
        self.id_label.grid(column=10, row=2, sticky=(E, S))
        self.fname_label.grid(column=10, row=3, sticky=(E, S))
        self.lname_label.grid(column=10, row=4, sticky=(E, S))
        self.age_label.grid(column=10, row=5, sticky=(E, S))
        self.gender_label.grid(column=10, row=6, sticky=(E, S))
        self.height_label.grid(column=10, row=7, sticky=(E, S))
        self.weight_label.grid(column=10, row=8, sticky=(E, S))
        self.date_label.grid(column=10, row=9, sticky=(E, S))
        self.current_weight_label.grid(column=10, row=10, sticky=(E, S))
        #self.gender_review_button = Button(self.frame, text="פילוג מין", command=self.gender_review_function)
       # self.gender_review_button.grid(column=9, row=2, sticky=(E, S))
        self.statics_for_trainer_button = Button(self.frame, text="סטטיסטיקת מתאמנים",
                                                   command=self.statics_for_trainer_function)
        self.statics_for_trainer_button.grid(column=9, row=3, sticky=(E, S))
        self.multi_report_button = Button(self.frame, text="הפקת דוחות נבחרים", command=self.multi_report_function,state="disabled")
        self.multi_report_button.grid(column=2, row=2)
        self.improvment_button=Button(self.frame,text="התקדמות בתרגילים",command=self.improvment_function,state="disabled")
        self.improvment_button.grid(column=2,row=3)
        for child in self.frame.winfo_children(): child.grid_configure(padx=10, pady=5)

        # exercises label and listbox with scroller
        exercises = []
        scrollbar = Scrollbar(self.frame)
        scrollbar.grid(column=1, row=2, sticky=(N, S))
        self.exercises_list = Listbox(self.frame, listvariable=exercises,selectmode='multiple', height=5, yscrollcommand=scrollbar.set)
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
        self.biggest_improvment_button.config(state="normal")
        self.multi_report_button.config(state="normal")
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
                                      row[0][6],row[0][7],row[0][8])
                self.full_report_button.config(state="normal")
                self.improvment_button.config(state="normal")
                self.multi_report_button.config(state="normal")

                self.add_personal_info_to_labels()
            else:
                print("User doesnt exist")
                messagebox.showerror("Error", "User dosent exist in DataBase")
                self.curr_user = ""
                self.full_report_button.config(state="disabled")
                self.improvment_button.config(state="disabled")
                self.multi_report_button.config(state="disabled")
                self.delete_personal_info_from_labels()
        except ValueError:
            messagebox.showerror("Error", "Enter only numbers (ID)")
            self.curr_user = ""
            self.full_report_button.config(state="disabled")
            self.improvment_button.config(state="disabled")
            self.multi_report_button.config(state="disabled")
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
        temp = self.curr_user.start_date
        temp = str(temp)
        self.date_label.config(text="תאריך התחלה: " + temp)
        temp = self.curr_user.current_weight
        temp = str(temp)
        self.current_weight_label.config(text="משקל נוכחי: " + temp)

        cur = self.conn.cursor()  # adding exercises to listbox
        cur.execute("SELECT ExerciseName FROM Exercises WHERE Id=? ", (self.curr_user.id,))
        rows = cur.fetchall()
        exercises = []
        for row in rows:
            exercises.append(row[0])
        self.exercises_list.delete('0', 'end')  # removing old exercises they will be added anyway
        exercises = list(set(exercises))
        for i in exercises:
            self.exercises_list.insert(END, i)

    def delete_personal_info_from_labels(self):
        self.id_label.config(text="תז: ")
        self.fname_label.config(text="שם פרטי: ")
        self.lname_label.config(text="שם משפחה: ")
        self.height_label.config(text="גובה: ")
        self.weight_label.config(text="משקל: ")
        self.gender_label.config(text="מין: ")
        self.age_label.config(text="גיל: ")
        self.date_label.config(text="תאריך התחלה: ")
        self.current_weight_label.config(text="משקל נוכחי: ")
        self.exercises_list.delete('0', 'end')

    def multi_report_function(self):
        if self.exercises_list.curselection():
            pdf = matplotlib.backends.backend_pdf.PdfPages("SelectedReport.pdf")
            selected_list=self.exercises_list.curselection()
            print(selected_list)
            for i in range(0,len(selected_list)):
                  selected=self.exercises_list.get(selected_list[i])
                  curr = self.conn.cursor()
                  curr.execute("SELECT Date,Weight FROM Exercises WHERE Id=? AND ExerciseName=?",
                               (self.curr_user.id, selected,))
                  rows = curr.fetchall()
                  # print(rows)
                  temp_list = []
                  dates_list = []
                  weights_list = []
                  for row in rows:
                      temp_record = Record(row[1], row[0])
                      temp_list.append(temp_record)
                  temp_list.sort(key=lambda date: datetime.strptime(date.date, "%d/%m/%Y"))
                  for record in temp_list:
                      weights_list.append(record.weight)
                      dates_list.append(record.date)
                  fig, ax = plt.subplots()
                  plt.plot(dates_list, weights_list, zorder=1)
                  plt.scatter(dates_list, weights_list, s=10,
                              color='red', zorder=2)
                  plt.suptitle(selected[::-1])
                  plt.setp(ax.xaxis.get_majorticklabels(), rotation=90, ha="right")
                  plt.gcf().subplots_adjust(bottom=0.20)
                  if len(weights_list) > 100:
                      fig.set_size_inches(100, 100)

                  elif len(weights_list) > 90:
                      fig.set_size_inches(90, 90)

                  elif len(weights_list) > 80:
                      fig.set_size_inches(80, 80)

                  elif len(weights_list) > 70:
                      fig.set_size_inches(70, 70)

                  elif len(weights_list) > 60:
                      fig.set_size_inches(60, 60)

                  elif len(weights_list) > 50:
                      fig.set_size_inches(50, 50)

                  elif len(weights_list) > 40:
                      fig.set_size_inches(40, 40)

                  elif len(weights_list) > 30:
                      fig.set_size_inches(30, 30)

                  elif len(weights_list) > 20:
                      fig.set_size_inches(20, 20)

                  pdf.savefig(fig)

            pdf.close()

        else:
            messagebox.showinfo("select an exercise", "please select an exercise from the list")






    def statics_for_trainer_function(self):

        def make_autopct(values):
            def my_autopct(pct):
                total = sum(values)
                val = int(round(pct * total / 100.0))
                return '({v:d})'.format(v=val)

            return my_autopct

        curr = self.conn.cursor()
        curr.execute("SELECT DISTINCT Id,ExerciseName FROM Exercises  ")
        rows = curr.fetchall()
        my_dict = {}
        for row in rows:
            if row[1] not in my_dict:
                my_dict[row[1]] = 1
            else:
                my_dict[row[1]] = my_dict[row[1]] + 1
        labels = []
        counts = []
        for x, y in my_dict.items():
            labels.append(x[::-1])
            counts.append(y)
        fig1, axs = plt.subplots(2, 2)
        axs[0, 0].pie(counts, labels=labels, autopct=make_autopct(counts),
                      shadow=True, startangle=90)
        axs[0, 0].axis('equal')
        temp = "התרגיל פופולרי ביותר"
        axs[0, 0].set_title(temp[::-1])

        curr.execute("SELECT COUNT(DISTINCT Id) FROM Users WHERE Gender=?", ("זכר",))
        rows = curr.fetchall()
        male = rows[0][0]
        curr.execute("SELECT COUNT(DISTINCT Id) FROM Users WHERE Gender=?", ("נקבה",))
        rows = curr.fetchall()
        female = rows[0][0]
        labels = 'רכז', 'הבקנ'
        axs[1, 1].pie([male, female], labels=labels, autopct=make_autopct([male,female]), shadow=True, startangle=90)
        axs[1, 1].axis('equal')
        temp = "מין"
        axs[1, 1].set_title(temp[::-1])

        curr.execute("SELECT StartDate FROM Users")
        rows=curr.fetchall()
        my_dict = {}
        months=[]
        counts=[]
        for row in rows:
            month=datetime.strptime(row[0],"%d/%m/%Y").strftime("%b")
            if month not in my_dict:
                my_dict[month]=1
            else:
                my_dict[month]=my_dict[month]+1
        for x, y in my_dict.items():
            months.append(x)
            counts.append(y)
        axs[0, 1].pie(counts, labels=months, autopct=make_autopct(counts), shadow=True, startangle=90)
        axs[0, 1].axis('equal')
        temp="תאריך התחלה"
        axs[0,1].set_title(temp[::-1])
        curr.execute("SELECT Age FROM Users")
        rows=curr.fetchall()
        my_dict={}
        ages=[]
        counts=[]
        for row in rows:
            if row[0] not in my_dict:
                my_dict[row[0]]=1
            else:
                my_dict[row[0]]=my_dict[ages]+1
        for x,y in my_dict.items():
            ages.append(x)
            counts.append(y)
        axs[1,0].pie(counts,labels=ages,autopct=make_autopct(counts), shadow=True, startangle=90)
        axs[1,0].axis('equal')
        temp="גיל"
        axs[1,0].set_title(temp[::-1])
        plt.show()


    def improvment_function(self):
        curr=self.conn.cursor()
        curr.execute("SELECT * FROM Exercises WHERE Id=?", (self.curr_user.id,))
        rows=curr.fetchall()


        my_exercises_dict = defaultdict(ExerciseArray)
        for row in rows:
            temp_record = Record(row[3], row[2])
            if row[1] not in my_exercises_dict:
                temp_array = ExerciseArray(row[1])
                temp_array.add_record(temp_record)
                my_exercises_dict[row[1]] = temp_array
            else:
                my_exercises_dict[row[1]].add_record(temp_record)

        self.curr_user.my_exercises = my_exercises_dict
        for name in self.curr_user.my_exercises:  # sorting by date
            self.curr_user.my_exercises[name].records_array.sort(key=lambda date: datetime.strptime(date.date, "%d/%m/%Y"))
        min_list=[]
        max_list=[]
        exercises_list_for_min_max=[]
        for exercise in self.curr_user.my_exercises:
            temp_weights=self.curr_user.my_exercises[exercise].get_weights()
            min_list.append(min(temp_weights))
            exercises_list_for_min_max.append(self.curr_user.my_exercises[exercise].name[::-1])
            max_list.append(max(temp_weights)-min(temp_weights))

        ind=np.arange(5)
        width=0.35
        p1=plt.bar(ind,min_list,width,color="blue")
        p2=plt.bar(ind,max_list,width,bottom=min_list,color="cornflowerblue")

        plt.ylabel('משקלים'[::-1])
        plt.title('שיפור במשקל לפי תרגיל'[::-1])
        plt.xticks(ind, exercises_list_for_min_max)
        totalmax=((max(max_list))+(max(min_list)))
        plt.yticks(np.arange(0, totalmax+20, 10))
        plt.legend((p1[0], p2[0]), ('משקל מינימלי בתרגיל'[::-1], 'משקל מקסימלי בתרגיל'[::-1]))
        plt.show()