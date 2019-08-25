import  sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)



def my_tables():
    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS Users (
                                            Id integer PRIMARY KEY,
                                            Fname text NOT NULL,
                                            Lname text NOT NULL,
                                            Gender text,
                                            Weight integer,
                                            Height integer
                                        ); """

    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS Exercises (
                                        id integer PRIMARY KEY,
                                        ExerciseName text NOT NULL,
                                        Date text NOT NULL,
                                        Weight integer NOT NULL,
                                        FOREIGN KEY (id) REFERENCES Users (id)
                                    );"""
    return sql_create_projects_table,sql_create_tasks_table