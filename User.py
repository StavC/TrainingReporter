import matplotlib.pyplot as plt
import csv
import tkinter.filedialog
import matplotlib.backends.backend_pdf
from DataBase import *
from matplotlib.gridspec import GridSpec

import base64
from io import BytesIO



class User(object):

    def __init__(self, id, first_name, last_name, gender, height, weight,age,start_date,current_weight):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.height = height
        self.weight = weight
        self.gender = gender
        self.age=age
        self.start_date=start_date
        self.current_weight=current_weight
        self.my_exercises = defaultdict(ExerciseArray)

    def plot_exercise(self):
        pdf = matplotlib.backends.backend_pdf.PdfPages("OutPuts\\FullExercisesReport.pdf")

        for exercise in self.my_exercises:

            fig, ax = plt.subplots()

            plt.plot(self.my_exercises[exercise].get_dates(), self.my_exercises[exercise].get_weights(), zorder=1,linewidth=1.5,color='royalblue')
            plt.scatter(self.my_exercises[exercise].get_dates(), self.my_exercises[exercise].get_weights(), s=30,
                        color='royalblue', zorder=4)
            plt.suptitle(exercise[::-1],fontsize=20,weight='bold')

            plt.setp(ax.xaxis.get_majorticklabels(), rotation=90, ha="right")
            plt.gcf().subplots_adjust(bottom=0.20)
            for i, v in enumerate(self.my_exercises[exercise].get_weights()):
                ax.text(i, v +0.05, "%d" % v, ha="center")


            if self.my_exercises[exercise].length() > 100:
                fig.set_size_inches(100, 100)

            elif self.my_exercises[exercise].length() > 90:
                fig.set_size_inches(90, 90)

            elif self.my_exercises[exercise].length() > 80:
                fig.set_size_inches(80, 80)

            elif self.my_exercises[exercise].length() > 70:
                fig.set_size_inches(70, 70)

            elif self.my_exercises[exercise].length() > 60:
                fig.set_size_inches(60, 60)

            elif self.my_exercises[exercise].length() > 50:
                fig.set_size_inches(50, 50)

            elif self.my_exercises[exercise].length() > 40:
                fig.set_size_inches(40, 40)

            elif self.my_exercises[exercise].length() > 30:
                fig.set_size_inches(30, 30)

            elif self.my_exercises[exercise].length() > 20:
                fig.set_size_inches(20, 20)
            #fig.show()
            ax.set_ylabel("משקל עבודה"[::-1],color='black'
                                                   '')
            #ax.set_facecolor('azure')

            #ax.set_xlabel("תאריך"[::-1],color='darkblue')
            ax.tick_params(labelcolor='black')
            ax.set_axisbelow(True)
            ax.grid(color='lightgray',axis='y')

            pdf.savefig(fig)
            plt.close(fig)




        pdf.close()

    def read_csv_create_or_load_user(self=0):
        csv_path = tkinter.filedialog.askopenfilename()
        with open(csv_path, 'r', encoding="cp1255") as csv_file:
            csv_reader = csv.reader(csv_file)
            need_to_create = True
            for line in csv_reader:
                if need_to_create and line[12] != "תז":
                    curr_user = User(line[12], line[10], line[11], line[13], line[15], line[14],line[16],line[17],line[18])
                    need_to_create = False
                if not need_to_create:
                    conn = create_connection("D:\SQLlite\\UsersData.db")
                    cur=conn.cursor()
                    cur.execute('''UPDATE Users 
                            SET CurrentWeight=?
                            WHERE Id=?''',(line[18],line[12],))
                    conn.commit()

                if line[7] == "" or line[7] == "משקל":
                    continue
                else:
                    if line[0] != "":
                        last_name = line[0]
                    if line[0] == "":
                        temp_record = Record(line[7], line[8])
                        curr_user.my_exercises[last_name].add_record(temp_record)
                    else:
                        temp_record = Record(line[7], line[8])
                        if last_name not in curr_user.my_exercises:
                            temp_array = ExerciseArray(last_name)
                            temp_array.add_record(temp_record)
                            curr_user.my_exercises[last_name] = temp_array
                        else:
                            curr_user.my_exercises[last_name].add_record(temp_record)
        csv_file.close()
        return curr_user


