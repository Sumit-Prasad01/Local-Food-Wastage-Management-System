import pandas as pd

# Load Datasets
providers = pd.read_csv("data/processed/providers_data_clean.csv")
receivers = pd.read_csv("data/processed/receivers_data_clean.csv")
listings = pd.read_csv("data/processed/food_listings_data_clean.csv")
claims = pd.read_csv("data/processed/claims_data_clean.csv")

# Referential Intergrity checks
## Listings must have valid Provider_ID

valid_listings = listings[listings['Provider_ID'].isin(providers['Provider_ID'])]
invalid_listings = listings[~listings['Provider_ID'].isin(providers['Provider_ID'])]

## Claims must have valid Food_ID and Receiver_ID
valid_claims = claims[
                    claims['Food_ID'].isin(valid_listings['Food_ID'])&
                    claims["Receiver_ID"].isin(receivers["Receiver_ID"])
                    ]

invalid_claims = claims[ 
                    ~claims['Food_ID'].isin(valid_listings['Food_ID'])&
                    ~claims["Receiver_ID"].isin(receivers["Receiver_ID"])
                    ]

# Build Clean Master Dataset
## Merge Listings with  providers

listings_with_providers = valid_listings.merge(
    providers, on='Provider_ID', how='left', suffixes = ("", "_Providers")
)

# Merge claims with listings and receivers
claims_with_all = valid_claims.merge(
    listings_with_providers, on="Food_ID", how="left", suffixes=("", "_Listing")
).merge(
    receivers, on="Receiver_ID", how="left", suffixes=("", "_Receiver")
)

# Save Outputs
claims_with_all.to_csv("data/Merged/all_data_clean_ready.csv", index=False)

# Collect rejects into one file
rejects = pd.concat([invalid_listings.assign(Issue="Invalid Provider_ID in Listings"),
                     invalid_claims.assign(Issue="Invalid Food_ID or Receiver_ID in Claims")])

rejects.to_csv("data/Merged/data_rejects.csv", index=False)

print("Referential integrity check complete.")
print(f"Clean dataset saved as all_data_clean_ready.csv with {len(claims_with_all)} rows.")
print(f"Rejected records saved as data_rejects.csv with {len(rejects)} rows.")