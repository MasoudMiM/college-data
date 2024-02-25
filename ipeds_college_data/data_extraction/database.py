import mysql.connector
import pandas as pd

class DatabaseConnection:
    # the object will need to know the host, user, password, database, and table
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    # the object will need to connect to the database
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
            )
            if self.connection.is_connected():
                print(f"Connected to MySQL database: {self.database}")
                return self.connection

        except mysql.connector.Error as e:
            print(f"Error: {e}")

    def execute_query(self, query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
        except mysql.connector.Error as e:
            print(f"Error: {e}")
            return None

    def close(self):
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed")
    
    # TODO: let's add a method to get the column names and unique values in the column
    # of a table named table_name+suffix where suffix is the 8th and 9th letter name of the database.
    # I temporarily added an example of how this code be done metadata.py file
    # it needs to be converted to a method in the class DatabaseConnection.
    # However, that approach uses the excel file. But I want to use the metadata
    # from the database itself, which are stored in the last three tables.



