import subprocess
from dagster import job, op
from extract import fetch_users
from load import load_to_postgres


@op
def extract_data():
    """
    Extracts user data from an API.
    """
    return fetch_users()


@op
def load_data(context, df):
    """
    Loads raw DataFrame into PostgreSQL as 'raw_users'.
    """
    load_to_postgres(df, "raw_users")


@op
def run_dbt():
    result = subprocess.run(
        ["dbt", "run", "--profiles-dir", "../"],
        cwd="dbt",  # make sure it's correct
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise Exception(f"dbt run failed: {result.stderr}")

    print("✅ dbt run completed successfully.")
    print(result.stdout)

@job
def etl_pipeline():
    """
    Full ETL pipeline:
    1. Extract data from API
    2. Load into raw_users table
    3. Run dbt transformations
    """
    df = extract_data()
    load_data(df)
    run_dbt()