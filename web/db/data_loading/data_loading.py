# from .. import config
import sqlalchemy
import pandas as pd
import numpy as np

connection = f'postgresql+psycopg2://admin:123@localhost:5416/dw_db'  # config.DATABASE_CONNECTION_URI
engine = sqlalchemy.create_engine(connection)
current_users_qry = "select id, username from users;"
current_users = pd.read_sql(current_users_qry, engine)

bv_raw_data = pd.read_csv('bv_raw_data.csv')

for column in bv_raw_data.columns:
    if column != 'day':
        # for each name in the csv check that the name exists in database
        if column in current_users['username'].tolist():
            # If exists in database add data to the table 1 at the time
            user_id = current_users.loc[current_users['username'] == column, 'id']
            user_data = bv_raw_data.loc[~bv_raw_data[column].isnull(), ['day', column]]

            insert_string = ""
            for index, col in user_data.iterrows():
                if col[column] != np.nan and col[column] != 0:
                    insert_string += f"""(
                    {user_id.item()}, cast('{col['day']}' as date), cast({col[column]} as int)),"""
            insert_string = insert_string[:-1]
            engine.execute(f"""
                                INSERT INTO daily_work ( user_id, dw_date, dw_minutes)
                                    VALUES {insert_string}
                            """
                           )