import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

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
st.set_page_config(page_title="📊 Analytics", layout="wide")
st.title("📊 Analytics & Insights")

st.markdown("Data-driven insights from providers, receivers, listings, and claims.")

# -----------------------------
# Claims by Status
# -----------------------------
st.subheader("📦 Claims by Status")
status_df = run_query("SELECT Status, COUNT(*) as count FROM claims GROUP BY Status;")

if not status_df.empty:
    fig, ax = plt.subplots()
    ax.pie(status_df["count"], labels=status_df["Status"], autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    st.pyplot(fig)
else:
    st.warning("⚠️ No claim data available.")

# -----------------------------
# Top Providers by Claims
# -----------------------------
st.subheader("🏬 Top Providers by Claims")
providers_df = run_query("""
    SELECT p.Name as Provider, COUNT(c.Claim_ID) as Total_Claims
    FROM providers p
    JOIN food_listings f ON p.Provider_ID = f.Provider_ID
    JOIN claims c ON f.Food_ID = c.Food_ID
    GROUP BY p.Name
    ORDER BY Total_Claims DESC
    LIMIT 5;
""")

if not providers_df.empty:
    st.bar_chart(providers_df.set_index("Provider"))
else:
    st.info("ℹ️ No claims available to rank providers.")

# -----------------------------
# Popular Food Types
# -----------------------------
st.subheader("🥗 Popular Food Types (by Claims)")
food_types_df = run_query("""
    SELECT f.Food_Type, COUNT(c.Claim_ID) as Total_Claims
    FROM food_listings f
    JOIN claims c ON f.Food_ID = c.Food_ID
    GROUP BY f.Food_Type
    ORDER BY Total_Claims DESC;
""")

if not food_types_df.empty:
    st.bar_chart(food_types_df.set_index("Food_Type"))
else:
    st.info("ℹ️ No claims available to analyze food types.")

# -----------------------------
# Claims Trend by Weekday/Hour
# -----------------------------
st.subheader("⏰ Claims Trend by Weekday & Hour")

trend_df = run_query("""
    SELECT 
        strftime('%w', Timestamp) as Weekday,
        strftime('%H', Timestamp) as Hour,
        COUNT(*) as Total_Claims
    FROM claims
    GROUP BY Weekday, Hour
    ORDER BY Weekday, Hour;
""")

if not trend_df.empty:
    trend_df["Weekday"] = trend_df["Weekday"].astype(int)
    weekday_map = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    trend_df["Weekday"] = trend_df["Weekday"].map(lambda x: weekday_map[x])

    pivot_df = trend_df.pivot(index="Hour", columns="Weekday", values="Total_Claims").fillna(0)

    st.line_chart(pivot_df)
else:
    st.info("ℹ️ No timestamped claim data available.")
