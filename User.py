import matplotlib.pyplot as plt
import csv
import tkinter.filedialog
import matplotlib.backends.backend_pdf
from DataBase import *


class User(object):

    def __init__(self, id, first_name, last_name, gender, height, weight,age):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.height = height
        self.weight = weight
        self.gender = gender
        self.age=age
        self.my_exercises = defaultdict(ExerciseArray)

    def plot_exercise(self):
        pdf = matplotlib.backends.backend_pdf.PdfPages("FullReport.pdf")


        for exercise in self.my_exercises:
            # self.my_exercises[exercise].print_array()
            fig, ax = plt.subplots()
            plt.plot(self.my_exercises[exercise].get_dates(), self.my_exercises[exercise].get_weights(), zorder=1)
            plt.scatter(self.my_exercises[exercise].get_dates(), self.my_exercises[exercise].get_weights(), s=10,
                        color='red', zorder=2)
            plt.suptitle(exercise[::-1])
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=90, ha="right")
            plt.gcf().subplots_adjust(bottom=0.20)


            if self.my_exercises[exercise].length()>100:
                fig.set_size_inches(100, 100)

            elif self.my_exercises[exercise].length()>90:
                fig.set_size_inches(90, 90)

            elif self.my_exercises[exercise].length()>80:
                fig.set_size_inches(80, 80)

            elif self.my_exercises[exercise].length()>70:
                fig.set_size_inches(70, 70)

            elif self.my_exercises[exercise].length()>60:
                fig.set_size_inches(60, 60)

            elif self.my_exercises[exercise].length()>50:
                fig.set_size_inches(50, 50)

            elif self.my_exercises[exercise].length()>40:
                fig.set_size_inches(40, 40)

            elif self.my_exercises[exercise].length()>30:
                fig.set_size_inches(30, 30)

            elif self.my_exercises[exercise].length()>20:
                fig.set_size_inches(20, 20)
            plt.show()
            pdf.savefig(fig)
        pdf.close()


    def read_csv_create_or_load_user(self=0):
        csv_path = tkinter.filedialog.askopenfilename()
        with open(csv_path, 'r', encoding="cp1255") as csv_file:
            csv_reader = csv.reader(csv_file)
            need_to_create = True
            for line in csv_reader:
                if need_to_create and line[12] != "תז":
                    curr_user = User(line[12], line[10], line[11], line[13], line[15], line[14],line[16])
                    need_to_create = False

                if line[7] == "" or line[7] == "משקל":
                    continue
                else:
                    # print(line[0])
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
        return curr_user


'''


    def read_csv(self):

    csv_path=tkinter.filedialog.askopenfilename()
    with open(csv_path,'r') as csv_file:
        csv_reader=csv.reader(csv_file)
        for line in csv_reader:
                 if line[0]!="":
                     temp_record=Record(line[4],line[5])
                     if line[0] not in self.my_exercises :
                          temp_array=ExerciseArray(line[0])
                          temp_array.add_record(temp_record)
                          self.my_exercises[line[0]]=temp_array
                     else:
                        self.my_exercises[line[0]].add_record(temp_record




def __init__(self,first_name,last_name,height=0,weight=0):
    self.first_name=first_name
    self.last_name=last_name
    self.height=height
    self.weight=weight
    self.bench_press_weights=[]
    self.bench_press_dates=[]


def add_bench_press_weights(self,bench_monthly_weights):
    for weight in bench_monthly_weights:
        self.bench_press_weights.append(weight)

def add_bench_press_dates(self, bench_monthly_dates):
    for date in bench_monthly_dates:
        self.bench_press_dates.append(date)

def display_bench_press_weights(self):
    fig=plt.plot(self.bench_press_dates,self.bench_press_weights,zorder=1)
    plt.scatter(self.bench_press_dates,self.bench_press_weights,s=300,color='red',zorder=2)
    plt.suptitle("Bench Press")

    plt.show()

def read_csv(self):

    csv_path=tkinter.filedialog.askopenfilename()
    with open(csv_path,'r') as csv_file:
        csv_reader=csv.reader(csv_file)

        for line in csv_reader:
            if line[0] in "Bench Press":
                print(f"{line[0]} , {line[4]}, {line[5]}")
                self.bench_press_weights.append(line[4])
                self.bench_press_dates.append(line[5])
            elif line[0] in "Head Press":    
'''
