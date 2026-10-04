import pandas as pd

INPUT_FILE = "data/raw/books.csv"

df = pd.read_csv(INPUT_FILE)

print("=== SHAPE ===")
print(df.shape)

print("\n=== COLUMNS ===")
print(df.columns.tolist())

print("\n=== DATA TYPES ===")
print(df.dtypes)

print("\n=== MISSING VALUES ===")
print(df.isna().sum())

print("\n=== DUPLICATES ===")
print(df.duplicated().sum())

print("\n=== SAMPLE ===")
print(df.head())