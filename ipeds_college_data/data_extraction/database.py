import mysql.connector
import pandas as pd

def read_excel_to_dataframe(excel_file_path, table_name):
    try:
        excel_file = pd.ExcelFile(excel_file_path)
        df = pd.read_excel(excel_file, table_name)
        return df
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None
    
class DatabaseConnection:
    def __init__(self, config_file_path):
        self.config = self.read_config(config_file_path)
        self.connection = None

    def read_config(self, config_file_path):
        config = {}
        with open(config_file_path) as f:
            for line in f:
                key, value = line.strip().split("=")
                config[key.strip()] = value.strip()
        return config

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.config['host'],
                user=self.config['user'],
                password=self.config['password'],
                database=self.config['database'],
            )
            if self.connection.is_connected():
                print(f"Connected to MySQL database: {self.config['database']}")
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
    
    # let's add another method that gets a table name and converts it to a pandas dataframe
    # ans skip the first row which is the column names
    def get_table(self, table_name):
        query = f"SELECT * FROM {table_name}"
        rows = self.execute_query(query)
        if rows:
            df = pd.DataFrame(rows[1:], columns=rows[0])
            return df
        else:
            return None
    
    def get_var_description(self, var_name):
        query = f"SELECT varTitle FROM vartable04 WHERE varName = '\"{var_name}\"'"
        # print(query)
        rows = self.execute_query(query)
        if rows:
            return rows[0][0]
        else:
            return None
        
    def get_values_for_institution(self, institution_name, variable_set, var_table_dict):
        try:
            cursor = self.connection.cursor()

            # Check if the institution_name exists in the specified column
            institution_query = f"SELECT COUNT(*) FROM {var_table_dict['INSTNM']} WHERE INSTNM = %s"
            cursor.execute(institution_query, (institution_name,))
            institution_count = cursor.fetchone()[0]

            if institution_count == 0:
                print(f"Institution '{institution_name}' not found in the '{var_table_dict['INSTNM']}' table.")
                return None

            # Get the variable corresponding to UNITID (assuming it's always named "UNITID")
            unitid_variable = "UNITID"

            # Build the SQL query to get UNITID for the given institution_name
            unitid_query = f"SELECT {unitid_variable} FROM {var_table_dict['INSTNM']} WHERE INSTNM = %s LIMIT 1"
            cursor.execute(unitid_query, (institution_name,))
            unitid = cursor.fetchone()

            if not unitid:
                print(f"UNITID not found for institution '{institution_name}'.")
                return None

            # Build the SQL query to get values for the given variables using UNITID
            variable_values = {}
            for variable in variable_set:
                table = var_table_dict[variable]
                print(table, variable, unitid[0])
                query = f"SELECT {variable} FROM {table} WHERE {unitid_variable} = %s LIMIT 1"
                cursor.execute(query, (unitid[0],))
                value = cursor.fetchone()
                variable_values[variable] = value[0] if value else None

            return variable_values

        except mysql.connector.Error as e:
            print(f"Error: {e}")
            return None
        finally:
            cursor.close()

    # TODO: let's add a method to get the column names and unique values in the column
    # of a table named table_name+suffix where suffix is the 8th and 9th letter name of the database.
    # I temporarily added an example of how this could be done in metadata.py file.
    # It needs to be converted to a method in the class DatabaseConnection.
    # However, that approach uses the excel file. But I want to use the metadata
    # from the database itself, which are stored in the last three tables.


