import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()

INPUT_FILE = "data/processed/books_clean.csv"


def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


def load_data(df):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO books (
            product_name,
            price,
            rating,
            stock_quantity,
            product_url,
            scraped_at
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (product_url)
        DO UPDATE SET
            product_name = EXCLUDED.product_name,
            price = EXCLUDED.price,
            rating = EXCLUDED.rating,
            stock_quantity = EXCLUDED.stock_quantity,
            scraped_at = EXCLUDED.scraped_at;
    """

    for _, row in df.iterrows():
        cursor.execute(
            query,
            (
                row["product_name"],
                row["price"],
                row["rating"],
                row["stock_quantity"],
                row["product_url"],
                row["scraped_at"],
            ),
        )

    conn.commit()

    cursor.close()
    conn.close()


def main():
    df = pd.read_csv(INPUT_FILE)

    print(f"Rows to load: {len(df)}")

    load_data(df)

    print("Data successfully loaded to Supabase PostgreSQL.")


if __name__ == "__main__":
    main()