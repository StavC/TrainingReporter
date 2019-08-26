from User import User
import json
from DataBase import *
from random import randint

def main():




    conn = create_connection("D:\SQLlite\\UsersData.db")
    users_table, exercises_table = my_tables()
    create_table(conn, users_table)
    create_table(conn, exercises_table)
    temp=randint(1,200000) #TODO change id to normal not rand
    stav = User(temp, "stav", "Cohen", "Male")
    stav.read_csv()
    #stav.plot_exercise()
    create_new_user(conn, stav) # new user in DB
    add_exercises_records_to_DB(conn, stav) # add his exercises to DB
    #return_user_info(conn,stav)
    plot_exercises_from_db(conn,stav)


if __name__ == '__main__':
    main()
