from User import User
import json
from DataBase import *
from random import randint
from GUI import *
from GUI import  GUI
from Calendar import  MplCalendar

#todo fix CSV BUGS of look
def main():
    conn = create_connection("D:\SQLlite\\UsersData.db")
    users_table, exercises_table,body_weights_table,benchpress_standards,squat_standards,deadlift_standards,headpress_standards = my_tables()
    create_table(conn, users_table)
    create_table(conn, exercises_table)
    create_table(conn,body_weights_table)
    create_table(conn,benchpress_standards)
    create_table(conn,squat_standards)
    create_table(conn,deadlift_standards)
    create_table(conn,headpress_standards)

    root= Tk()
    gui = GUI(root)
    root.title("WhyFitness Reporter")

    root.mainloop()



if __name__ == '__main__':
    main()
