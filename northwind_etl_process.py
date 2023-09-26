import psycopg2
from psycopg2 import OperationalError
import pandas as pd
import sys
from pathlib import Path
from datetime import date

# Parâmetros para a conexão com a DB
host = "localhost"
port = 5432
dbname = "northwind"
user = "postgres"
password = "root"
connection_timeout = 10

# Establish a connection
try:
  connection = psycopg2.connect(
      host=host,
      port=port,
      database=dbname,
      user=user,
      password=password,
      connect_timeout=connection_timeout
  )
except OperationalError as e:
    # Handle connection timeout or other errors
    print(f"Step 1 - Connection with database failed: {e}")
    sys.exit(1)

## Getting the table names:

try:
  cursor = connection.cursor()

  cursor.execute("""SELECT table_schema, table_name
                        FROM information_schema.tables
                        WHERE table_schema != 'pg_catalog'
                        AND table_schema != 'information_schema'
                        AND table_type='BASE TABLE'
                        ORDER BY table_schema, table_name""")
  tables = cursor.fetchall()

  table_names = []

  for i in tables:
    table_names.append(i[1])


  date_execution = input("Date of execution (yyyy-mm-dd) - if today, leave it blank: ")
  if date_execution == "":
    date_execution = str(date.today())

  folder_path = "C:/Users/caiqr/Documents/Projetos/northwind/data/postgres/"

  for table in table_names:
    cursor.execute(f"SELECT * FROM {table}")
    table_data = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    table_df = pd.DataFrame(table_data, columns=column_names)
    
    path = folder_path +  table + "/" + date_execution + "/"
    Path(path).mkdir(parents=True, exist_ok=True) ## create folder
    table_df.to_csv(path + table + ".csv", index=False, sep=";") ## save as csv

  ## Fechando o cursor

  cursor.close()
  connection.close()

  ## Importando o arquivo CSV:
  path_csv = "C:/Users/caiqr/Documents/Projetos/northwind/order_details.csv"
  csv = pd.read_csv(path_csv)

  path_csv_target = "C:/Users/caiqr/Documents/Projetos/northwind/data/csv/" + date_execution + "/"
  file_name = "order_details.csv"

  Path(path_csv_target).mkdir(parents=True, exist_ok=True)
  csv.to_csv(path_csv_target + file_name, index=False, sep=';')

except:
  print("Error at step 1. Run the code again.")
  sys.exit(1)

## Step 2:

try:

  orders_path = "C:/Users/caiqr/Documents/Projetos/northwind/data/postgres/orders/" + date_execution + '/' + 'orders.csv'
  order_details_path = "C:/Users/caiqr/Documents/Projetos/northwind/data/csv/" + date_execution + '/' + 'order_details.csv'

  # transforming the tables into dataframes

  df_orders = pd.read_csv(orders_path, sep=';')
  df_order_details = pd.read_csv(order_details_path, sep=';')

  # merging the tables

  df_orders_and_details = df_orders.merge(df_order_details, left_on='order_id', right_on='order_id')

  # connecting with database northwind_trans

  import psycopg2
  from sqlalchemy import create_engine

  # parameters for the database connection
  host = "localhost"
  port = 5432
  dbname = "northwind_trans"
  user = "postgres"
  password = "root"

  # creating the engine for the connection
  
  try:
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{dbname}", connect_args={'connect_timeout': 10})


    # adding table to postgreSQL

    table_name = 'orders_and_details'

    df_orders_and_details.to_sql(table_name,
                                engine, 
                                if_exists='replace', ## if data need to be appended to existent table, change parameter to 'append'
                                index=False) 

    # closing the connection

    engine.dispose()

 

  except:
    print("Step 2 - Error at database connection.")
    sys.exit(1)

except:
  print("Error at Step 2 - Run the script for step 2.")
  sys.exit(1)

print("The northwind ETL process is finished.")