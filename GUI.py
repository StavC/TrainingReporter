from tkinter import *
from tkinter import messagebox
from tkinter import Scrollbar
from tkinter import font
from User import User
from DataBase import *
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
import numpy as np
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
import inspect
from fpdf import FPDF
from datetime import datetime
from Calendar import MplCalendar
from tkinter import ttk
from bidi.algorithm import get_display

FPDF.SYSTEM_TTFONTS = '/path/to/system/fonts'

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
        self.create_user_button = Button(self.frame, text="טעינת גילון משתמש", command=self.load_user_button_function,
                                         height=1, width=20)
        self.create_user_button.grid(column=0, row=0, sticky=(S, E))
        self.quit_button = Button(self.frame, text="יציאה", command=self.frame.quit, height=1, width=20)
        self.quit_button.grid(column=10, row=0, sticky=(E, S))
        self.full_report_button = Button(self.frame, text="דוח התקדמות מלא", state="disabled",
                                         command=self.print_full_report_button_function, height=1, width=20)
        self.full_report_button.grid(column=2, row=0, sticky=S)
        self.search = StringVar()
        self.search_field = Entry(self.frame, textvariable=self.search, width=25)
        self.search_field.grid(column=3, row=0, sticky=(S, E))
        self.search_button = Button(self.frame, text="חיפוש", command=self.search_user_button_function, height=1,
                                    width=20)
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
        # self.gender_review_button = Button(self.frame, text="פילוג מין", command=self.gender_review_function)
        # self.gender_review_button.grid(column=9, row=2, sticky=(E, S))
        self.statics_for_trainer_button = Button(self.frame, text="סטטיסטיקת מתאמנים",
                                                 command=self.statics_for_trainer_function, height=1, width=20)
        self.statics_for_trainer_button.grid(column=9, row=3, sticky=(E, S))
        self.multi_report_button = Button(self.frame, text="הפקת דוחות נבחרים", command=self.multi_report_function,
                                          state="disabled", height=1, width=20)
        self.multi_report_button.grid(column=2, row=2)
        self.improvment_button = Button(self.frame, text="התקדמות בתרגילים", command=self.improvment_function,
                                        state="disabled", height=1, width=20)
        self.improvment_button.grid(column=2, row=3)
        self.body_weights_button = Button(self.frame, text="מעקב משקל גוף", command=self.body_weights_function,
                                          state="disabled", height=1, width=20)
        self.body_weights_button.grid(column=2, row=4)
        self.load_bench_button = Button(self.frame, text="טעינת בנץ ממוצע", command=self.insert_benchpress_weights,
                                        height=1, width=20)
        self.load_bench_button.grid(column=9, row=4)
        self.load_squat_button = Button(self.frame, text="טעינת סקוואט ממוצע", command=self.insert_squat_weights,
                                        height=1, width=20)
        self.load_squat_button.grid(column=9, row=5)
        self.load_deadlift_button = Button(self.frame, text="טעינת דדליפט ממוצע", command=self.insert_deadlift_weights,
                                           height=1, width=20)
        self.load_deadlift_button.grid(column=9, row=6)
        self.load_headpress_button = Button(self.frame, text="טעינת לחיצת ראש ממוצע",
                                            command=self.insert_headpress_weights, height=1, width=20)
        self.load_headpress_button.grid(column=9, row=7)
        self.user_compare_to_avg_button = Button(self.frame, text="ממוצע משקלים מרכזיים ",
                                                 command=self.user_compare_to_avg_function, state="disabled", height=1,
                                                 width=20)
        self.user_compare_to_avg_button.grid(column=2, row=5)
        self.delete_exercise_button = Button(self.frame, text="מחיקת תרגיל", command=self.delete_exercise_popup,
                                             state="disabled")
        self.delete_exercise_button.grid(column=0, row=8)
        self.targets_button = Button(self.frame, text="עריכת מטרות", command=self.open_targets_frame, height=1,
                                     width=20, state="disabled")
        self.targets_button.grid(column=9, row=8)
        for child in self.frame.winfo_children(): child.grid_configure(padx=10, pady=5)

        # exercises label and listbox with scroller
        exercises = []
        scrollbar = Scrollbar(self.frame)
        scrollbar.grid(column=1, row=2, sticky=(N, S))
        self.exercises_list = Listbox(self.frame, listvariable=exercises, selectmode='multiple', height=5,
                                      yscrollcommand=scrollbar.set)
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
        else:
            curr = self.conn.cursor()
            datetimeObj = datetime.now()
            date_stamp = datetimeObj.strftime("%d/%m/%Y")
            curr.execute("INSERT INTO BodyWeights(Id,Date,Weight)VALUES(?,?,?)",
                         (self.curr_user.id, date_stamp, self.curr_user.current_weight,))

        add_exercises_records_to_DB(self.conn, self.curr_user)  # add his exercises to DB
        self.full_report_button.config(state="normal")
        self.improvment_button.config(state="normal")
        self.multi_report_button.config(state="normal")
        self.body_weights_button.config(state="normal")
        self.user_compare_to_avg_button.config(state="normal")
        self.delete_exercise_button.config(state="normal")
        self.targets_button.config(state="normal")

        plot_exercises_from_db(self.conn, self.curr_user)
        self.add_personal_info_to_labels()

    def print_full_report_button_function(self):

        if self.running_user_id == "":
            print("load user first no id in ")
        else:
            self.create_calendar_function()

            plot_exercises_from_db(self.conn, self.curr_user)
            self.improvment_function()
            self.body_weights_function()
            self.user_compare_to_avg_function()
            self.make_monthly_report()

    def make_summary_page(self):

        pdf = FPDF(orientation='P', format=(290, 300))
        pdf.add_page()
        pdf.add_font('arial', '', 'Fonts\\arial.ttf', uni=True)
        pdf.add_font('Abraham-Regular', '', 'Fonts\\Abraham-Regular.ttf', uni=True)
        pdf.set_font("Abraham-Regular", '', size=10)
        # pdf.cell(200,10,txt=get_display("אז מה היה לנו החודש"),ln=1,align='C')
        curr = self.conn.cursor()
        curr.execute('SELECT * FROM Targets WHERE Id=? AND Status=?', (self.curr_user.id, "הושלמה",))
        rows = curr.fetchall()

        print(len(rows))
        x = 20
        y = 25
        cell_h = 25
        number_in_row = 0

        for i in range(0, len(rows)):
            print(rows[i][1])
            #pdf.set_fill_color(100, 255, 0)
            #pdf.rect(x, y, 70, 70, 'F')
            pdf.image('Inputs\\note.png',x=x,y=y,w=80,h=80)
            text_x=x
            text_y=y
            pdf.set_xy(x+10,y+13)
            last_y=y
            pdf.multi_cell(70,10, txt=get_display("כותרת: " + str(rows[i][1])), align='C',border=0)
            y=y+10
            pdf.set_xy(x+8, y+10)
            pdf.multi_cell(70,10, txt=get_display("משקל מטרה: " + str(rows[i][2])), align='R',border=0)
            y = y + 10
            pdf.set_xy(x+8, y+10)
            pdf.multi_cell(70,10, txt=get_display("תרגיל: " + str(rows[i][3])), align='R',border=0)
            y = y + 10
            pdf.set_xy(x, y)

            y=last_y
            #pdf.cell(10, h=cell_h, txt="",border=3)
            #pdf.text(x+5 , y+5, txt=get_display("כותרת: "+str(rows[i][1])))
            number_in_row += 1
            x += 90

            if number_in_row == 3:
                number_in_row = 0
                x = 20
                y += 90


            # pdf.rect(110,20,70,70,'F')
            # pdf.rect(200,20,70,70,'F')

        '''
        for row in rows:

                # Enter data in colums
                # Notice the use of the function str to coerce any input to the
                # string type. This is needed
                # since pyFPDF expects a string, not a number.
                pdf.cell(col_width, row_height*2, txt=get_display(str(row[1])), border=1)
                pdf.cell(col_width, row_height*2, txt=str(row[2]), border=1)
                pdf.cell(col_width, row_height*2, txt=get_display(str(row[3])), border=1)
                pdf.cell(col_width, row_height*2, txt=get_display(str(row[4])), border=1)
                pdf.cell(col_width, row_height*2, txt=get_display(str(row[5])), border=1)
                pdf.cell(col_width, row_height*2, txt=str(row[6]), border=1)
                pdf.cell(col_width, row_height*2, txt=str(row[7]), border=1)

                #pdf.cell(col_width, row_height, txt=str(item)[::-1], border=1)
                pdf.ln(row_height)
        '''
        pdf.output('OutPuts\\simple_table.pdf')

    def make_monthly_report(self):

        self.make_summary_page()
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('arial', '', 'Fonts\\arial.ttf', uni=True)
        pdf.add_font('Abraham-Regular', '', 'Fonts\\Abraham-Regular.ttf', uni=True)
        pdf.set_font("Abraham-Regular", '', size=20)
        welcome = f" ברוך הבא לדוח החודשי {self.curr_user.first_name} {self.curr_user.last_name}!"[::-1]
        pdf.cell(200, 10, txt=welcome, ln=1, align="C")
        pdf.image('Inputs\\WhyFitness.jpg', x=None, y=None, w=190, h=80, type='', link='')
        pdf.ln(h='200')
        pdf.ln(h='200')
        curr = self.conn.cursor()
        curr.execute("SELECT COUNT(Id) FROM BodyWeights WHERE Id=?", (self.curr_user.id,))

        rows = curr.fetchall()
        # pdf.line(0, 130, 300, 130)
        pdf.set_font("Abraham-Regular", '', size=15)
        details = f" משקל כרגע:  {str(self.curr_user.current_weight)[::-1]} \n תאריך התחלה: {str(self.curr_user.start_date)[::-1]} \n גיל: {str(self.curr_user.age)[::-1]} \n מין: {self.curr_user.gender} \n משקל התחלה: {str(self.curr_user.weight)[::-1]} \n גובה: {str(self.curr_user.height)[::-1]} \n מספר זהות: {str(self.curr_user.id)[::-1]} \n שם משפחה: {self.curr_user.last_name} \n שם פרטי: {self.curr_user.first_name} \n חודש מספר: {str(rows[0][0])[::-1]}"[
                  ::-1]
        pdf.image('OutPuts\\Calander.png', x=0, y=130, w=150, h=140, type='', link='')
        pdf.image('Inputs\\BeastMode.jpg', x=150, y=230, w=60, h=60, type='', link='')
        pdf.multi_cell(200, 10, txt=details, align="R")
        pdf.output("OutPuts\\Front.pdf")

        file0 = PdfFileReader('OutPuts\\Front.pdf', "rb")
        file1 = PdfFileReader('OutPuts\\CompareMySelf.pdf', "rb")
        file2 = PdfFileReader('OutPuts\\DiagramWeights.pdf', "rb")
        file3 = PdfFileReader('OutPuts\\FullExercisesReport.pdf', "rb")
        file4 = PdfFileReader('OutPuts\\BodyWeights.pdf', "rb")

        output = PdfFileWriter()
        output.addPage(file0.getPage(0))
        output.addPage(file2.getPage(0))
        output.addPage(file1.getPage(0))
        output.addPage(file4.getPage(0))
        output.appendPagesFromReader(file3)
        outputStream = open('OutPuts\\MonthlyReport.pdf', "wb")
        output.write(outputStream)
        outputStream.close()

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
                                      row[0][6], row[0][7], row[0][8])
                self.full_report_button.config(state="normal")
                self.improvment_button.config(state="normal")
                self.multi_report_button.config(state="normal")
                self.body_weights_button.config(state="normal")
                self.user_compare_to_avg_button.config(state="normal")
                self.delete_exercise_button.config(state="normal")
                self.targets_button.config(state="normal")

                self.add_personal_info_to_labels()
            else:
                print("User doesnt exist")
                messagebox.showerror("Error", "User dosent exist in DataBase")
                self.curr_user = ""
                self.full_report_button.config(state="disabled")
                self.improvment_button.config(state="disabled")
                self.multi_report_button.config(state="disabled")
                self.body_weights_button.config(state="disabled")
                self.user_compare_to_avg_button.config(state="disabled")
                self.delete_exercise_button.config(state="disabled")
                self.targets_button.config(state="disabled")
                self.delete_personal_info_from_labels()
        except ValueError:
            messagebox.showerror("Error", "Enter only numbers (ID)")
            self.curr_user = ""
            self.full_report_button.config(state="disabled")
            self.improvment_button.config(state="disabled")
            self.multi_report_button.config(state="disabled")
            self.user_compare_to_avg_button.config(state="disabled")
            self.delete_exercise_button.config(state="disabled")
            self.targets_button.config(state="disabled")

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
        self.curr_user_exercises = list(set(exercises))
        for i in self.curr_user_exercises:
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
            pdf = matplotlib.backends.backend_pdf.PdfPages('SelectedReport.pdf')
            selected_list = self.exercises_list.curselection()
            print(selected_list)
            for i in range(0, len(selected_list)):
                selected = self.exercises_list.get(selected_list[i])
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
                plt.suptitle(selected[::-1], fontsize=20)
                plt.setp(ax.xaxis.get_majorticklabels(), rotation=90, ha="right")
                plt.gcf().subplots_adjust(bottom=0.20)
                for i, v in enumerate(weights_list):
                    ax.text(i, v + 0.02, "%d" % v, ha="center")
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
                plt.show()
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
        colors = ['cornflowerblue', 'indigo']
        axs[1, 1].pie([male, female], labels=labels, autopct=make_autopct([male, female]), shadow=True, startangle=90,
                      colors=colors)
        axs[1, 1].axis('equal')
        temp = "מין"
        axs[1, 1].set_title(temp[::-1])

        curr.execute("SELECT StartDate FROM Users")
        rows = curr.fetchall()
        my_dict = {}
        months = []
        counts = []
        for row in rows:
            month = datetime.strptime(row[0], "%d/%m/%Y").strftime("%b")
            if month not in my_dict:
                my_dict[month] = 1
            else:
                my_dict[month] = my_dict[month] + 1
        for x, y in my_dict.items():
            months.append(x)
            counts.append(y)
        axs[0, 1].pie(counts, labels=months, autopct=make_autopct(counts), shadow=True, startangle=90)
        axs[0, 1].axis('equal')
        temp = "תאריך התחלה"
        axs[0, 1].set_title(temp[::-1])
        curr.execute("SELECT Age FROM Users")
        rows = curr.fetchall()
        my_dict = {}
        ages = []
        counts = []
        for row in rows:
            if row[0] not in my_dict:
                my_dict[row[0]] = 1
            else:
                my_dict[row[0]] = my_dict[ages] + 1
        for x, y in my_dict.items():
            ages.append(x)
            counts.append(y)
        axs[1, 0].pie(counts, labels=ages, autopct=make_autopct(counts), shadow=True, startangle=90)
        axs[1, 0].axis('equal')
        temp = "גיל"
        axs[1, 0].set_title(temp[::-1])
        plt.show()

    def improvment_function(self):

        def autolabel(rects, rects2, xpos='center'):
            ha = {'center': 'center', 'right': 'left', 'left': 'right'}
            offset = {'center': 0, 'right': 1, 'left': -1}
            i = 0
            if rects2 == 0:
                for rect in rects:
                    height = rect.get_height()
                    rect.set_width(0.5)
                    plt.annotate('{}'.format(height),
                                 xy=(rect.get_x() + rect.get_width() / 2, height),
                                 xytext=(offset[xpos] * 3, 3),  # use 3 points offset
                                 textcoords="offset points",  # in both directions
                                 ha=ha[xpos], va='bottom')
            else:
                for rect in rects:
                    height = rect.get_height() + rects2[i].get_height()
                    rect.set_width(0.5)
                    plt.annotate('{}'.format(height),
                                 xy=(rect.get_x() + rect.get_width() / 2, height),
                                 xytext=(offset[xpos] * 3, 3),  # use 3 points offset
                                 textcoords="offset points",  # in both directions
                                 ha=ha[xpos], va='bottom')
                    i += 1

        curr = self.conn.cursor()
        curr.execute("SELECT * FROM Exercises WHERE Id=?", (self.curr_user.id,))
        rows = curr.fetchall()

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
            self.curr_user.my_exercises[name].records_array.sort(
                key=lambda date: datetime.strptime(date.date, "%d/%m/%Y"))
        min_list = []
        max_list = []
        exercises_list_for_min_max = []
        for exercise in self.curr_user.my_exercises:
            temp_weights = self.curr_user.my_exercises[exercise].get_weights()
            min_list.append(min(temp_weights))
            exercises_list_for_min_max.append(self.curr_user.my_exercises[exercise].name[::-1])
            max_list.append(max(temp_weights) - min(temp_weights))
        ind = np.arange(len(min_list))
        width = 0.35
        fig, ax = plt.subplots()
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=90, ha="right")
        plt.gcf().subplots_adjust(bottom=0.20)
        p1 = plt.bar(ind, min_list, width, color="blue")
        p2 = plt.bar(ind, max_list, width, bottom=min_list, color="cornflowerblue")

        plt.ylabel('משקלים'[::-1])
        plt.title('שיפור במשקל לפי תרגיל'[::-1], fontsize=20)
        plt.xticks(ind, exercises_list_for_min_max)
        totalmax = ((max(max_list)) + (max(min_list)))
        plt.yticks(np.arange(0, totalmax + 20, 10))
        plt.legend((p2[0], p1[0]), ('משקל מקסימלי בתרגיל'[::-1], 'משקל מינימלי בתרגיל'[::-1]))
        autolabel(p1, 0)
        autolabel(p2, p1)
        fig.set_size_inches(20, 20)
        if inspect.stack()[
            1].function == "print_full_report_button_function":  ##checking if the function was called from a full report button
            pdf = matplotlib.backends.backend_pdf.PdfPages("OutPuts\\DiagramWeights.pdf")
            pdf.savefig(fig)
            plt.close(fig)
            pdf.close()
        else:
            fig.show()

    def body_weights_function(self):

        cur = self.conn.cursor()
        cur.execute("SELECT Weight,Date FROM BodyWeights WHERE Id=?", (self.curr_user.id,))
        rows = cur.fetchall()
        temp_list = []
        dates_list = []
        weights_list = []
        for row in rows:
            temp_record = Record(row[0], row[1])
            temp_list.append(temp_record)
        temp_list.sort(key=lambda date: datetime.strptime(date.date, "%d/%m/%Y"))
        for record in temp_list:
            weights_list.append(record.weight)
            dates_list.append(record.date)
        fig, ax = plt.subplots()
        plt.plot(dates_list, weights_list, zorder=1, linewidth=1.5, color='royalblue')
        plt.scatter(dates_list, weights_list, s=30,
                    color='royalblue', zorder=4)
        plt.suptitle(" מעקב משקל גוף"[::-1], fontsize=20, weight='bold')
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=90, ha="right")
        plt.gcf().subplots_adjust(bottom=0.20)
        for i, v in enumerate(weights_list):
            ax.text(i, v + 0.05, "%d" % v, ha="center")
        ax.set_ylabel("משקל גוף"[::-1], color='black'
                                              '')
        # ax.set_xlabel("תאריך"[::-1],color='darkblue')
        ax.tick_params(labelcolor='black')
        # ax.set_facecolor('azure')
        ax.set_axisbelow(True)
        ax.grid(color='lightgray', axis='y')

        if inspect.stack()[
            1].function == "print_full_report_button_function":  ##checking if the function was called from a full report button
            pdf = matplotlib.backends.backend_pdf.PdfPages("OutPuts\\BodyWeights.pdf")
            pdf.savefig(fig)
            plt.close(fig)
            pdf.close()
        else:
            fig.show()

    def insert_benchpress_weights(self):
        cur = self.conn.cursor()
        csv_path = tkinter.filedialog.askopenfilename()
        with open(csv_path, 'r', encoding="cp1255") as csv_file:
            csv_reader = csv.reader(csv_file)
            for line in csv_reader:
                if line[5] != "Elite":
                    cur.execute(
                        "INSERT INTO BenchPress(BodyWeight,Beginner,Novice,Intermediate,Advanced,Elite,Gender)VALUES(?,?,?,?,?,?,?)",
                        (line[0], line[1], line[2], line[3], line[4], line[5], line[6],))
                    self.conn.commit()
                if line[5] == "":
                    continue
        csv_file.close()

    def insert_squat_weights(self):
        cur = self.conn.cursor()
        csv_path = tkinter.filedialog.askopenfilename()
        with open(csv_path, 'r', encoding="cp1255") as csv_file:
            csv_reader = csv.reader(csv_file)
            for line in csv_reader:
                if line[5] != "Elite":
                    cur.execute(
                        "INSERT INTO Squat(BodyWeight,Beginner,Novice,Intermediate,Advanced,Elite,Gender)VALUES(?,?,?,?,?,?,?)",
                        (line[0], line[1], line[2], line[3], line[4], line[5], line[6],))
                    self.conn.commit()
                if line[5] == "":
                    continue
        csv_file.close()

    def insert_deadlift_weights(self):
        cur = self.conn.cursor()
        csv_path = tkinter.filedialog.askopenfilename()
        with open(csv_path, 'r', encoding="cp1255") as csv_file:
            csv_reader = csv.reader(csv_file)
            for line in csv_reader:
                if line[5] != "Elite":
                    cur.execute(
                        "INSERT INTO DeadLift(BodyWeight,Beginner,Novice,Intermediate,Advanced,Elite,Gender)VALUES(?,?,?,?,?,?,?)",
                        (line[0], line[1], line[2], line[3], line[4], line[5], line[6],))
                    self.conn.commit()
                if line[5] == "":
                    continue
        csv_file.close()

    def insert_headpress_weights(self):
        cur = self.conn.cursor()
        csv_path = tkinter.filedialog.askopenfilename()
        with open(csv_path, 'r', encoding="cp1255") as csv_file:
            csv_reader = csv.reader(csv_file)
            for line in csv_reader:
                if line[5] != "Elite":
                    cur.execute(
                        "INSERT INTO HeadPress(BodyWeight,Beginner,Novice,Intermediate,Advanced,Elite,Gender)VALUES(?,?,?,?,?,?,?)",
                        (line[0], line[1], line[2], line[3], line[4], line[5], line[6],))
                    self.conn.commit()
                if line[5] == "":
                    continue
        csv_file.close()

    def user_compare_to_avg_function(self):
        weight_to_compare = int(self.curr_user.current_weight) - (int(self.curr_user.current_weight) % 5)
        curr = self.conn.cursor()
        if weight_to_compare < 40 and self.curr_user.gender == "נקבה":
            RAISED("ERROR female weight cant be less than 40")
        if weight_to_compare < 50 and self.curr_user.gender == "זכר":
            RAISED("ERROR MALE weight cant be less than 50")
        # BENCHPRESS
        curr.execute("SELECT * FROM BenchPress WHERE BodyWeight=? AND Gender=?",
                     (weight_to_compare, self.curr_user.gender,))
        rows = curr.fetchall()
        fig, axs = plt.subplots(2, 2, figsize=(16, 9))
        if rows:
            temp_list = []
            title_list = []
            weights_list = []
            for row in rows:
                temp_record = Record(row[1], "מתחיל")
                temp_list.append(temp_record)
                temp_record = Record(row[2], "בינוני")
                temp_list.append(temp_record)
                temp_record = Record(row[3], "מתקדם")
                temp_list.append(temp_record)
                temp_record = Record(row[4], "מתקדם מאוד")
                temp_list.append(temp_record)
                temp_record = Record(row[5], "תחרותי")
                temp_list.append(temp_record)

            curr.execute("SELECT Weight FROM Exercises WHERE Id=? AND ExerciseName=?",
                         (self.curr_user.id, "בנץ פרס רמ1",))
            rows = curr.fetchall()
            if rows:
                max_weight = max(rows)
                temp_record = Record(max_weight[0], "אני")
                temp_list.append(temp_record)
                temp_list.sort(key=lambda Record: Record.weight)
                for line in temp_list:
                    title_list.append(line.date[::-1])
                    weights_list.append(line.weight)
                axs[0, 0].plot(title_list, weights_list, zorder=1, linewidth=1.5, color='royalblue')
                axs[0, 0].scatter(title_list, weights_list, s=30, color='royalblue', zorder=2)
                axs[0, 0].scatter("ינא", max_weight[0], s=40, color='red', zorder=3)
                axs[0, 0].set_title(str(weight_to_compare) + "משקל בנץ פרס רמ1 מול משקל גוף ממוצע-"[::-1], fontsize=20,
                                    weight='bold')
                axs[0, 0].set(ylabel='משקל בנץ פרס'[::-1])
                axs[0, 0].tick_params(labelcolor='black')
                axs[0, 0].set_axisbelow(True)
                axs[0, 0].grid(color='lightgray', axis='y')
                for i, v in enumerate(weights_list):
                    axs[0, 0].text(i, v + 4, "%d" % v, ha="center")
                axs[0, 0].set_yticks(np.arange(0, max(weights_list) + 30, 15))
            else:
                curr.execute("SELECT Weight FROM Exercises WHERE Id=? AND ExerciseName=?",
                             (self.curr_user.id, "בנץ פרס",))
                rows = curr.fetchall()
                if rows:
                    max_weight = max(rows)
                    temp_list2 = []
                    for i in range(0, len(temp_list)):
                        temp_record = temp_list.pop()
                        temp_record.weight = temp_record.weight * 0.84
                        temp_list2.append(temp_record)

                    temp_record = Record(max_weight[0], "אני")
                    temp_list2.append(temp_record)
                    temp_list2.sort(key=lambda Record: Record.weight)
                    for line in temp_list2:
                        title_list.append(line.date[::-1])
                        weights_list.append(line.weight)
                    axs[0, 0].plot(title_list, weights_list, zorder=1, linewidth=1.5, color='royalblue')
                    axs[0, 0].scatter(title_list, weights_list, s=30, color='royalblue', zorder=2)
                    axs[0, 0].scatter("ינא", max_weight[0], s=40, color='red', zorder=3)
                    axs[0, 0].set_title(str(weight_to_compare) + "משקל בנץ פרס רמ5 מול משקל גוף ממוצע-"[::-1],
                                        fontsize=20, weight='bold')
                    axs[0, 0].set(ylabel='משקל בנץ פרס'[::-1])
                    for i, v in enumerate(weights_list):
                        axs[0, 0].text(i, v + 4, "%d" % v, ha="center")
                    axs[0, 0].set_yticks(np.arange(0, max(weights_list) + 30, 15))
                    axs[0, 0].tick_params(labelcolor='black')
                    axs[0, 0].set_axisbelow(True)
                    axs[0, 0].grid(color='lightgray', axis='y')
                else:
                    axs[0, 0].text(0.5, 0.5, 'אינך עושה בנץ פרס כרגע'[::-1], horizontalalignment='center',
                                   verticalalignment='center', bbox=dict(facecolor='red', alpha=0.5))

        # SQUAT
        curr.execute("SELECT * FROM Squat WHERE BodyWeight=? AND Gender=?", (weight_to_compare, self.curr_user.gender,))
        rows = curr.fetchall()
        if rows:
            temp_list = []
            title_list = []
            weights_list = []
            for row in rows:
                temp_record = Record(row[1], "מתחיל")
                temp_list.append(temp_record)
                temp_record = Record(row[2], "בינוני")
                temp_list.append(temp_record)
                temp_record = Record(row[3], "מתקדם")
                temp_list.append(temp_record)
                temp_record = Record(row[4], "מתקדם מאוד")
                temp_list.append(temp_record)
                temp_record = Record(row[5], "תחרותי")
                temp_list.append(temp_record)

            curr.execute("SELECT Weight FROM Exercises WHERE Id=? AND ExerciseName=?",
                         (self.curr_user.id, "סקוואט רמ1",))
            rows = curr.fetchall()
            if rows:

                max_weight = max(rows)
                temp_record = Record(max_weight[0], "אני")
                temp_list.append(temp_record)
                temp_list.sort(key=lambda Record: Record.weight)
                for line in temp_list:
                    title_list.append(line.date[::-1])
                    weights_list.append(line.weight)
                axs[0, 1].plot(title_list, weights_list, zorder=1, linewidth=1.5, color='royalblue')
                axs[0, 1].scatter(title_list, weights_list, s=30, color='royalblue', zorder=2)
                axs[0, 1].scatter("ינא", max_weight[0], s=40, color='red', zorder=3)
                axs[0, 1].set_title(str(weight_to_compare) + "משקל סקוואט רמ1 מול משקל גוף ממוצע-"[::-1], fontsize=20,
                                    weight='bold')
                axs[0, 1].set(ylabel='משקל סקוואט'[::-1])
                for i, v in enumerate(weights_list):
                    axs[0, 1].text(i, v + 4, "%d" % v, ha="center")
                axs[0, 1].set_yticks(np.arange(0, max(weights_list) + 30, 15))
                axs[0, 1].tick_params(labelcolor='black')
                axs[0, 1].set_axisbelow(True)
                axs[0, 1].grid(color='lightgray', axis='y')
            else:
                curr.execute("SELECT Weight FROM Exercises WHERE Id=? AND ExerciseName=?",
                             (self.curr_user.id, "סקוואט",))
                rows = curr.fetchall()
                if rows:
                    max_weight = max(rows)
                    temp_list2 = []
                    for i in range(0, len(temp_list)):
                        temp_record = temp_list.pop()
                        temp_record.weight = temp_record.weight * 0.84
                        temp_list2.append(temp_record)
                    temp_record = Record(max_weight[0], "אני")
                    temp_list2.append(temp_record)
                    temp_list2.sort(key=lambda Record: Record.weight)
                    for line in temp_list2:
                        title_list.append(line.date[::-1])
                        weights_list.append(line.weight)
                    axs[0, 1].plot(title_list, weights_list, zorder=1, linewidth=1.5, color='royalblue')
                    axs[0, 1].scatter(title_list, weights_list, s=30, color='royalblue', zorder=2)
                    axs[0, 1].scatter("ינא", max_weight[0], s=40, color='red', zorder=3)
                    axs[0, 1].set_title(str(weight_to_compare) + "משקל סקוואט 5רמ מול משקל גוף ממוצע-"[::-1],
                                        fontsize=20, weight='bold')
                    axs[0, 1].set(ylabel='משקל סקוואט'[::-1])
                    for i, v in enumerate(weights_list):
                        axs[0, 1].text(i, v + 4, "%d" % v, ha="center")
                    axs[0, 1].set_yticks(np.arange(0, max(weights_list) + 30, 15))
                    axs[0, 1].tick_params(labelcolor='black')
                    axs[0, 1].set_axisbelow(True)
                    axs[0, 1].grid(color='lightgray', axis='y')
                else:
                    axs[0, 1].text(0.5, 0.5, 'אינך עושה סקוואט כרגע'[::-1], horizontalalignment='center',
                                   verticalalignment='center', bbox=dict(facecolor='red', alpha=0.5))

        # DEADLIFT
        curr.execute("SELECT * FROM DeadLift WHERE BodyWeight=? AND Gender=?",
                     (weight_to_compare, self.curr_user.gender,))
        rows = curr.fetchall()
        if rows:
            temp_list = []
            title_list = []
            weights_list = []

            for row in rows:
                temp_record = Record(row[1], "מתחיל")
                temp_list.append(temp_record)
                temp_record = Record(row[2], "בינוני")
                temp_list.append(temp_record)
                temp_record = Record(row[3], "מתקדם")
                temp_list.append(temp_record)
                temp_record = Record(row[4], "מתקדם מאוד")
                temp_list.append(temp_record)
                temp_record = Record(row[5], "תחרותי")
                temp_list.append(temp_record)
            curr.execute("SELECT Weight FROM Exercises WHERE Id=? AND ExerciseName=?",
                         (self.curr_user.id, "דדליפט רמ1",))
            rows = curr.fetchall()
            if rows:
                max_weight = max(rows)
                temp_record = Record(max_weight[0], "אני")
                temp_list.append(temp_record)
                temp_list.sort(key=lambda Record: Record.weight)
                for line in temp_list:
                    title_list.append(line.date[::-1])
                    weights_list.append(line.weight)
                axs[1, 1].plot(title_list, weights_list, zorder=1, linewidth=1.5, color='royalblue')
                axs[1, 1].scatter(title_list, weights_list, s=30, color='royalblue', zorder=2)
                axs[1, 1].scatter("ינא", max_weight[0], s=40, color='red', zorder=3)
                axs[1, 1].set_title(str(weight_to_compare) + "משקל דדליפט רמ1 מול משקל גוף ממוצע-"[::-1], fontsize=20,
                                    weight='bold')
                axs[1, 1].set(ylabel='משקל דדליפט'[::-1])

                for i, v in enumerate(weights_list):
                    axs[1, 1].text(i, v + 4, "%d" % v, ha="center")
                axs[1, 1].set_yticks(np.arange(0, max(weights_list) + 30, 15))
                axs[1, 1].tick_params(labelcolor='black')
                axs[1, 1].set_axisbelow(True)
                axs[1, 1].grid(color='lightgray', axis='y')
            else:
                curr.execute("SELECT Weight FROM Exercises WHERE Id=? AND ExerciseName=?",
                             (self.curr_user.id, "דדליפט",))
                rows = curr.fetchall()
                if rows:
                    max_weight = max(rows)
                    temp_list2 = []
                    for i in range(0, len(temp_list)):
                        temp_record = temp_list.pop()
                        temp_record.weight = temp_record.weight * 0.84
                        temp_list2.append(temp_record)

                    temp_record = Record(max_weight[0], "אני")
                    temp_list2.append(temp_record)
                    temp_list2.sort(key=lambda Record: Record.weight)
                    for line in temp_list2:
                        title_list.append(line.date[::-1])
                        weights_list.append(line.weight)
                    axs[1, 1].plot(title_list, weights_list, zorder=1, linewidth=1.5, color='royalblue')
                    axs[1, 1].scatter(title_list, weights_list, s=30, color='royalblue', zorder=2)
                    axs[1, 1].scatter("ינא", max_weight[0], s=40, color='red', zorder=3)
                    axs[1, 1].set_title(str(weight_to_compare) + "משקל דדליפט רמ5 מול משקל גוף ממוצע-"[::-1],
                                        fontsize=20, weight='bold')
                    axs[1, 1].set(ylabel='משקל דדליפט'[::-1])
                    for i, v in enumerate(weights_list):
                        axs[1, 1].text(i, v + 4, "%d" % v, ha="center")
                    axs[1, 1].set_yticks(np.arange(0, max(weights_list) + 30, 15))
                    axs[1, 1].tick_params(labelcolor='black')
                    axs[1, 1].set_axisbelow(True)
                    axs[1, 1].grid(color='lightgray', axis='y')
                else:
                    axs[1, 1].text(0.5, 0.5, 'אינך עושה דדליפט כרגע'[::-1], horizontalalignment='center',
                                   verticalalignment='center', bbox=dict(facecolor='red', alpha=0.5))

        # HEADPRESS
        curr.execute("SELECT * FROM HeadPress WHERE BodyWeight=? AND Gender=?",
                     (weight_to_compare, self.curr_user.gender,))
        rows = curr.fetchall()
        if rows:
            temp_list = []
            title_list = []
            weights_list = []

            for row in rows:
                temp_record = Record(row[1], "מתחיל")
                temp_list.append(temp_record)
                temp_record = Record(row[2], "בינוני")
                temp_list.append(temp_record)
                temp_record = Record(row[3], "מתקדם")
                temp_list.append(temp_record)
                temp_record = Record(row[4], "מתקדם מאוד")
                temp_list.append(temp_record)
                temp_record = Record(row[5], "תחרותי")
                temp_list.append(temp_record)
            curr.execute("SELECT Weight FROM Exercises WHERE Id=? AND ExerciseName=?",
                         (self.curr_user.id, "הד פרס רמ1",))
            rows = curr.fetchall()
            if rows:
                max_weight = max(rows)
                temp_record = Record(max_weight[0], "אני")
                temp_list.append(temp_record)
                temp_list.sort(key=lambda Record: Record.weight)
                for line in temp_list:
                    title_list.append(line.date[::-1])
                    weights_list.append(line.weight)
                axs[1, 0].plot(title_list, weights_list, zorder=1, linewidth=1.5, color='royalblue')
                axs[1, 0].scatter(title_list, weights_list, s=30, color='royalblue', zorder=2)
                axs[1, 0].scatter("ינא", max_weight[0], s=40, color='red', zorder=3)
                axs[1, 0].set_title(str(weight_to_compare) + "משקל הד פרס מול משקל גוף ממוצע-"[::-1], fontsize=20,
                                    weight='bold')
                axs[1, 0].set(ylabel='משקל הד פרס'[::-1])
                for i, v in enumerate(weights_list):
                    axs[1, 0].text(i, v + 4, "%d" % v, ha="center")
                axs[1, 0].set_yticks(np.arange(0, max(weights_list) + 30, 15))
                axs[1, 0].tick_params(labelcolor='black')
                axs[1, 0].set_axisbelow(True)
                axs[1, 0].grid(color='lightgray', axis='y')
            else:
                curr.execute("SELECT Weight FROM Exercises WHERE Id=? AND ExerciseName=?",
                             (self.curr_user.id, "הד פרס",))
                rows = curr.fetchall()
                if rows:
                    max_weight = max(rows)
                    temp_list2 = []
                    for i in range(0, len(temp_list)):
                        temp_record = temp_list.pop()
                        temp_record.weight = temp_record.weight * 0.84
                        temp_list2.append(temp_record)
                    temp_record = Record(max_weight[0], "אני")
                    temp_list2.append(temp_record)
                    temp_list2.sort(key=lambda Record: Record.weight)
                    for line in temp_list2:
                        title_list.append(line.date[::-1])
                        weights_list.append(line.weight)
                    axs[1, 0].plot(title_list, weights_list, zorder=1, linewidth=1.5, color='royalblue')
                    axs[1, 0].scatter(title_list, weights_list, s=30, color='royalblue', zorder=2)
                    axs[1, 0].scatter("ינא", max_weight[0], s=40, color='red', zorder=3)
                    axs[1, 0].set_title(str(weight_to_compare) + "משקל הד פרס מול משקל גוף ממוצע-"[::-1], fontsize=20,
                                        weight='bold')
                    axs[1, 0].set(ylabel='משקל הד פרס'[::-1])
                    for i, v in enumerate(weights_list):
                        axs[1, 0].text(i, v + 4, "%d" % v, ha="center")
                    axs[1, 0].set_yticks(np.arange(0, max(weights_list) + 30, 15))
                    axs[1, 0].tick_params(labelcolor='black')
                    axs[1, 0].set_axisbelow(True)
                    axs[1, 0].grid(color='lightgray', axis='y')
                else:
                    axs[1, 0].text(0.5, 0.5, 'אינך עושה הד פרס כרגע'[::-1], horizontalalignment='center',
                                   verticalalignment='center', bbox=dict(facecolor='red', alpha=0.5))

        if inspect.stack()[
            1].function == "print_full_report_button_function":  ##checking if the function was called from a full report button
            pdf = matplotlib.backends.backend_pdf.PdfPages("OutPuts\\CompareMySelf.pdf")
            pdf.savefig(fig)
            plt.close(fig)
            pdf.close()
        else:
            fig.show()

    def delete_exercise_popup(self):
        if self.exercises_list.curselection():
            print(len(self.exercises_list.curselection()))
            print(self.exercises_list.size())
            if self.exercises_list.size() != 1:
                if self.exercises_list.size() != len(self.exercises_list.curselection()):
                    self.popup = Tk()
                    frame1 = Frame(self.popup, highlightbackground="RED", highlightcolor="RED", highlightthickness=1,
                                   bd=0)
                    frame1.pack()
                    self.popup.overrideredirect(1)
                    self.popup.geometry("300x75+650+400")
                    lbl = Label(frame1, text="אתה בטוח שאתה רוצה למחוק את התרגילים ?")
                    lbl.pack()
                    yes_btn = Button(frame1, text="Yes", bg="light blue", fg="red",
                                     command=self.delete_exercise_function, width=10)
                    yes_btn.pack(padx=30, pady=10, side=LEFT)
                    no_btn = Button(frame1, text="No", bg="light blue", fg="red", command=self.popup.destroy, width=10)
                    no_btn.pack(padx=10, pady=10, side=LEFT)
                    self.popup.mainloop()
                else:
                    messagebox.showerror("Error", "אי אפשר למחוק את כל התרגילים חייב שישאר אחד במינימום")
            else:
                messagebox.showerror("Error",
                                     "אי אפשר להשאיר משתמש בלי תרגילים תוסיפו תרגיל ואחר כך תמחקו את התרגיל הזה")

    def delete_exercise_function(self):

        selected_list = self.exercises_list.curselection()
        curr = self.conn.cursor()
        for i in range(0, len(selected_list)):
            selected = self.exercises_list.get(selected_list[i])
            curr.execute("DELETE FROM Exercises WHERE Id=? AND ExerciseName=? ",
                         (self.curr_user.id, selected,))
            self.conn.commit()
        self.search_user_button_function()
        self.popup.destroy()

    def create_calendar_function(self):
        current_year = datetime.now().year
        current_month = datetime.now().month
        months_to_add_0 = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        cal = MplCalendar(current_year, 8)
        curr = self.conn.cursor()
        curr.execute("SELECT DISTINCT(Date) FROM Exercises WHERE Id=?", (self.curr_user.id,))
        rows = curr.fetchall()
        for row in rows:
            if current_month in months_to_add_0:
                if datetime.strptime(row[0], '%d/%m/%Y').strftime('%m') == "0" + str(8):
                    if datetime.strptime(row[0], '%d/%m/%Y').strftime('%Y') == str(current_year):
                        day = datetime.strptime(row[0], '%d/%m/%Y').strftime('%d')
                        if day.startswith("0"):
                            day = day[1::]
                        cal.add_event(day, "'")
            else:
                if datetime.strptime(row[0], '%d/%m/%Y').strftime('%m') == str(current_month):
                    if datetime.strptime(row[0], '%d/%m/%Y').strftime('%Y') == str(current_year):
                        day = datetime.strptime(row[0], '%d/%m/%Y').strftime('%d')
                        if day.startswith("0"):
                            day = day[1::]
                        cal.add_event(day, "'")
        cal.show()

    def open_targets_frame(self):  # todo add open target limit to 9

        def add_target():

            def add_target_to_db():
                try:
                    input_from_weight_target = int(self.weight_target_field.get())
                    # print(input_from_weight_target)
                    input_from_description = self.description_text.get("1.0", "end-1c")
                    # print(input_from_description)
                    categories = self.categorize_menu.get()
                    # print(categories)
                    input_from_start_date = self.starting_date_field.get()
                    # print(input_from_start_date)
                    exercise_name = self.exercises_menu.get()
                    # print(exercise_name)
                    input_from_title = str(self.title_field.get())
                    # print(input_from_title)
                    curr = self.conn.cursor()
                    curr.execute(
                        "INSERT INTO Targets(Id,Title,WeightTarget,ExerciseName,Description,Status,StartingDate,FinishedDate,Categorize)VALUES(?,?,?,?,?,?,?,?,?)",
                        (self.curr_user.id, input_from_title, input_from_weight_target, exercise_name,
                         input_from_description, "לא הושלמה", input_from_start_date, " ", categories,))
                    self.conn.commit()
                    curr = self.conn.cursor()
                    curr.execute("SELECT * FROM Targets WHERE Id=?", (self.curr_user.id,))
                    rows = curr.fetchall()
                    targets_list.delete('0', 'end')
                    for row in rows:
                        targets_list.insert(END, row[1])

                except ValueError:
                    messagebox.showerror("Error", "נא להכניס רק מספרים בשדה (משקל מטרה)")

            self.add_targets_tk = Tk()
            self.frame_add_target = Frame(self.add_targets_tk)
            self.frame_add_target.grid()
            # self.add_targets_tk.geometry("350x300+650+400")
            len_max = 0
            for m in self.curr_user_exercises:
                if len(m) > len_max:
                    len_max = len(m)
            self.explain_label = Label(self.frame_add_target, text="!הוספת מטרה חדשה ", font="Helvetica 12 underline")
            self.explain_label.grid(column=1, row=0)
            self.weight_target = StringVar()
            self.weight_target_field = Entry(self.frame_add_target, textvariable=self.weight_target, width=15)
            self.weight_target_label = Label(self.frame_add_target, text="משקל מטרה")
            self.weight_target_field.grid(column=1, row=4)
            self.weight_target_label.grid(column=1, row=3)
            self.description_text = Text(self.frame_add_target, width=len_max, height=4)
            self.description_text.grid(column=1, row=6)
            self.description_label = Label(self.frame_add_target, text="תיאור המטרה")
            self.description_label.grid(column=1, row=5)

            self.title_var = StringVar()
            self.title_field = Entry(self.frame_add_target, textvariable=self.title_var, width=15)
            self.title_label = Label(self.frame_add_target, text="כותרת מטרה")
            self.title_label.grid(column=1, row=1)
            self.title_field.grid(column=1, row=2)

            options = ["משקל בתרגיל", "משקל גוף", "מספר אימונים החודש"]
            self.categorize_menu = ttk.Combobox(self.frame_add_target, values=options)
            self.categorize_menu.grid(column=1, row=8)
            self.categorize_label = Label(self.frame_add_target, text="קטגורית מטרה")
            self.categorize_label.grid(column=1, row=7)
            self.exercise_label = Label(self.frame_add_target, text="בחירת תרגיל")
            self.exercise_label.grid(column=1, row=9)

            self.exercises_menu = ttk.Combobox(self.frame_add_target, values=self.curr_user_exercises, width=len_max)
            self.exercises_menu.grid(column=1, row=8)
            today = datetime.today()
            current_date = today.strftime("%d/%m/%Y")
            self.starting_date = StringVar()
            self.starting_date_field = Entry(self.frame_add_target, textvariable=self.starting_date, width=15)
            self.starting_date_field.insert(0, current_date)
            self.starting_date_label = Label(self.frame_add_target, text="תאריך התחלה")
            self.starting_date_label.grid(column=1, row=11)
            self.starting_date_field.grid(column=1, row=12)

            self.approve_button = Button(self.frame_add_target, text="אישור", command=add_target_to_db)
            self.cancel_button = Button(self.frame_add_target, text="ביטול", command=self.add_targets_tk.destroy)
            self.approve_button.grid(column=0, row=12)
            self.cancel_button.grid(column=2, row=12)

        def onselect(evt):
            # Note here that Tkinter passes an event object to onselect()
            w = evt.widget
            # index = w.curselection()[0]
            # value = w.get(index)
            # print('You selected item %d: "%s"' % (index, value))
            # print(w.get(ANCHOR))

            curr.execute("SELECT * FROM Targets WHERE Id=? AND Title=?", (self.curr_user.id, w.get(ANCHOR),))
            rows = curr.fetchall()
            # print(rows)

            temp = rows[0][1]
            temp = str(temp)
            title_label.config(text="כותרת מטרה: " + temp)

            temp = rows[0][2]
            temp = str(temp)
            weight_target_label.config(text="משקל מטרה: " + temp)

            temp = rows[0][3]
            temp = str(temp)
            exercise_name_label.config(text="שם תרגיל: " + temp)

            temp = rows[0][4]
            temp = str(temp)
            description_label.config(text="תיאור מטרה: " + temp)

            temp = rows[0][5]
            temp = str(temp)
            status_label.config(text="סטטוס מטרה: " + temp)

            temp = rows[0][6]
            temp = str(temp)
            state_date_label.config(text="תאריך התחלה: " + temp)

            temp = rows[0][7]
            temp = str(temp)
            finish_date_label.config(text="תאריך סיום: " + temp)

        def delete_target_from_db():
            curr.execute("DELETE FROM Targets WHERE Id=? AND Title=? ",
                         (self.curr_user.id, targets_list.get(ANCHOR),))
            self.conn.commit()
            self.popup.destroy()
            curr.execute("SELECT * FROM Targets WHERE Id=?", (self.curr_user.id,))
            rows = curr.fetchall()
            targets_list.delete('0', 'end')
            for row in rows:
                targets_list.insert(END, row[1])

        def delete_target():
            selected = targets_list.get(ANCHOR)
            if selected:
                self.popup = Tk()
                frame1 = Frame(self.popup, highlightbackground="RED", highlightcolor="RED", highlightthickness=1,
                               bd=0)
                frame1.pack()
                self.popup.overrideredirect(1)
                self.popup.geometry("300x75+650+400")
                lbl = Label(frame1, text="אתה בטוח שאתה את המטרה ?")
                lbl.pack()
                yes_btn = Button(frame1, text="Yes", bg="light blue", fg="red",
                                 command=delete_target_from_db, width=10)
                yes_btn.pack(padx=30, pady=10, side=LEFT)
                no_btn = Button(frame1, text="No", bg="light blue", fg="red", command=self.popup.destroy, width=10)
                no_btn.pack(padx=10, pady=10, side=LEFT)
                self.popup.mainloop()

        def edit_target():

            def edit_target_to_db():
                try:
                    input_from_weight_target = int(self.weight_target_field.get())
                    # print(input_from_weight_target)
                    input_from_description = self.description_text.get("1.0", "end-1c")
                    # print(input_from_description)
                    categories = self.categorize_menu.get()
                    # print(categories)
                    input_from_start_date = self.starting_date_field.get()
                    # print(input_from_start_date)
                    exercise_name = self.exercises_menu.get()
                    # print(exercise_name)
                    input_from_title = str(self.title_field.get())
                    # print(input_from_title)
                    selected_title = targets_list.get(ANCHOR)
                    curr = self.conn.cursor()
                    curr.execute(
                        '''UPDATE Targets SET Title=?,WeightTarget=?,ExerciseName=?,Description=?,StartingDate=?
                         WHERE Id=? AND Title=? ''',
                        (input_from_title, input_from_weight_target, exercise_name, input_from_description,
                         input_from_start_date, self.curr_user.id, selected_title,))
                    self.conn.commit()
                    curr = self.conn.cursor()
                    curr.execute("SELECT * FROM Targets WHERE Id=?", (self.curr_user.id,))
                    rows = curr.fetchall()
                    targets_list.delete('0', 'end')
                    for row in rows:
                        targets_list.insert(END, row[1])
                    self.edit_targets_tk.destroy()

                except ValueError:
                    messagebox.showerror("Error", "נא להכניס רק מספרים בשדה (משקל מטרה)")

            self.edit_targets_tk = Tk()
            self.frame_edit_target = Frame(self.edit_targets_tk)
            self.frame_edit_target.grid()
            # self.add_targets_tk.geometry("350x300+650+400")
            len_max = 0
            for m in self.curr_user_exercises:
                if len(m) > len_max:
                    len_max = len(m)
            self.explain_label = Label(self.frame_edit_target, text="!עריכת מטרה קיימת ", font="Helvetica 12 underline")
            self.explain_label.grid(column=1, row=0)
            self.weight_target = StringVar()
            self.weight_target_field = Entry(self.frame_edit_target, textvariable=self.weight_target, width=15)
            self.weight_target_label = Label(self.frame_edit_target, text="משקל מטרה")
            self.weight_target_field.grid(column=1, row=4)
            self.weight_target_label.grid(column=1, row=3)
            self.description_text = Text(self.frame_edit_target, width=len_max, height=4)
            self.description_text.grid(column=1, row=6)
            self.description_label = Label(self.frame_edit_target, text="תיאור המטרה")
            self.description_label.grid(column=1, row=5)

            self.title_var = StringVar()
            self.title_field = Entry(self.frame_edit_target, textvariable=self.title_var, width=15)
            self.title_label = Label(self.frame_edit_target, text="כותרת מטרה")
            self.title_label.grid(column=1, row=1)
            self.title_field.grid(column=1, row=2)

            options = ["משקל בתרגיל", "משקל גוף", "מספר אימונים החודש"]
            self.categorize_menu = ttk.Combobox(self.frame_edit_target, values=options)
            self.categorize_menu.grid(column=1, row=8)
            self.categorize_label = Label(self.frame_edit_target, text="קטגורית מטרה")
            self.categorize_label.grid(column=1, row=7)
            self.exercise_label = Label(self.frame_edit_target, text="בחירת תרגיל")
            self.exercise_label.grid(column=1, row=9)

            self.exercises_menu = ttk.Combobox(self.frame_edit_target, values=self.curr_user_exercises, width=len_max)
            self.exercises_menu.grid(column=1, row=8)
            today = datetime.today()
            current_date = today.strftime("%d/%m/%Y")
            self.starting_date = StringVar()
            self.starting_date_field = Entry(self.frame_edit_target, textvariable=self.starting_date, width=15)
            self.starting_date_field.insert(0, current_date)
            self.starting_date_label = Label(self.frame_edit_target, text="תאריך התחלה")
            self.starting_date_label.grid(column=1, row=11)
            self.starting_date_field.grid(column=1, row=12)

            self.approve_button = Button(self.frame_edit_target, text="אישור", command=edit_target_to_db)
            self.cancel_button = Button(self.frame_edit_target, text="ביטול", command=self.edit_targets_tk.destroy)
            self.approve_button.grid(column=0, row=12)
            self.cancel_button.grid(column=2, row=12)

        curr = self.conn.cursor()
        self.targets = Tk()
        self.frame_targets = Frame(self.targets)
        self.frame_targets.grid()
        # self.targets.geometry("300x300+650+400") #todo change the geometry to fit to center
        add_target_button = Button(self.frame_targets, text="הוספת מטרה", command=add_target)
        add_target_button.grid(row=0, column=1)
        edit_target_button = Button(self.frame_targets, text="עריכת מטרה", command=edit_target)
        edit_target_button.grid(row=0, column=2)
        delete_target_button = Button(self.frame_targets, text="מחיקת מטרה", command=delete_target)
        delete_target_button.grid(row=0, column=3)

        title_label = Label(self.frame_targets, text=":כותרת מטרה ")
        weight_target_label = Label(self.frame_targets, text=":משקל מטרה ")
        exercise_name_label = Label(self.frame_targets, text=':שם תרגיל ')
        description_label = Label(self.frame_targets, text=':תיאור מטרה ')
        status_label = Label(self.frame_targets, text=':סטטוס מטרה ')
        state_date_label = Label(self.frame_targets, text=':תאריך התחלה ')
        finish_date_label = Label(self.frame_targets, text=' :תאריך סיום ')
        title_label.grid(row=2, column=5)
        weight_target_label.grid(row=3, column=5)
        exercise_name_label.grid(row=4, column=5)
        description_label.grid(row=5, column=5)
        status_label.grid(row=6, column=5)
        state_date_label.grid(row=7, column=5)
        finish_date_label.grid(row=8, column=5)

        ##### handiling targets list
        targets = []
        targets_list = Listbox(self.frame_targets, listvariable=targets, height=15, name='lb')
        targets_list.grid(row=2, column=0, rowspan=6, sticky=(W, S, N, E))
        targets_label = Label(self.frame_targets, text="רשימת מטרות ", font="Helvetica 12 underline")
        targets_label.grid(row=1, column=0, sticky=(W, S))
        targets_list.bind('<<ListboxSelect>>', onselect)

        curr.execute("SELECT * FROM Targets WHERE Id=?", (self.curr_user.id,))
        rows = curr.fetchall()
        # print(rows)
        for row in rows:
            targets_list.insert(END, row[1])

        self.targets.mainloop()
