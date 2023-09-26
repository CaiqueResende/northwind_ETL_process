import pandas as pd
from sqlalchemy import create_engine
import sys
from pathlib import Path
from datetime import date

try:
  
  # getting date:

    date_execution = input("Date of execution (yyyy-mm-dd) - if today, leave it blank: ")
    if date_execution == "":
        date_execution = str(date.today())


    orders_path = "C:/Users/caiqr/Documents/Projetos/northwind/data/postgres/orders/" + date_execution + '/' + 'orders.csv'
    order_details_path = "C:/Users/caiqr/Documents/Projetos/northwind/data/csv/" + date_execution + '/' + 'order_details.csv'

    # transforming the tables into dataframes

    df_orders = pd.read_csv(orders_path, sep=';')
    df_order_details = pd.read_csv(order_details_path, sep=';')

    # merging the tables

    df_orders_and_details = df_orders.merge(df_order_details, left_on='order_id', right_on='order_id')

    # connecting with database northwind_trans

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
    print("Error at Step 2 - Run the script for step 2 again.")
    sys.exit(1)

print("Step 2 - Status: success")