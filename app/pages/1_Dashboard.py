import streamlit as st
import sqlite3
import pandas as pd
import altair as alt

# -----------------------------
# DB Connection
# -----------------------------
@st.cache_resource
def get_connection(db_path="../db/lfwms.db"):
    conn = sqlite3.connect(db_path, check_same_thread=False)
    return conn

def run_query(query):
    conn = get_connection()
    return pd.read_sql(query, conn)

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="📊 Dashboard", layout="wide")
st.title("📊 Dashboard & Analytics")

st.markdown("This dashboard gives an overview of **food availability, claims, and provider activity** in the system.")

# -----------------------------
# 1. Claim Status Distribution
# -----------------------------
st.subheader("✅ Claim Status Distribution")

status_df = run_query("""
    SELECT Status, COUNT(*) as total
    FROM claims
    GROUP BY Status
""")

if not status_df.empty:
    pie_chart = alt.Chart(status_df).mark_arc().encode(
        theta="total",
        color="Status",
        tooltip=["Status", "total"]
    )
    st.altair_chart(pie_chart, use_container_width=True)
else:
    st.info("No claim data available.")

# -----------------------------
# 2. Food Listings by Type
# -----------------------------
st.subheader("🍴 Food Listings by Type")

food_df = run_query("""
    SELECT Food_Type, COUNT(*) as total
    FROM food_listings
    GROUP BY Food_Type
""")

if not food_df.empty:
    bar_chart = alt.Chart(food_df).mark_bar().encode(
        x="Food_Type",
        y="total",
        color="Food_Type",
        tooltip=["Food_Type", "total"]
    )
    st.altair_chart(bar_chart, use_container_width=True)
else:
    st.info("No food listing data available.")

# -----------------------------
# 3. Top Cities by Listings
# -----------------------------
st.subheader("🏬 Top Cities by Food Listings")

city_df = run_query("""
    SELECT Location as City, COUNT(*) as total
    FROM food_listings
    GROUP BY Location
    ORDER BY total DESC
    LIMIT 10
""")

if not city_df.empty:
    city_chart = alt.Chart(city_df).mark_bar().encode(
        x=alt.X("total", title="Number of Listings"),
        y=alt.Y("City", sort="-x"),
        color="City",
        tooltip=["City", "total"]
    )
    st.altair_chart(city_chart, use_container_width=True)
else:
    st.info("No city listing data available.")

# -----------------------------
# 4. Claims Trend by Day
# -----------------------------
st.subheader("📈 Claims Trend Over Time")

claims_trend = run_query("""
    SELECT DATE(Timestamp) as claim_date, COUNT(*) as total
    FROM claims
    GROUP BY claim_date
    ORDER BY claim_date
""")

if not claims_trend.empty:
    trend_chart = alt.Chart(claims_trend).mark_line(point=True).encode(
        x="claim_date:T",
        y="total:Q",
        tooltip=["claim_date", "total"]
    )
    st.altair_chart(trend_chart, use_container_width=True)
else:
    st.info("No claims trend data available.")
