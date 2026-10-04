import pandas as pd
from pathlib import Path

INPUT_FILE = "data/raw/books.csv"
OUTPUT_FILE = Path("data/processed/books_clean.csv")


def transform_data(df):

    # Price: "Â£51.77" -> 51.77
    df["price"] = (
        df["price"]
        .str.replace(r"[^\d.]", "", regex=True)
        .astype(float)
    )

    # Rating: "Three" -> 3
    rating_mapping = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5,
    }

    df["rating"] = df["rating"].map(rating_mapping)

    # Stock quantity -> integer
    df["stock_quantity"] = pd.to_numeric(
        df["stock_quantity"],
        errors="coerce"
    ).astype("Int64")

    # Remove duplicate products
    df = df.drop_duplicates(subset=["product_url"])

    # Data validation
    df = df[df["product_name"].notna()]
    df = df[df["price"] > 0]
    df = df[df["rating"].between(1, 5)]
    df = df[df["stock_quantity"] >= 0]

    return df


def main():

    df = pd.read_csv(INPUT_FILE)

    print("Before transformation:")
    print(df.shape)

    df = transform_data(df)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(OUTPUT_FILE, index=False)

    print("\nAfter transformation:")
    print(df.shape)

    print("\nData types:")
    print(df.dtypes)

    print("\nSample:")
    print(df.head())

    print(f"\nSaved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()