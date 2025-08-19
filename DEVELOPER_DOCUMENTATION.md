# 🛠 Developer Documentation - Local Food Wastage Management System (LFWMS)

## 1. Introduction

The **Local Food Wastage Management System (LFWMS)** is designed to
reduce food wastage by connecting providers (restaurants, supermarkets,
caterers, etc.) with receivers (NGOs, shelters, individuals).\
This documentation provides a detailed technical guide for developers
who want to understand, maintain, or extend the system.

------------------------------------------------------------------------

## 2. System Architecture

The system follows a **data-driven architecture**: - **SQLite Database
(`lfwms.db`)**: Stores providers, receivers, food listings, and claims.\
- **Python Scripts (`scripts/`)**: Data cleaning, feature engineering,
and database loading.\
- **Streamlit App (`Home.py` + `pages/`)**: Provides interactive
dashboards, management pages, and analytics.\
- **Validation Pipeline**: Ensures referential integrity across datasets
before loading to SQL.

**Workflow**:

    Providers → Food Listings → Claims → Receivers → Analytics

------------------------------------------------------------------------

## 3. Database Schema & Relationships

Tables: 1. **providers**\
- `Provider_ID (PK)`, `Name`, `Type`, `Address`, `City`, `Contact`\
2. **receivers**\
- `Receiver_ID (PK)`, `Name`, `Type`, `City`, `Contact`\
3. **food_listings**\
- `Food_ID (PK)`, `Food_Name`, `Quantity`, `Expiry_Date`,
`Provider_ID (FK)`, `Food_Type`, `Meal_Type`\
4. **claims**\
- `Claim_ID (PK)`, `Food_ID (FK)`, `Receiver_ID (FK)`, `Status`,
`Timestamp`

**Key Constraints**: - `Provider_ID` in listings must exist in
providers.\
- `Receiver_ID` in claims must exist in receivers.\
- `Food_ID` in claims must exist in food_listings.

------------------------------------------------------------------------

## 4. Data Cleaning & Validation

-   Each dataset (`providers`, `receivers`, `food_listings`, `claims`)
    undergoes **cleaning & feature engineering** using pandas.\
-   A **validation pipeline** combines them and outputs:
    -   `all_data_clean_ready.csv` → valid rows for SQL import.\
    -   `data_rejects.csv` → invalid/mismatched rows for debugging.

------------------------------------------------------------------------

## 5. Streamlit Application Pages

-   **Home.py** → Project intro + KPIs (Providers, Receivers, Listings,
    Claims).\
-   **Dashboard** → Charts (claim trends, food types, provider
    contributions).\
-   **Browse Listings** → Receivers view and claim available food.\
-   **Claims Management** → Track/cancel/update claim status.\
-   **Providers Page** → View provider details + their food listings.\
-   **Analytics** → Predefined SQL insights (e.g., most active
    receivers).\
-   **Custom Query** → Run arbitrary SQL queries with results in a
    table.

------------------------------------------------------------------------

## 6. SQL Queries

-   Queries stored in `sql/queries_15.sql`.\
-   Examples:
    -   Top 5 providers by listings.\
    -   Most common food types.\
    -   Claims trend by month.\
-   `Custom Query` page allows execution of user-defined queries.

------------------------------------------------------------------------

## 7. Running the Project

1.  **Environment Setup**

    ``` bash
    pip install -r requirements.txt
    ```

2.  **Database Initialization**

    ``` bash
    sqlite3 db/lfwms.db < sql/schema.sql
    python scripts/load_to_db.py
    ```

3.  **Run Streamlit App**

    ``` bash
    streamlit run Home.py
    ```

------------------------------------------------------------------------

## 8. Future Enhancements (Developer Perspective)

-   **Add Authentication** for providers & receivers.\
-   **API Integration** to push/pull data from external systems.\
-   **Machine Learning** for food demand prediction.\
-   **Notification System** (email/SMS when new listings are
    available).\
-   **Unit Tests** for data validation & SQL queries.

------------------------------------------------------------------------

## 9. Contribution Guide

-   Fork and clone the repo.\
-   Create feature branches for new modules.\
-   Submit pull requests with proper testing.
