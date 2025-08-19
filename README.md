# 🍽 Local Food Wastage Management System (LFWMS)

## 📌 Project Overview

The **Local Food Wastage Management System (LFWMS)** is a
database-driven platform that connects **food providers** (restaurants,
supermarkets, grocery stores, etc.) with **receivers** (NGOs, shelters,
individuals) to minimize food wastage and distribute surplus food
efficiently.

Built with **SQLite + Streamlit**, the system allows users to manage
food listings, make and track claims, and generate insights through
dashboards and analytics.

------------------------------------------------------------------------

## 🚀 Features

-   🏠 **Home Page** → Overview with KPIs.\
-   📊 **Dashboard** → Data visualizations (claims, food, providers).\
-   🍽 **Browse Listings** → Receivers can browse available food and
    claim it.\
-   📥 **Claims Management** → Receivers manage their claims (cancel,
    track status).\
-   🏬 **Providers Page** → View provider details, listings, and claim
    history.\
-   📈 **Analytics** → SQL-powered insights (trends, food types, top
    providers).\
-   🛠 **Custom Query Tool** → Admins can run SQL queries directly.

------------------------------------------------------------------------

## 🗄 Database Schema

The system uses an **SQLite database (`lfwms.db`)** with the following
tables:

-   **providers** → Provider details (name, type, city, contact).\
-   **receivers** → Receiver details (name, type, city, contact).\
-   **food_listings** → Available food items with expiry dates and meal
    types.\
-   **claims** → Track requests made by receivers for food listings.

------------------------------------------------------------------------

## 🏗 Tech Stack

-   **Frontend:** Streamlit\
-   **Backend/Database:** SQLite\
-   **Language:** Python (pandas, matplotlib, streamlit, sqlite3)

------------------------------------------------------------------------

## ▶️ Running the Project

1.  Clone the repo and install requirements:

    ``` bash
    pip install -r requirements.txt
    ```

2.  Set up the database:

    ``` bash
    sqlite3 db/lfwms.db < sql/schema.sql
    python scripts/load_to_db.py
    ```

3.  Run the Streamlit app:

    ``` bash
    streamlit run Home.py
    ```

------------------------------------------------------------------------

## 📂 File Structure

    📦 Local Food Wastage Management System
     ┣ 📂 db               # SQLite database
     ┣ 📂 sql              # Schema & query files
     ┣ 📂 scripts          # Data cleaning + load scripts
     ┣ 📂 pages            # Streamlit pages (Dashboard, Claims, Providers, etc.)
     ┣ 📜 Home.py          # Main Streamlit home page
     ┣ 📜 requirements.txt # Python dependencies
     ┣ 📜 README.md        # Project documentation

------------------------------------------------------------------------

## ✨ Future Improvements

-   🤖 Machine learning to predict demand & optimize food allocation.\
-   📱 Mobile-friendly UI.\
-   🔔 Notification system for new listings.

------------------------------------------------------------------------

## 👨‍💻 Author

Developed as part of a project on **Food Waste Management Systems**.

