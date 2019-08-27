import matplotlib.pyplot as plt
import csv
import tkinter.filedialog
from Record import Record
from ExerciseArray import ExerciseArray
from collections import defaultdict
from DataBase import *
import json


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

        for exercise in self.my_exercises:
            # self.my_exercises[exercise].print_array()
            plt.plot(self.my_exercises[exercise].get_dates(), self.my_exercises[exercise].get_weights(), zorder=1)
            plt.scatter(self.my_exercises[exercise].get_dates(), self.my_exercises[exercise].get_weights(), s=300,
                        color='red', zorder=2)
            plt.suptitle(exercise[::-1])
            plt.show()

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
