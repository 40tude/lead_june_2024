import os
import logging
import pandas as pd
from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator

k_GouvHTML = "https://www.data.gouv.fr/fr/datasets/r/5c4e1452-3850-4b59-b11c-3dd51d7fb8b5"
k_Data = "./data"


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# ti = self
def fetch_data(ti):
    logging.info("Fetching data")
    df = pd.read_csv(k_GouvHTML)
    filename = os.path.join(k_Data, f"{datetime.now().strftime('%Y%m%d')}_raw_covid.csv")
    df.to_csv(filename, index=False)
    ti.xcom_push("target_filename", filename)
    logging.info("Data saved - %s", filename)


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# ti = self
def transform_data(ti):
    logging.info("Transforming data")
    filename = ti.xcom_pull(task_ids="fetch_data", key="target_filename")
    logging.info("target_filename: %s", filename)
    df = pd.read_csv(filename)
    mean = df.groupby("date")["incid_hosp"].mean()
    mean_filename = os.path.join(k_Data, f"{datetime.now().strftime('%Y%m%d')}_cooked_covid.csv")
    mean.to_csv(mean_filename)
    ti.xcom_push("mean_target_filename", mean_filename)
    logging.info("Means saved -  %s", mean_filename)


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
with DAG("covid_dag", start_date=datetime(2022, 1, 1), schedule_interval="@hourly", catchup=False) as dag:
    fetch_data = PythonOperator(task_id="fetch_data", python_callable=fetch_data)
    transform_data = PythonOperator(task_id="transform_data", python_callable=transform_data)

    fetch_data >> transform_data
