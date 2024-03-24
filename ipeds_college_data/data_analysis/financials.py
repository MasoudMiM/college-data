## Implement functions/classes for processing financial data.
import json
import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)
print(ROOT_DIR)

from data_extraction.database import DatabaseConnection

class FinancialDataExtraction:
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        # read the dataset name from the config file
        # it is written in front of database =
        try:
            with open(config_file_path) as f:
                for line in f:
                    if "database" in line:
                        self.dataset_name = line.split("=")[1].strip()
                        break
        except Exception as e:
            print(f"Error reading config file: {e}")

    def retrieve_financial_data(self, institution_name, variable_set):
        db_connection = DatabaseConnection(self.config_file_path)
        db_connection.connect()

        var_desc_path = f"{ROOT_DIR}/data_extraction/data/data_{self.dataset_name}/var_description.json"
        var_table_path = f"{ROOT_DIR}/data_extraction/data/data_{self.dataset_name}/var_table.json"
        
        variable_description = {var: db_connection.get_var_description(var, var_desc_path) for var in variable_set}
        # print(variable_description)
        variable_table = {var: db_connection.get_var_table(var, var_table_path) for var in variable_set}
        # print(variable_table)
        inst_table = db_connection.get_inst_unitid(var_table_path)

        financial_data = {}
        for variable in variable_set:
            table_name = variable_table[variable]
            if table_name:
                description = variable_description[variable]
                if description:
                    data = db_connection.get_values_for_institution(institution_name, variable, table_name, inst_table)  # Pass var_table directly
                    financial_data[variable] = {"description": description, "data": data}
                else:
                    financial_data[variable] = {"description": "Description not found", "data": None}
            else:
                financial_data[variable] = {"description": "Variable not found in var_table", "data": None}

        db_connection.close()
        return financial_data


if __name__ == "__main__":
    extractor = FinancialDataExtraction("ipeds_college_data/config/connection.config")

    # Example institution and variable sets
    institution_name = '"Stony Brook University"'
    variable_set_1 = {"F3B02","F2E107"} #, '"F2E107"', '"F2E111"'}  # Example set of variables

    financial_data = extractor.retrieve_financial_data(institution_name, variable_set_1)
    print(f"Financial data for institution {institution_name}:")
    for variable, data in financial_data.items():
        description = data["description"]
        values = data["data"]
        for key, value in values.items():
            if value is not None:
                print(f"Value for {description} ({variable}) for institution {institution_name}: {value}")
            else:
                print(f"Value for {description} ({variable}) for institution {institution_name}: No data available")

# TODO: come up with a reseanable approach to deal with a case where
# a given table in a database does not exist! as of now, it returns
# an error in the form of 
# Error: 1146 (42S02): Table '{database_name}.{table_table}' doesn't exist
                

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



# ------ finanice information}
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
