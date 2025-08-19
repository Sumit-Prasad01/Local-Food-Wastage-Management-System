import streamlit as st
import sqlite3
import pandas as pd

# -----------------------------
# DB Connection
# -----------------------------
@st.cache_resource
def get_connection(db_path="../db/lfwms.db"):
    conn = sqlite3.connect(db_path, check_same_thread=False)
    return conn

def run_query(query, params=()):
    conn = get_connection()
    return pd.read_sql(query, conn, params=params)

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="🏬 Providers Management", layout="wide")
st.title("🏬 Providers Management")

st.markdown("Browse provider details, their food listings, and related claims.")

# -----------------------------
# Providers List
# -----------------------------
providers = run_query("SELECT Provider_ID, Name, Type, City, Contact FROM providers ORDER BY Name;")

provider_map = dict(zip(providers["Name"], providers["Provider_ID"]))
selected_provider = st.selectbox("🏬 Select Provider", list(provider_map.keys()))

provider_id = provider_map[selected_provider]
provider_details = providers[providers["Provider_ID"] == provider_id].iloc[0]

# -----------------------------
# Show Provider Details
# -----------------------------
st.subheader(f"📋 Details for {provider_details['Name']}")
st.write(f"**Type:** {provider_details['Type']}")
st.write(f"**City:** {provider_details['City']}")
st.write(f"**Contact:** {provider_details['Contact']}")

# -----------------------------
# Provider Listings
# -----------------------------
st.markdown("### 🍽 Food Listings")
listings_query = """
    SELECT Food_ID, Food_Name, Quantity, Expiry_Date, Food_Type, Meal_Type, Location
    FROM food_listings
    WHERE Provider_ID = ?
"""
listings = run_query(listings_query, (provider_id,))

if not listings.empty:
    st.dataframe(listings, use_container_width=True)
else:
    st.warning("⚠️ This provider has no active listings.")

# -----------------------------
# Claims on Provider’s Listings
# -----------------------------
st.markdown("### 📦 Claims on Listings")
claims_query = """
    SELECT c.Claim_ID, c.Status, c.Timestamp,
           f.Food_Name, f.Quantity, f.Expiry_Date,
           r.Name as Receiver_Name, r.Type as Receiver_Type
    FROM claims c
    JOIN food_listings f ON c.Food_ID = f.Food_ID
    JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
    WHERE f.Provider_ID = ?
    ORDER BY c.Timestamp DESC
"""
claims = run_query(claims_query, (provider_id,))

if not claims.empty:
    st.dataframe(claims, use_container_width=True)
else:
    st.info("ℹ️ No claims have been made for this provider’s listings yet.")
