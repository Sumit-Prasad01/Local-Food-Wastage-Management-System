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

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="🛠 Custom SQL Query", layout="wide")
st.title("🛠 Run Custom SQL Query")

st.markdown("""
Type your own SQL query below and execute it on the **Local Food Wastage Management System** database.
⚠️ Be careful: this can **modify or delete data**!
""")

# -----------------------------
# Query Input
# -----------------------------
default_query = "SELECT name FROM sqlite_master WHERE type='table';"
sql_query = st.text_area("✍️ Enter SQL Query:", default_query, height=200)

if st.button("▶️ Run Query"):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql_query.strip())

        if sql_query.strip().lower().startswith("select"):
            # Fetch results into dataframe
            df = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
            if not df.empty:
                st.success(f"✅ Query executed successfully. Returned {len(df)} rows.")
                st.dataframe(df, use_container_width=True)
            else:
                st.info("ℹ️ Query executed but returned no results.")
        else:
            # Commit for INSERT/UPDATE/DELETE
            conn.commit()
            st.success("✅ Query executed successfully. Database updated.")

    except Exception as e:
        st.error(f"❌ SQL Error: {e}")
