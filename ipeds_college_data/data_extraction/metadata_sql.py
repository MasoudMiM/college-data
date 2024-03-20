import pandas as pd
import os
import sys
import json

current_dir = os.path.dirname(os.path.realpath('__file__'))
# let's add this directory to the path
sys.path.append(current_dir)

# let's import the data extraction tools
from ipeds_college_data.data_extraction import database

script_directory = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(script_directory, '..'))

# Reading Excel file into DataFrame
EXCEL_FILE_PATH = ROOT_DIR+'/ipeds_data/IPEDS200405TablesDoc.xlsx'


TABLE_NAME = 'Tables04'
dic_tables = database.read_excel_to_dataframe(EXCEL_FILE_PATH, TABLE_NAME)
table_name_description = {}
for index, row in dic_tables.iterrows():
    table_name_description[row['TableName']] = row['Description']

TABLE_NAME = 'vartable04'
dic_var = database.read_excel_to_dataframe(EXCEL_FILE_PATH, TABLE_NAME)
varName_varTitle, varName_varTable = {}, {}
for index, row in dic_var.iterrows():
    varName_varTitle[row['varName']] = row['varTitle']
    varName_varTable[row['varName']] = row['TableName']

# let's convert these into json files
TABLE_DESC = ROOT_DIR+'/data_extraction/data/table_description.json'
VAR_DESC = ROOT_DIR+'/data_extraction/data/var_description.json'
VAR_TABLE= ROOT_DIR+'/data_extraction/data/var_table.json'
with open(TABLE_DESC, 'w') as file:
    json.dump(table_name_description, file, indent=4)
with open(VAR_DESC, 'w') as file:
    json.dump(varName_varTitle, file, indent=4)
with open(VAR_TABLE, 'w') as file:
    json.dump(varName_varTable, file, indent=4)

# Example usage:
config_file_path = "ipeds_college_data/config/connection.config"  # Path to your config file
db_connection = database.DatabaseConnection(config_file_path)
db_connection.connect()

# Example: Get values for a set of variables for a given institution
institution_name = '"LAMSON COLLEGE"'
variable_set = {"F1AF18", "F3B01"}  # Set of variables you want to retrieve
variable_description = {var: db_connection.get_var_description(var) for var in variable_set}
print(variable_description)
result = db_connection.get_values_for_institution(institution_name, variable_set, varName_varTable)

for count, value in enumerate(variable_set):
    print(f"Value for {variable_description[value]} ({value}) for institution {institution_name}: {result[value]}")

# ------ tution information
# "chg1py1": "Published tuition and fees 2002-03",
# "chg1py2": "Published tuition and fees 2003-04",

# "TUITION2": "In-state average tuition for full-time undergraduates",
# "FEE2": "In-state required fees for full-time undergraduates",
# "HRCHG2": "In-state per credit hour charge for part-time undergraduates",
# "CMPFEE2": " In-state comprehensive fee for full-time undergraduates",
# "TUITION3": "Out-of-state average tuition for full-time undergraduates",
# "FEE3": "Out-of-state required fees for full-time undergraduates",
# "HRCHG3": "Out-of-state per credit hour charge for part-time undergraduates",
# "CMPFEE3": "Out-of-state comprehensive fee for full-time undergraduates",
# "F1B01": "Tuition and fees, after deducting discounts and allowances",

# "TUFE2002": "Tuition and fees, 2002-03",
# "TUFE2003": "Tuition and fees, 2003-04",
# "TUFE2004": "Tuition and fees, 2004-05"



# ------ finanice information
# "F2E106": "Independent operations-Interest",
# "F2E107": "Independent operations-All other",
# "F2E111": "Operation and maintenance of plant-Total amount",
# "F2E112": "Operation and maintenance of plant-Salaries and wages",
# "F2E113": "Operation and maintenance of plant-Benefits",
# "F2E114": "Operation and maintenance of plant-Operation and maintenance of plant",
# "F2E115": "Operation and maintenance of plant-Depreciation",
# "F2E116": "Operation and maintenance of plant-Interest",
# "F2E117": "Operation and maintenance of plant-All other",
# "F2E121": "Other expenses-Total amount",
# "F2E122": "Other expenses-Salaries and wages",
# "F2E123": "Other expenses-Benefits",
# "F2E124": "Other expenses-Operation and maintenance of plant",
# "F2E125": "Other expenses-Depreciation",
# "F2E126": "Other expenses-Interest",
# "F2E127": "Other expenses-All other",

# "F1C101": "Scholarships and fellowships expenses -- Current year total_x000D_\n",
# "F1C102": "Scholarships and fellowships expenses -- Salaries and wages",
# "F1C103": "Scholarships and fellowships expenses -- Employee fringe benefits_x000D_\n",
# "F1C104": "Scholarships and fellowships expenses -- Depreciation_x000D_\n",
# "F1C105": "Scholarships and fellowships expenses -- All other_x000D_\n",

# "F1D01": "Total revenues and other additions",
# "F1D02": "Total expenses and other deductions",

# "F1D06": "Net assets end of year",
# "F1H01": "Value of endowment assets at the beginning of the fiscal year  ",
# "F1H02": "Value of endowment assets at the end of the fiscal year  ",

# "F1AF18": "Total expenses and losses ",
# "F1AG01": "Total current assets",
# "F1AG02": "Total non-current assets ",
# "F1AG03": "Total assets",
# "F1AG04": "Total current liabilities",
# "F1AG05": "Total noncurrent liabilities",
# "F1AG06": "Total liabilities ",

# "F3A01": "Total assets",
# "F3A02": "Total liabilities",
# "F3A03": "Total equity",
# "F3A04": "Total liabilities and equity",
# "F3B01": "Total revenues and investment return",
# "F3B02": "Total expenses ",


# ------ salary information
# "SALTOTL": "Average salary equated to 9-month contracts of full-time instructional faculty - all ranks",
# "SalProf": "Average salary equated to 9-month contracts of full-time instructional faculty - professors",
# "SalAssc": "Average salary equated to 9-month contracts of full-time instructional faculty - associate professors",
# "SalAsst": "Average salary equated to 9-month contracts of full-time instructional faculty - assistant professors ",
# "SalInst": "Average salary equated to 9-month contracts of full-time instructional faculty - instructors ",
# "Sallect": "Average salary equated to 9-month contracts of full-time instructional faculty - lecturers",
# "SALNRNK": "Average salary equated to 9-month contracts of full-time instructional faculty - No academic rank",


# ------ assets information
# "F2A01": "Long-term investments",
# "F2A02": "Total assets",
# "F2A03": "Total liabilities",
# "F2A04": "Total unrestricted net assets",
# "F2A05": "Total restricted net assets",
# "F2A06": "Total net assets",
    

# ------ enrollment information
# "SCFA2": "Total number of undergraduates",
# "SCFY2": "Total number of undergraduates",
# "COHRTSTU": "Enrolled any full-time first-time students",


# ------ graduation information
# "GBA4RTT": "Graduation rate - Bachelor degree within 4 years, total ",
# "GBA5RTT": "Graduation rate - Bachelor degree within 5 years, total ",
# "GBA6RTT": "Graduation rate - Bachelor degree within 6 years, total ",
# "GBA6RTM": "Graduation rate - Bachelor degree within 6 years, men",
# "GBA6RTW": "Graduation rate - Bachelor degree within 6 years, women",
