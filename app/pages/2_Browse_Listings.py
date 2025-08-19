import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

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

def insert_claim(food_id, receiver_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO claims (Food_ID, Receiver_ID, Status, Timestamp) VALUES (?, ?, ?, ?)",
        (food_id, receiver_id, "Pending", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="🍽 Browse Listings", layout="wide")
st.title("🍽 Browse Food Listings")

st.markdown("Filter and explore available food items from providers, and claim surplus food.")

# -----------------------------
# Filters
# -----------------------------
cities = run_query("SELECT DISTINCT Location FROM food_listings ORDER BY Location;")["Location"].tolist()
food_types = run_query("SELECT DISTINCT Food_Type FROM food_listings ORDER BY Food_Type;")["Food_Type"].tolist()
meal_types = run_query("SELECT DISTINCT Meal_Type FROM food_listings ORDER BY Meal_Type;")["Meal_Type"].tolist()

col1, col2, col3 = st.columns(3)

with col1:
    selected_city = st.selectbox("🏙 Select City", ["All"] + cities)

with col2:
    selected_food_type = st.selectbox("🥗 Select Food Type", ["All"] + food_types)

with col3:
    selected_meal_type = st.selectbox("🍴 Select Meal Type", ["All"] + meal_types)

# -----------------------------
# Receiver Dropdown (demo purpose)
# -----------------------------
receivers = run_query("SELECT Receiver_ID, Name FROM receivers ORDER BY Name;")
receiver_map = dict(zip(receivers["Name"], receivers["Receiver_ID"]))
selected_receiver = st.selectbox("🙋 Select Receiver", list(receiver_map.keys()))

# -----------------------------
# Query with Filters
# -----------------------------
query = """
    SELECT f.Food_ID, f.Food_Name, f.Quantity, f.Expiry_Date,
           f.Food_Type, f.Meal_Type, f.Location,
           p.Name as Provider_Name, p.Type as Provider_Type, p.Contact as Provider_Contact
    FROM food_listings f
    JOIN providers p ON f.Provider_ID = p.Provider_ID
    WHERE 1=1
"""
params = []

if selected_city != "All":
    query += " AND f.Location = ?"
    params.append(selected_city)

if selected_food_type != "All":
    query += " AND f.Food_Type = ?"
    params.append(selected_food_type)

if selected_meal_type != "All":
    query += " AND f.Meal_Type = ?"
    params.append(selected_meal_type)

df = run_query(query, tuple(params))

# -----------------------------
# Display Results with Claim Buttons
# -----------------------------
if not df.empty:
    for idx, row in df.iterrows():
        with st.expander(f"🍴 {row['Food_Name']} ({row['Quantity']}) - {row['Location']}"):
            st.write(f"**Provider:** {row['Provider_Name']} ({row['Provider_Type']})")
            st.write(f"📍 Location: {row['Location']}")
            st.write(f"📞 Contact: {row['Provider_Contact']}")
            st.write(f"🥗 Type: {row['Food_Type']} | 🍴 Meal: {row['Meal_Type']}")
            st.write(f"⏳ Expiry: {row['Expiry_Date']}")
            
            if st.button(f"✅ Claim this item (ID {row['Food_ID']})", key=f"claim_{row['Food_ID']}"):
                insert_claim(row["Food_ID"], receiver_map[selected_receiver])
                st.success(f"Claim placed successfully for {row['Food_Name']} by {selected_receiver}!")
else:
    st.warning("⚠️ No food listings match your filters.")
