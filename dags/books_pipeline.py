from datetime import datetime

from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator


with DAG(
    dag_id="books_pipeline",
    start_date=datetime(2026, 10, 4),
    schedule=None,
    catchup=False,
    tags=["data-engineering", "books"],
) as dag:

    scrape = BashOperator(
        task_id="scrape_books",
        bash_command="cd /opt/airflow && python src/scraper/scrape_books.py",
    )

    transform = BashOperator(
        task_id="transform_books",
        bash_command="cd /opt/airflow && python src/transformation/transform_books.py",
    )

    validate = BashOperator(
        task_id="validate_books",
        bash_command="cd /opt/airflow && python src/validation/validate_books.py",
    )

    load = BashOperator(
        task_id="load_books",
        bash_command="cd /opt/airflow && python src/loader/load_books.py",
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="cd /opt/airflow/dbt_books && dbt run",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="cd /opt/airflow/dbt_books && dbt test",
    )

    scrape >> transform >> validate >> load >> dbt_run >> dbt_test

