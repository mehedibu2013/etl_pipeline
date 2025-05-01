import pandas as pd
from extract import fetch_users
from load import load_to_postgres

df = fetch_users()
load_to_postgres(df, "raw_users")