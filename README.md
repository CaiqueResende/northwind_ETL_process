# Northwind ETL Process

This repository contains a Python script for the Extract, Transform, and Load (ETL) process for the Northwind database ([entity relationship diagram](url)). The Northwind database is a sample database provided by Microsoft for demonstration purposes. The ETL process extracts data from this database, transforms it, and loads it into a target database.

The primary objective of this script is to facilitate the extraction of data from PostgreSQL tables and a CSV file. Subsequently, it orchestrates the storage of this data in a local directory. Additionally, the script is designed to merge the 'order' table with the CSV file's contents and subsequently load this new dataset into another PostgreSQL database.

**Requirements for the script:**

1. **Step-by-Step Execution**: The script allows for the execution of each step independently. This flexibility enables users to run only the necessary steps as needed.

2. **Dependency on Step 1**: Step 2 is configured to run only if Step 1 succeeds. This ensures that data extraction and staging are completed successfully before proceeding to data transformation and loading.

3. **Error Tracking**: In the event of an error, the script is designed to provide clear information about the step at which the error occurred. This feature enables users to pinpoint issues and rerun the script from the appropriate step for efficient troubleshooting.

4. **Date Identification**: The script incorporates date identification in the naming or path of each table. This ensures that data is organized and distinguishable by date. Additionally, users have the flexibility to run the process with past dates, facilitating historical data retrieval and analysis.

These requirements enhance the script's usability and robustness, making it a reliable tool for managing the ETL process with PostgreSQL and CSV data.

## Prerequisites

Before running the ETL process, ensure you have the following prerequisites:

1. **PostgreSQL**: You need to have PostgreSQL installed and running locally.

2. **Python**: This script is written in Python. Make sure you have Python installed on your system.

3. **Required Python Libraries**: Install the required Python libraries by running the following command:

   ```
   pip install psycopg2 pandas sqlalchemy
   ```

## How does the script work?

### Scripts:

- [Full Script](scripts/northwind_etl_process.py)
- [Step 1](scripts/step1_northwind_etl_process.py)
- [Step 2](scripts/step2_northwind_etl_process.py)

### Step 1 - Data Extraction and Staging

1. **Database Connection**: Configure the source database connection parameters in the script:

   - `host`: The PostgreSQL host.
   - `port`: The PostgreSQL port.
   - `dbname`: The name of the Northwind database.
   - `user`: Your PostgreSQL username.
   - `password`: Your PostgreSQL password.

2. **Staging Area**: Specify the folder path where the extracted data will be staged. By default, the postgres tables are set to `"C:/Users/caiqr/Documents/Projetos/northwind/data/postgres/"` and the CSV file is set to `"C:/Users/caiqr/Documents/Projetos/northwind/data/csv/"`.

3. **Step 1**: At step 1, the script will extract tables from the Northwind database, save them as CSV files in the staging area with a timestamp, and also export the `order_details` table to a separate CSV file. If a error occurs at this step, the script will close and an error message will be printed.

4. Date: the process date will be asked and should be inputed in the format "yyyy-mm-dd". If date is today, just leave it blank.

### Step 2 - Data Transformation and Loading

1. **Execute Step 2**: After successfully running Step 1, execute Step 2. This step performs the following tasks:

   - Reads the CSV files generated in Step 1.
   - Merges the `orders` and `order_details` tables.
   - Connects to a target database (specified in the script).
   - Loads the merged data into a new table in the target database (by default, the target database is named "northwind_trans").

2. **Database Connection**: Configure the target database connection parameters in the script:

   - `host`: The PostgreSQL host.
   - `port`: The PostgreSQL port.
   - `dbname`: The name of the Northwind database.
   - `user`: Your PostgreSQL username.
   - `password`: Your PostgreSQL password.

### Completion

Upon successful completion of the ETL process, the merged data from the `orders` and `order_details` tables will be available in the target database.

## Notes

- The script assumes that the Northwind database and the target database (e.g., "northwind_trans") exist in your PostgreSQL instance. You may need to create the target database manually if it does not already exist.

- The script uses hard-coded file paths and database connection parameters. Adjust these parameters as needed to match your environment.

- If any errors occur during execution, the script will provide error messages to assist with troubleshooting.

- This ETL process is designed for educational and demonstration purposes. In production environments, additional error handling, logging, and security measures should be implemented.

Thank you for using the Northwind ETL script! If you have any questions or encounter issues, please feel free to reach out for assistance.
