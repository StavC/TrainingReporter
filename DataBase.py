import sqlite3
from sqlite3 import Error
from collections import defaultdict
from ExerciseArray import ExerciseArray
from Record import Record
from datetime import datetime
import tkinter.filedialog
import csv
import operator

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def my_tables():
    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS Users (
                                            Id integer PRIMARY KEY,
                                            Fname text NOT NULL,
                                            Lname text NOT NULL,
                                            Gender text,
                                            Height integer,
                                            Weight integer,
                                            Age integer,
                                            StartDate text,
                                            CurrentWeight
                                        ); """

    sql_create_exercises_table = """CREATE TABLE IF NOT EXISTS Exercises (
                                        Id integer ,
                                        ExerciseName ,
                                        Date text ,
                                        Weight integer NOT NULL,
                                        PRIMARY KEY(Id,ExerciseName,Date)
                                        FOREIGN KEY (id) REFERENCES Users (id)
                                    );"""

    sql_create_body_weights_table = """CREATE TABLE IF NOT EXISTS BodyWeights(
                                    Id integer,
                                    Date text,
                                    Weight integer NOT NULL,
                                    PRIMARY KEY(Id,Date,Weight)
                                    FOREIGN KEY (Id) REFERENCES Users (Id)
                                    );"""

    sql_create_benchpress_standards="""CREATE TABLE IF NOT EXISTS BenchPress(
                                    BodyWeight integer,
                                    Beginner integer,
                                    Novice integer,
                                    Intermediate integer,
                                    Advanced integer,
                                    Elite integer,
                                    Gender text,
                                    PRIMARY KEY(BodyWeight,Gender)
                                    );"""

    sql_create_squat_standards = """CREATE TABLE IF NOT EXISTS Squat(
                                        BodyWeight integer,
                                        Beginner integer,
                                        Novice integer,
                                        Intermediate integer,
                                        Advanced integer,
                                        Elite integer,
                                        Gender text,
                                        PRIMARY KEY(BodyWeight,Gender)
                                        );"""

    sql_create_deadlift_standards = """CREATE TABLE IF NOT EXISTS DeadLift(
                                        BodyWeight integer,
                                        Beginner integer,
                                        Novice integer,
                                        Intermediate integer,
                                        Advanced integer,
                                        Elite integer,
                                        Gender text,
                                        PRIMARY KEY(BodyWeight,Gender)
                                        );"""

    sql_create_headpress_standards = """CREATE TABLE IF NOT EXISTS HeadPress(
                                        BodyWeight integer,
                                        Beginner integer,
                                        Novice integer,
                                        Intermediate integer,
                                        Advanced integer,
                                        Elite integer,
                                        Gender text,
                                        PRIMARY KEY(BodyWeight,Gender)
                                        );"""


    return sql_create_users_table, sql_create_exercises_table,sql_create_body_weights_table,sql_create_benchpress_standards,sql_create_squat_standards,sql_create_deadlift_standards,sql_create_headpress_standards



def insert_user(conn, user):
    sql = ''' INSERT INTO Users(Id,Fname,Lname,Gender,Weight,Height,Age,StartDate,CurrentWeight)
              VALUES(?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, user)

    datetimeObj=datetime.now()
    print(datetimeObj)
    date_stamp=datetimeObj.strftime("%d/%m/%Y")
    print(date_stamp)
    print(user)
    cur.execute("INSERT INTO BodyWeights(Id,Date,Weight)VALUES(?,?,?)",(user[0],date_stamp,user[8],))
    return cur.lastrowid


def create_new_user(conn, user):
    with conn:
        curr_user = (user.id, user.first_name, user.last_name, user.gender, user.weight, user.height,user.age,user.start_date,user.current_weight)
        curr_id = insert_user(conn, curr_user)


def insert_exercise(conn, Exercise):
    sql = ''' INSERT INTO Exercises(Id,ExerciseName,Date,Weight)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, Exercise)
    return cur.lastrowid


def create_new_exercise(conn, user, exe_name, date, weight):
    with conn:
        curr_exe = (user.id, exe_name, date, weight)
        curr_id = insert_exercise(conn, curr_exe)


def add_exercises_records_to_DB(conn, user):
    with conn:
        while user.my_exercises:  # as long as there is more exercises
            pointer = user.my_exercises.popitem()
            temp_exe_arr = pointer[1]
            while temp_exe_arr.records_array:  # as long as there is more records in a certain exercise
                temp_record = temp_exe_arr.records_array.pop()
                create_new_exercise(conn, user, temp_exe_arr.name, temp_record.date, temp_record.weight)


def return_user_info(conn,user):
    cur=conn.cursor()
    cur.execute("SELECT * FROM Users WHERE Id=?",(user.id,))
    rows=cur.fetchall()
   # print(rows)
    #print(rows[0][0])
    #print(rows[0][1])
    #print(rows[0][2])
    return rows[0][0],rows[0][1],rows[0][2],rows[0][3],rows[0][4],rows[0][5]

def return_user_exercises(conn,user):
    cur=conn.cursor()
    cur.execute("SELECT * FROM Exercises WHERE Id=?",(user.id,))
    rows=cur.fetchall()
    return rows

def plot_exercises_from_db(conn,user):
    rows=return_user_exercises(conn,user)
    my_exercises_dict=defaultdict(ExerciseArray)
    for row in rows:
        temp_record=Record(row[3],row[2])
        if row[1] not in my_exercises_dict:
              temp_array=ExerciseArray(row[1])
              temp_array.add_record(temp_record)
              my_exercises_dict[row[1]]=temp_array
        else:
              my_exercises_dict[row[1]].add_record(temp_record)

    user.my_exercises=my_exercises_dict
    for name in user.my_exercises: # sorting by date
        user.my_exercises[name].records_array.sort(key=lambda date: datetime.strptime(date.date, "%d/%m/%Y"))
   # print(type(user.my_exercises))
    user.plot_exercise()


def check_if_need_to_create(conn,id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM Users WHERE Id=?", (id,))
    rows = cur.fetchall()
    if rows:
        print("not need to create user in table")
        return False
    else:
        print("need to create user in table")
        return True

def search_user(conn,id):
    cur = conn.cursor()
    cur.execute("SELECT Id FROM Exercises WHERE Id=?", (id,))
    user_id = cur.fetchall()
    return user_id

