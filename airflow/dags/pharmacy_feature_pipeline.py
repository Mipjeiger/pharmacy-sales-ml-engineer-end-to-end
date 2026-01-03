from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime, timedelta

# from plugins.slack_utils import slack_alert  # Comment out if slack_utils not available

default_args = {
    "owner": "ml-engineer",
    # "on_failure_callback": slack_alert,  # Comment out if slack_utils not available
}

with DAG(
    dag_id="pharmacy_feature_pipeline",
    start_date=datetime(2025, 1, 1),
    default_args=default_args,
    catchup=False,
    schedule=None,
    tags=["pharmacy", "features"],
) as dag:

    check_raw_data = SQLExecuteQueryOperator(
        task_id="check_raw_pharmacy_sales",
        conn_id="pharmacy_db",
        sql="""
        SELECT COUNT(*) FROM raw.pharmacy_sales WHERE sales IS NULL OR quantity < 0;
        """,
    )

    refresh_sales_feature = SQLExecuteQueryOperator(
        task_id="refresh_pharmacy_sales_features",
        conn_id="pharmacy_db",
        sql="""
        DELETE FROM features.sales_feature WHEN year = EXTRACT(YEAR FROM CURRENT_DATE)
            AND month = EXTRACT(MONTH FROM CURRENT_DATE);

        INSERT INTO features.sales_feature
        SELECT
            distributor,
            channel,
            sub_channel,
            city,
            product_name,
            product_class,
            sales_team,
            year,
            month,
            SUM(quantity) AS total_quantity,
            AVG(price) AS avg_price,
            SUM(sales) AS total_sales
        FROM raw.pharmacy_sales
        GROUP BY 1,2,3,4,5,6,7,8,9;
        """,
    )

    refresh_llm_context = SQLExecuteQueryOperator(
        task_id="refresh_sales_llm_context",
        conn_id="pharmacy_db",
        sql="""
        INSERT INTO features.sales_llm_context
        SELECT * FROM features.sales_feature
        WHERE month = EXTRACT(MONTH FROM CURRENT_DATE);""",
    )

    check_raw_data >> refresh_sales_feature >> refresh_llm_context
