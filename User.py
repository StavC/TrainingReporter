import matplotlib.pyplot as plt
import csv
import tkinter.filedialog
from Record import Record
from ExerciseArray import ExerciseArray
from collections import defaultdict


class User(object):

    def __init__(self, first_name, last_name, height=0, weight=0):
        self.first_name = first_name
        self.last_name = last_name
        self.height = height
        self.weight = weight
        self.my_exercises = defaultdict(ExerciseArray)

    # self.my_exercises=[]

    # def add_exercise(self,exerciseArray):
    #     self.my_exercises.append(exerciseArray)

    def plot_exercise(self):

        for exercise in self.my_exercises:
            self.my_exercises[exercise].print_array()
            plt.plot(self.my_exercises[exercise].get_dates(), self.my_exercises[exercise].get_weights(), zorder=1)
            plt.scatter(self.my_exercises[exercise].get_dates(), self.my_exercises[exercise].get_weights(), s=300,
                        color='red', zorder=2)
            plt.suptitle(exercise)
            plt.show()

    def read_csv(self):

        csv_path = tkinter.filedialog.askopenfilename()
        with open(csv_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for line in csv_reader:
                if line[0] != "":
                    last_name = line[0]
                if line[0] == "":
                    temp_record = Record(line[4], line[5])
                    self.my_exercises[last_name].add_record(temp_record)
                else:
                    temp_record = Record(line[4], line[5])
                    if last_name not in self.my_exercises:
                        temp_array = ExerciseArray(last_name)
                        temp_array.add_record(temp_record)
                        self.my_exercises[last_name] = temp_array
                    else:
                        self.my_exercises[last_name].add_record(temp_record)



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
