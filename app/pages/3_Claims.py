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

def update_claim_status(claim_id, new_status):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE claims SET Status = ?, Timestamp = ? WHERE Claim_ID = ?",
        (new_status, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), claim_id)
    )
    conn.commit()

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="📥 Manage Claims", layout="wide")
st.title("📥 Manage Claims")

st.markdown("View and manage claims made by receivers.")

# -----------------------------
# Receiver Selection (for demo)
# -----------------------------
receivers = run_query("SELECT Receiver_ID, Name FROM receivers ORDER BY Name;")
receiver_map = dict(zip(receivers["Name"], receivers["Receiver_ID"]))
selected_receiver = st.selectbox("🙋 Select Receiver", list(receiver_map.keys()))

# -----------------------------
# Filter by Claim Status
# -----------------------------
status_filter = st.selectbox("📊 Filter by Status", ["All", "Pending", "Completed", "Cancelled"])

# -----------------------------
# Fetch Claims for Receiver
# -----------------------------
query = """
    SELECT c.Claim_ID, c.Status, c.Timestamp,
           f.Food_Name, f.Quantity, f.Expiry_Date,
           f.Food_Type, f.Meal_Type, f.Location,
           p.Name as Provider_Name, p.Contact as Provider_Contact
    FROM claims c
    JOIN food_listings f ON c.Food_ID = f.Food_ID
    JOIN providers p ON f.Provider_ID = p.Provider_ID
    WHERE c.Receiver_ID = ?
"""
params = [receiver_map[selected_receiver]]

if status_filter != "All":
    query += " AND c.Status = ?"
    params.append(status_filter)

claims_df = run_query(query, tuple(params))

# -----------------------------
# Display Claims
# -----------------------------
if not claims_df.empty:
    for idx, row in claims_df.iterrows():
        with st.expander(f"📦 Claim #{row['Claim_ID']} - {row['Food_Name']} ({row['Status']})"):
            st.write(f"**Provider:** {row['Provider_Name']}")
            st.write(f"📍 Location: {row['Location']}")
            st.write(f"📞 Contact: {row['Provider_Contact']}")
            st.write(f"🥗 Food Type: {row['Food_Type']} | 🍴 Meal: {row['Meal_Type']}")
            st.write(f"⏳ Expiry: {row['Expiry_Date']}")
            st.write(f"📅 Last Updated: {row['Timestamp']}")

            if row["Status"] == "Pending":
                if st.button(f"❌ Cancel Claim #{row['Claim_ID']}", key=f"cancel_{row['Claim_ID']}"):
                    update_claim_status(row["Claim_ID"], "Cancelled")
                    st.success(f"Claim #{row['Claim_ID']} cancelled successfully!")
                    st.experimental_rerun()
else:
    st.warning("⚠️ No claims found for this receiver.")
