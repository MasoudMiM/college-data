
import mysql.connector

# let's make this an object
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

    def close(self):
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed")

##### test the class
# if __name__ == "__main__":
#     db = DatabaseConnection("localhost", "root", "password", "IPEDS200405")
#     db.connect()
#     table_name = 'C2004_A'
#     rows = db.execute_query(f"SELECT * FROM {table_name} LIMIT 10;")
#     for row in rows:
#         print(row)
#     db.close()

