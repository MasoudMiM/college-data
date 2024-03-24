import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)

from data_extraction import DataExtraction

Database_names = ["IPEDS200405", "IPEDS200708", "IPEDS201011", 
                  "IPEDS201314", "IPEDS201617"]

Table_names_dec = ['Tables04', 'Tables07', 'Tables10', 
                   'Tables13', 'Tables16']

Table_names_var = ['vartable04', 'varTable07', 
                   'varTable10', 'vartable13', 
                   'vartable16']

for i in range(len(Database_names)):
    print(f"Extracting data from {Database_names[i]}")
    extractor = DataExtraction(Database_names[i], Table_names_dec[i], Table_names_var[i])
    table_desc, var_desc, var_table = extractor.read_data_from_excel()
    extractor.convert_to_json(table_desc, var_desc, var_table)
