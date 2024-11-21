from datetime import datetime

import pandas as pd
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

default_args = {
    "owner": "airflow",
    "start_date": datetime(2022, 6, 1),
}


def _create_small_csv():
    """Creates a small CSV and saves it to `/tmp/my_csv_file.csv`."""
    pd.DataFrame({"first_name": ["Dark", "Dark"], "last_name": ["Vador", "Maul"]}).to_csv(
        "/tmp/my_csv_file.csv", header=None, index=False
    )


with DAG(dag_id="s3_redshift_dag", default_args=default_args, catchup=False) as dag:
    create_small_csv = PythonOperator(task_id="create_small_csv", python_callable=_create_small_csv)

    create_small_csv
