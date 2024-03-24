import pandas as pd
import os
import json

import database

class DataExtraction:
    def __init__(self, dataset_name, table_name_des, table_name_var):
        self.DATASET_NAME = dataset_name
        self.TABLE_NAME_DES = table_name_des
        self.TABLE_NAME_VAR = table_name_var
        self.script_directory = os.path.dirname(os.path.realpath(__file__))
        self.ROOT_DIR = os.path.abspath(os.path.join(self.script_directory, '..'))
        self.EXCEL_FILE_PATH = f'{self.ROOT_DIR}/ipeds_data/{self.DATASET_NAME}TablesDoc.xlsx'

    def read_data_from_excel(self):
        dic_tables = database.read_excel_to_dataframe(self.EXCEL_FILE_PATH, self.TABLE_NAME_DES)
        table_name_description = {}
        for index, row in dic_tables.iterrows():
            table_name_description[row['TableName']] = row['Description']

        dic_var = database.read_excel_to_dataframe(self.EXCEL_FILE_PATH, self.TABLE_NAME_VAR)
        varName_varTitle, varName_varTable = {}, {}
        for index, row in dic_var.iterrows():
            varName_varTitle[row['varName']] = row['varTitle']
            varName_varTable[row['varName']] = row['TableName']

        return table_name_description, varName_varTitle, varName_varTable

    def convert_to_json(self, table_desc, var_desc, var_table):
        TABLE_DESC = f'{self.ROOT_DIR}/data_extraction/data/data_{self.DATASET_NAME}/table_description.json'
        VAR_DESC = f'{self.ROOT_DIR}/data_extraction/data/data_{self.DATASET_NAME}/var_description.json'
        VAR_TABLE = f'{self.ROOT_DIR}/data_extraction/data/data_{self.DATASET_NAME}/var_table.json'

        for file in [TABLE_DESC, VAR_DESC, VAR_TABLE]:
            if not os.path.exists(os.path.dirname(file)):
                try:
                    os.makedirs(os.path.dirname(file))
                except OSError as exc:
                    raise exc

        with open(TABLE_DESC, 'w') as file:
            json.dump(table_desc, file, indent=4)
        with open(VAR_DESC, 'w') as file:
            json.dump(var_desc, file, indent=4)
        with open(VAR_TABLE, 'w') as file:
            json.dump(var_table, file, indent=4)
