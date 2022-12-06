# from .. import config
import sqlalchemy
import pandas as pd
import numpy as np

connection = f'postgresql+psycopg2://admin:123@localhost:5416/dw_db'  # config.DATABASE_CONNECTION_URI
engine = sqlalchemy.create_engine(connection)
engine.execute(f"""
                    UPDATE daily_work
SET last_update_dt = CURRENT_DATE
                """
               )

