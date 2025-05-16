
# 🧾 ETL Pipeline with Dagster, dbt & PostgreSQL

This repository contains a full ETL pipeline that:
- Extracts data from a public API
- Loads it into a local PostgreSQL database
- Transforms it using dbt (Data Build Tool)
- Orchestrates everything using **Dagster**

✔️ Great for learning how to build modern data pipelines  
✔️ Works on Windows (tested in PowerShell / PyCharm)  
✔️ Includes scheduling-ready setup  

---

## 🧰 Technologies Used

| Tool | Purpose |
|------|---------|
| **Python** | Scripting and orchestration |
| **Dagster** | Workflow orchestration and scheduling |
| **dbt Core** | Transformations using SQL |
| **PostgreSQL** | Data warehouse (local or remote) |

---

## 📁 Project Structure

```
etl_pipeline/
│
├── .env                  # Contains DB connection string
├── .gitignore             # Git ignore file
├── README.md              # This file
├── dagster.yaml           # Dagster configuration
├── extract.py             # Fetch data from external APIs
├── load.py                # Load data into PostgreSQL
├── pipeline.py            # Dagster job definition
├── requirements.txt       # Python dependencies
│
└── dbt/                 # dbt transformation layer
    ├── dbt_project.yml    # dbt config
    └── models/
        └── stg_users.sql  # Transformation logic
```

---

## 🛠 Setup Instructions

### 1. Clone or Create Project

If you're creating manually:

```bash
mkdir etl_pipeline
cd etl_pipeline
mkdir dbt
mkdir dbt/models
```

### 2. Install Python Dependencies

Make sure you have Python 3.9+ installed.

```powershell
pip install -r requirements.txt
```

### 3. Set Up PostgreSQL

Install PostgreSQL for Windows:  
🔗 [https://www.enterprisedb.com/downloads/postgres-postgresql-downloads#windows](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads#windows)

Ensure a database named `etl_db` exists:

```powershell
psql -U postgres -h localhost -c "CREATE DATABASE etl_db;"
```

---

### 4. Set Environment Variables

Create `.env` at the root of your project:

```env
DB_CONNECTION_STRING=postgresql+psycopg2://postgres:postgres@localhost:5432/etl_db
```

Then install support for `.env`:

```powershell
pip install python-dotenv
```

> Make sure this file is not committed to version control!

---

## 🔄 Run the Pipeline

### Option A: Using Dagster UI

Start the Dagster webserver:

```powershell
dagster dev -f pipeline.py
```

Go to http://localhost:3000 → Select your job → Click **Launch Run**

### Option B: Run via Command Line

Test the pipeline without the UI:

```powershell
python -c "from pipeline import etl_pipeline; etl_pipeline.execute_in_process()"
```

This will run the whole job locally.

---

## 🔨 dbt Setup

Your dbt transformation model is in:

```
dbt/models/stg_users.sql
```

Which contains:

```sql
SELECT 
  id,
  name,
  email,
  company_name
FROM raw_users
WHERE email IS NOT NULL
```

Run dbt transformations directly:

```powershell
cd dbt
dbt debug --profiles-dir ../
dbt run
```

---

## ⚠️ Known Issue: Can't Drop Table Because of Dependent Views

You may get an error like:

```
cannot drop table raw_users because other objects depend on it
HINT: Use DROP ... CASCADE to drop dependent objects
```

### ✅ Fix: Update Your `load.py` File

Use `CASCADE` when dropping tables:

```python
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
engine = create_engine(os.getenv("DB_CONNECTION_STRING"))

def load_to_postgres(df, table_name):
    with engine.connect() as conn:
        with conn.begin():
            logger.info(f"Dropping {table_name} with CASCADE...")
            conn.execute(text(f"DROP TABLE IF EXISTS {table_name} CASCADE"))
        df.to_sql(table_name, engine, if_exists='append', index=False)
        logger.info(f"Loaded {len(df)} records into '{table_name}'")
```

Now `raw_users` can be dropped safely if `stg_users` depends on it.

---

## 🕒 Schedule Weekly

Since `SystemCronScheduler` doesn't work natively on Windows, use:

### Option A: Task Scheduler

Create a `.bat` file:

#### `run_pipeline.bat`

```bat
@echo off
cd /d "F:\python projects\etl_pipeline"
call .venv\Scripts\activate
python -c "from pipeline import etl_pipeline; etl_pipeline.execute_in_process()"
```

Then:
- Open **Task Scheduler**
- Create Basic Task → Daily / Weekly
- Action → Start Program → Select `run_pipeline.bat`

✅ Done! Now runs weekly.

---

## 📦 Sample Requirements (`requirements.txt`)

```txt
requests
pandas
sqlalchemy
psycopg2-binary
python-dotenv
dagster
dagit
dbt-core
dbt-postgres
```

---

## 📝 How to Contribute

Feel free to add more transformations in the `models/` folder, or improve the pipeline by adding:
- More robust error handling
- Email notifications on failure
- Unit tests
- Docker support

---

## 📄 License

MIT License — feel free to modify and distribute

---

## 💬 Questions?

Let me know if you'd like help:
- Packaging this into a downloadable ZIP
- Automating cleanup
- Adding more transformations

---

Would you like me to generate a **downloadable ZIP** of this full project including all files? Just say yes 👍
