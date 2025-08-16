import pandas as pd
from sqlalchemy import create_engine

# Database connection (SQLite)
engine = create_engine("sqlite:///lfwms.db", echo=False)

# Expected schemas
expected_columns = {
    "providers": [
        "Provider_ID", "Name", "Type", "Address", "City", "Contact"
    ],
    "receivers": [
        "Receiver_ID", "Name", "Type", "City", "Contact"
    ],
    "food_listings": [
        "Food_ID", "Food_Name", "Quantity", "Expiry_Date", "Provider_ID",
        "Provider_Type", "Location", "Food_Type", "Meal_Type"
    ],
    "claims": [
        "Claim_ID", "Food_ID", "Receiver_ID", "Status", "Timestamp"
    ]
}

# File mapping
file_map = {
    "providers": "data/processed/providers_data_clean.csv",
    "receivers": "data/processed/receivers_data_clean.csv",
    "food_listings": "data/processed/food_listings_data_clean.csv",
    "claims": "data/processed/claims_data_clean.csv"
}

# Function to validate dataframe columns
def validate_dataframe(df, table_name):
    missing = set(expected_columns[table_name]) - set(df.columns)
    extra = set(df.columns) - set(expected_columns[table_name])
    if missing:
        raise ValueError(
            f"{table_name} is missing required columns: {missing}"
        )
    if extra:
        print(f"{table_name} has extra columns (will be ignored): {extra}")
        # Drop extras so schema stays clean
        df = df[expected_columns[table_name]]
    return df

# Load and validate all datasets
dataframes = {}
for table, file in file_map.items():
    print(f"Loading {file} into {table}...")
    df = pd.read_csv(file)
    df = validate_dataframe(df, table)
    dataframes[table] = df

# Write to SQLite database
for table, df in dataframes.items():
    df.to_sql(table, engine, if_exists="replace", index=False)
    print(f"{table} table loaded successfully ({len(df)} rows).")

print("\n All cleaned datasets validated and loaded into lfwms.db")
