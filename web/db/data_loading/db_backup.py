# from .. import config
import sqlalchemy
import pandas as pd
import numpy as np

connection = f'postgresql+psycopg2://admin:123@localhost:5416/dw_db'  # config.DATABASE_CONNECTION_URI
engine = sqlalchemy.create_engine(connection)
current_users_qry = "select * from users;"
users = pd.read_sql(current_users_qry, engine)
daily_work_qry = "select * from daily_work;"
daily_work = pd.read_sql(daily_work_qry, engine)

daily_work.to_csv("db_backup/daily_work.csv")
users.to_csv("db_backup/users.csv")
