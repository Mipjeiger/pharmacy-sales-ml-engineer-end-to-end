from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from plugins.slack_utils import slack_alert

default_args = {
    "owner": "ml-engineer",
    "on_failure_callback": slack_alert,
}

with DAG(
    dag_id="pharmacy_model_pipeline",
    start_date=days_ago(1),
    default_args=default_args,
    catchup=False,
    schedule_interval="@weekly",
    tags=["pharmacy", "model"],
) as dag:

    train_model = BashOperator(
        task_id="train_voting_regressor_model",
        bash_command="""
        
        """,
    )

    generate_llm_insights = BashOperator(
        task_id="generate_llm_insights",
        bash_command="""
        
        """,
    )

    train_model >> generate_llm_insights
