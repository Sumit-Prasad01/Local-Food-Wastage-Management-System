-- Providers Table
CREATE TABLE providers (
    Provider_ID   INTEGER PRIMARY KEY,
    Name          TEXT NOT NULL,
    Type          TEXT,
    Address       TEXT,
    City          TEXT,
    Contact       TEXT
);

-- Receivers Table
CREATE TABLE receivers (
    Receiver_ID   INTEGER PRIMARY KEY,
    Name          TEXT NOT NULL,
    Type          TEXT,
    City          TEXT,
    Contact       TEXT
);

-- Food Listings Table
CREATE TABLE food_listings (
    Food_ID       INTEGER PRIMARY KEY,
    Food_Name     TEXT NOT NULL,
    Quantity      INTEGER CHECK (Quantity >= 0),
    Expiry_Date   DATE NOT NULL,
    Provider_ID   INTEGER NOT NULL,
    Provider_Type TEXT,
    Location      TEXT,
    Food_Type     TEXT,
    Meal_Type     TEXT,
    FOREIGN KEY (Provider_ID) REFERENCES providers(Provider_ID) ON DELETE CASCADE
);

-- Claims Table
CREATE TABLE claims (
    Claim_ID      INTEGER PRIMARY KEY,
    Food_ID       INTEGER NOT NULL,
    Receiver_ID   INTEGER NOT NULL,
    Status        TEXT CHECK(Status IN ('Pending', 'Completed', 'Cancelled')),
    Timestamp     DATETIME NOT NULL,
    FOREIGN KEY (Food_ID) REFERENCES food_listings(Food_ID) ON DELETE CASCADE,
    FOREIGN KEY (Receiver_ID) REFERENCES receivers(Receiver_ID) ON DELETE CASCADE
);
