import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def main():
    print("Testing database connection...")

    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

    cursor = conn.cursor()

    cursor.execute("SELECT version();")
    version = cursor.fetchone()

    print("Connection successful!")
    print(f"PostgreSQL version: {version[0]}")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()