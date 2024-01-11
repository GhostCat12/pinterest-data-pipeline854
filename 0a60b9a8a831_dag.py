from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksSubmitRunOperator, DatabricksRunNowOperator
from datetime import datetime, timedelta 


#Define params for Submit Run Operator
notebook_task = {
    'notebook_path': '/Users/maryam.hashmi@hotmail.co.uk/pinterest/pinterest_batch_data',         # <DATABRICKS_NOTEBOOK_PATH>
}


#Define params for Run Now Operator
notebook_params = {
    "Variable":5
}


default_args = {
    'owner': '0a60b9a8a831',                                            # <OWNER_NAME>
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,                                                   # <NUMBER_DESIRED_RETRIES>
    'retry_delay': timedelta(minutes=2)
}


with DAG('0a60b9a8a831_dag',
    # should be a datetime format
    start_date= datetime(2023, 12, 24),                             # <DESIRED_START_DATE>
    # check out possible intervals, should be a string
    schedule_interval='@daily',                                     # <DESIRED_INTERVAL>'
    catchup=False,
    default_args=default_args
    ) as dag:


    opr_submit_run = DatabricksSubmitRunOperator(
        task_id='submit_run',
        # the connection we set-up previously
        databricks_conn_id='databricks_default',
        existing_cluster_id='1108-162752-8okw8dgg',                 # <CLUSTER_ID>
        notebook_task=notebook_task
    )
    opr_submit_run
