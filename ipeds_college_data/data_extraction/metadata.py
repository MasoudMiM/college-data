##
import pandas as pd
import json
import numpy as np
import os

# let's read the excel file located at this address:
# ROOT_DIR+ipeds_data/IPEDS200405TablesDoc.xlsx
# Get the directory of the current script file and then get the root directory
script_directory = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(script_directory, '..'))
print(ROOT_DIR)

EXCEL_FILE_PATH = ROOT_DIR+'/ipeds_data/IPEDS200405TablesDoc.xlsx'
print(EXCEL_FILE_PATH)
TABLE_NAME = 'vartable04'
CONFIG_FILE = ROOT_DIR+'/config/metadata.json'

excel_file = pd.ExcelFile(EXCEL_FILE_PATH)
df_var = pd.read_excel(excel_file, TABLE_NAME)

# let's create separate dataframes for each unique value in the column "TableName"
# and then save them all in a dictionary with the table name as the key
# and the dataframe as the value
df_dict = {}
for table_name in df_var['TableName'].unique():
    df_dict[table_name] = df_var[df_var['TableName'] == table_name]
    # save each dataframe in a csv file
    df_dict[table_name].to_csv(ROOT_DIR+'/config/'+table_name+'.csv', index=False)

# let's read varName and varTitle from the excel file and creat a dictionary
# with varName as key and varTitle as value
varName_varTitle = {}
for index, row in df_var.iterrows():
    varName_varTitle[row['varName']] = row['varTitle']

# let's also get table names, table titles and table descriptions
# from excel file, from tab "tables04" which are in coulmns named "TableName", "TableTitle" and "Description" and
# save them in a dictionary and then save the dictionary in a json file
TABLE_NAME = 'Tables04'
df_tables = pd.read_excel(excel_file, TABLE_NAME)
table_name_table_title, table_name_table_description = {}, {}

for index, row in df_tables.iterrows():
    table_name_table_title[row['TableName']] = row['TableTitle']

for index, row in df_tables.iterrows():
    table_name_table_description[row['TableName']] = row['Description']

# Create a JSON file from the dictionary and save it in the .ipeds_dcollege_data/config folder
# let's also make sure that the jason file is properly formatted such that each key-value pair
# is on a new line.
TABLE_DESCRIPTION_FILE = ROOT_DIR+'/config/table_description.json'
with open(TABLE_DESCRIPTION_FILE, 'w') as file:
    json.dump(table_name_table_description, file, indent=4)


# let's read the variables in tab "vartable04" from the same excel file
# and put them in a dataframe and then save the dataframe in a csv file
VARIABLES_FILE = ROOT_DIR+'/config/variables.csv'
df_var.to_csv(VARIABLES_FILE, index=False)




