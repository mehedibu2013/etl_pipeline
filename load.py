from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()
db_conn_string = os.getenv("DB_CONNECTION_STRING")
if not db_conn_string:
    raise ValueError("DB_CONNECTION_STRING not set in .env")

engine = create_engine(db_conn_string)
logger = logging.getLogger(__name__)


def load_to_postgres(df, table_name):
    with engine.connect() as conn:
        with conn.begin():
            logger.info(f"Dropping {table_name} with CASCADE...")
            conn.execute(text(f"DROP TABLE IF EXISTS {table_name} CASCADE"))

        logger.info(f"Inserting into {table_name}")
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        logger.info(f"Loaded {len(df)} records into '{table_name}'")