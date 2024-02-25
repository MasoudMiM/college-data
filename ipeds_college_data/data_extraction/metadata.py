##
import pandas as pd
import json
import numpy as np

# let's read the excel file located at this address:
# ROOT_DIR+ipeds_data/IPEDS200405TablesDoc.xlsx
# from tab "vartable04"
ROOT_DIR = ''
EXCEL_FILE_PATH = ROOT_DIR+'ipeds_data/IPEDS200405TablesDoc.xlsx'
TABLE_NAME = 'vartable04'
CONFIG_FILE = ROOT_DIR+'config/metadata.json'

excel_file = pd.ExcelFile(EXCEL_FILE_PATH)
df_var = pd.read_excel(excel_file, TABLE_NAME)

# Convert NumPy arrays to Python lists in the DataFrame
df_var = df_var.apply(lambda x: x.tolist() if isinstance(x, np.ndarray) else x)

# Get column names and unique values
column_names = df_var.columns
column_values = {}
for column in column_names:
    column_values[column] = df_var[column].unique()

# Create a JSON file from the dictionary and save it in the .ipeds_dcollege_data/config folder
with open(CONFIG_FILE, 'w') as f:
    json.dump(column_values, f, default=str)




