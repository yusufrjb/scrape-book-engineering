import pandas as pd

INPUT_FILE = "data/processed/books_clean.csv"


def validate_data(df):

    errors = []

    # 1. Check required columns
    required_columns = [
        "product_name",
        "price",
        "rating",
        "stock_quantity",
        "product_url",
        "scraped_at",
    ]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        errors.append(
            f"Missing columns: {missing_columns}"
        )

    # 2. Check null values
    null_counts = df[required_columns].isna().sum()

    for column, count in null_counts.items():
        if count > 0:
            errors.append(
                f"{column} contains {count} null values"
            )

    # 3. Check duplicate product URLs
    duplicate_urls = df["product_url"].duplicated().sum()

    if duplicate_urls > 0:
        errors.append(
            f"Found {duplicate_urls} duplicate product URLs"
        )

    # 4. Check price
    invalid_price = (df["price"] <= 0).sum()

    if invalid_price > 0:
        errors.append(
            f"Found {invalid_price} invalid prices"
        )

    # 5. Check rating
    invalid_rating = (
        ~df["rating"].between(1, 5)
    ).sum()

    if invalid_rating > 0:
        errors.append(
            f"Found {invalid_rating} invalid ratings"
        )

    # 6. Check stock quantity
    invalid_stock = (
        df["stock_quantity"] < 0
    ).sum()

    if invalid_stock > 0:
        errors.append(
            f"Found {invalid_stock} invalid stock quantities"
        )

    return errors


def main():

    df = pd.read_csv(INPUT_FILE)

    print("=== DATA QUALITY CHECK ===")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")

    errors = validate_data(df)

    print("\n=== RESULT ===")

    if errors:
        print("FAILED")

        for error in errors:
            print(f"- {error}")

    else:
        print("PASSED")
        print("All data quality checks passed.")


if __name__ == "__main__":
    main()