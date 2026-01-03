from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime, timedelta

# from plugins.slack_utils import slack_alert  # Comment out if slack_utils not available

default_args = {
    "owner": "ml-engineer",
    # "on_failure_callback": slack_alert,  # Comment out if slack_utils not available
}

with DAG(
    dag_id="pharmacy_model_pipeline",
    start_date=datetime(2025, 1, 1),
    default_args=default_args,
    catchup=False,
    schedule=None,
    tags=["pharmacy", "model"],
) as dag:

    train_model = BashOperator(
        task_id="train_voting_regressor_model",
        bash_command="""
        cd /Users/miftahhadiyannoor/Documents/pharma_sales && \
        python pipelines/training/train.py
        """,
    )

    generate_llm_insights = BashOperator(
        task_id="generate_llm_insights",
        bash_command="""
        cd /Users/miftahhadiyannoor/Documents/pharma_sales && \
        python pipelines/llm/llm_insight.py
        """,
    )

    train_model >> generate_llm_insights
