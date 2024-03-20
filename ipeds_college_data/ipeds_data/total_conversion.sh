#!/bin/bash

# Main log file for stdout
LOG_FILE="log_file.txt"
# Warning log file for stderr
WARNING_LOG="warning_log.txt"
# Redirect stdout to both console and the main log file
exec > >(tee -a "$LOG_FILE") 
# Redirect stderr to the warning log file
exec 2> >(tee -a "$WARNING_LOG" >/dev/null)

MYSQL_USERNAME="root"
MYSQL_PASSWORD="password"
ACCDB_DIR="/home/masoudmim/Documents/Projects/college-data/ipeds_college_data/ipeds_data/"
ACCDB_FILES=("IPEDS200405" "IPEDS200506.accdb" "IPEDS200607.accdb" "IPEDS200708" "IPEDS200809.accdb" "IPEDS200910.accdb" "IPEDS201011" "IPEDS201112.accdb" "IPEDS201213.accdb" "IPEDS201314" "IPEDS201415.accdb" "IPEDS201516.accdb" "IPEDS201617" "IPEDS201718.accdb" "IPEDS201819.accdb" "IPEDS201920.accdb" "IPEDS202021.accdb" "IPEDS202122.accdb" "IPEDS202223.accdb") # Add your ACCDB file names here

for accdb_file in "${ACCDB_FILES[@]}"; do
  # Extract database name from ACCDB file (replace extension with _db)
  db_name=$(basename "$accdb_file" .accdb)
  printf '***********************************\n'
  printf 'database name: %s\n' "$db_name"

  # Step 1: Convert ACCDB to CSV using mdbtools
  OUTPUT_DIR="output_$db_name"
  mkdir -p "$OUTPUT_DIR"
  printf 'output directory: %s\n' "$OUTPUT_DIR"

  # Get the list of tables
  tables=$(mdb-tables -1 "$ACCDB_DIR/$accdb_file.accdb")

  # Loop through each table and export to CSV
  printf 'looping through the tables ...\n'
  for table in $tables; do
    printf ' table: %s' "$table"
    mdb-export "$ACCDB_DIR/$accdb_file.accdb" "$table" > "$OUTPUT_DIR/$table.csv"
  done

  # Step 2: Enable LOAD DATA LOCAL on MySQL Server
  # Note: Adjust the MySQL configuration and restart the server before running this script

  # Step 3: Create the database if not exists
  printf 'creating database...\n'
  mysql -u "$MYSQL_USERNAME" -p"$MYSQL_PASSWORD" -e "CREATE DATABASE IF NOT EXISTS $db_name;"

  # Step 4: Import CSV files into MySQL with dynamic table creation
  printf 'importing the csv files into MySQL ...\n'
  for file in "$OUTPUT_DIR"/*.csv; do
    table_name=$(basename "$file" .csv)

    # Read the first line of the CSV file to infer column names and types
    # columns_info=$(head -n 1 "$file" | awk -F',' '{for(i=1;i<=NF;++i) printf "column%d %s,", i, ($i ~ /^[0-9]+$/ ? "INT" : "VARCHAR(30)")}')
    
    # Remove trailing comma and spaces
    # columns_info=$(echo "$columns_info" | sed 's/,$//')

    # Read the first line of the CSV file to get the actual column names
    column_names=$(head -n 1 "$file" | tr ',' '\n')
    
    # Generate column information with actual column names and data types
    columns_info=""
    for column_name in $column_names; do
      columns_info+="`echo $column_name | sed 's/[^a-zA-Z0-9]/_/g'` VARCHAR(255), "
    done

    # Remove trailing comma and spaces
    columns_info=$(echo "$columns_info" | sed 's/,\s*$//')

    # Create table if not exists
    mysql -u "$MYSQL_USERNAME" -p"$MYSQL_PASSWORD" -e "CREATE TABLE IF NOT EXISTS $db_name.$table_name ($columns_info);"

    # Load data into the table
    mysql -u "$MYSQL_USERNAME" -p"$MYSQL_PASSWORD" --local-infile=1 -e "LOAD DATA LOCAL INFILE '$file' INTO TABLE $db_name.$table_name FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';"
  done

  # Clean up: Remove temporary CSV files
  printf 'deleting the output directory...\n'
  rm -rf "$OUTPUT_DIR"
  printf '***********************************\n'
done

