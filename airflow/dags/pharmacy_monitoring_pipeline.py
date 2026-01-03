from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime, timedelta

# from plugins.slack_utils import slack_alert  # Comment out if slack_utils not available

default_args = {
    "owner": "ml-engineer",
    # "on_failure_callback": slack_alert,  # Comment out if slack_utils not available
}

with DAG(
    dag_id="pharmacy_monitoring_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    default_args=default_args,
    tags=["pharmacy", "monitoring"],
) as dag:

    check_model_quality = SQLExecuteQueryOperator(
        task_id="check_model_quality",
        conn_id="pharmacy_db",
        sql="""
        SELECT COUNT(*) FROM features.sales_feature WHERE total_sales < 0;
        """,
    )

    publish_feature_store = SQLExecuteQueryOperator(
        task_id="publish_feature_store",
        conn_id="pharmacy_db",
        sql="""
        CREATE TABLE IF NOT EXISTS features_store.sales_features_v1 AS
        SELECT
            distributor,
            product_name,
            city,
            total_quantity,
            total_sales,
            CURRENT_TIMESTAMP AS snapshot_time
        FROM features.sales_feature;
        """,
    )

    check_model_quality >> publish_feature_store
