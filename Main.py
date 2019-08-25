from User import User
import json
from DataBase import *
def main():

    stav=User("stav","Cohen")
   # stav.read_csv()
   # stav.plot_exercise()
    conn=create_connection("D:\SQLlite\\UsersData.db")
    data1,data2= my_tables()
    create_table(conn,data1)
    create_table(conn,data2)

if __name__ == '__main__':
    main()