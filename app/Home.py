import streamlit as st
import sqlite3

# -----------------------------
# Database connection function
# -----------------------------
@st.cache_resource
def get_connection(db_path="../db/lfwms.db"):
    conn = sqlite3.connect(db_path, check_same_thread=False)
    return conn

# -----------------------------
# Query helper
# -----------------------------
def run_query(query, params=()):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()
    return rows

# -----------------------------
# Streamlit App Home
# -----------------------------
st.set_page_config(page_title="Local Food Wastage Management System", layout="wide")

st.title("🥗 Local Food Wastage Management System")
st.markdown(
    """
    Welcome to the **Local Food Wastage Management System (LFWMS)**.  
    This platform connects **food providers** (restaurants, supermarkets, caterers)  
    with **receivers** (NGOs, shelters, individuals) to **minimize food waste**  
    and distribute surplus food effectively.  

    ---
    """
)

# -----------------------------
# KPIs Section
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_providers = run_query("SELECT COUNT(*) FROM providers;")[0][0]
    st.metric("Providers", total_providers)

with col2:
    total_receivers = run_query("SELECT COUNT(*) FROM receivers;")[0][0]
    st.metric("Receivers", total_receivers)

with col3:
    total_food = run_query("SELECT COUNT(*) FROM food_listings;")[0][0]
    st.metric("Food Listings", total_food)

with col4:
    total_claims = run_query("SELECT COUNT(*) FROM claims;")[0][0]
    st.metric("Claims", total_claims)

# -----------------------------
# Footer / Info
# -----------------------------
st.markdown(
    """
    ---
    ✅ Navigate using the sidebar to explore:  
    - 📊 Dashboard (Analytics & Charts)  
    - 🍽 Browse Food Listings  
    - 📥 Manage Claims  
    - 🏬 Providers Management  
    - 📈 Analytics (SQL Insights)  
    """
)
