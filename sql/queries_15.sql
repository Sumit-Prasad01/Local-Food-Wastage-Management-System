-- 1) Number of providers per city
SELECT City, COUNT(*) AS total_providers
FROM providers
GROUP BY City
ORDER BY total_providers DESC;

-- 2) Number of receivers per city
SELECT City, COUNT(*) AS total_receivers
FROM receivers
GROUP BY City
ORDER BY total_receivers DESC;

-- 3) Top provider types by total quantity donated
SELECT Provider_Type, SUM(Quantity) AS total_quantity
FROM food_listings
GROUP BY Provider_Type
ORDER BY total_quantity DESC;

-- 4) Provider contact details in a chosen city (example: 'New Jessica')
SELECT Name, Contact
FROM providers
WHERE City = 'New Jessica';

-- 5) Receivers with the most claims
SELECT r.Name, COUNT(*) AS total_claims
FROM claims c
JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
GROUP BY r.Name
ORDER BY total_claims DESC;

-- 6) Total available food quantity (not expired)
SELECT SUM(Quantity) AS total_available
FROM food_listings
WHERE DATE(Expiry_Date) >= DATE('now');

-- 7) City with the most food listings
SELECT Location AS City, COUNT(*) AS total_listings
FROM food_listings
GROUP BY Location
ORDER BY total_listings DESC;

-- 8) Most common food types
SELECT Food_Type, COUNT(*) AS frequency
FROM food_listings
GROUP BY Food_Type
ORDER BY frequency DESC;

-- 9) Claims count per food item
SELECT f.Food_Name, COUNT(c.Claim_ID) AS total_claims
FROM food_listings f
LEFT JOIN claims c ON f.Food_ID = c.Food_ID
GROUP BY f.Food_Name
ORDER BY total_claims DESC;

-- 10) Provider with highest completed claims
SELECT p.Name, COUNT(*) AS completed_claims
FROM claims c
JOIN food_listings f ON c.Food_ID = f.Food_ID
JOIN providers p ON f.Provider_ID = p.Provider_ID
WHERE c.Status = 'Completed'
GROUP BY p.Name
ORDER BY completed_claims DESC;

-- 11) Claim status distribution (%)
SELECT Status,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM claims), 2) AS percentage
FROM claims
GROUP BY Status;

-- 12) Average quantity claimed per receiver
SELECT r.Name, ROUND(AVG(f.Quantity), 2) AS avg_quantity
FROM claims c
JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
JOIN food_listings f ON c.Food_ID = f.Food_ID
GROUP BY r.Name
ORDER BY avg_quantity DESC;

-- 13) Most claimed meal type
SELECT f.Meal_Type, COUNT(*) AS total_claims
FROM claims c
JOIN food_listings f ON c.Food_ID = f.Food_ID
GROUP BY f.Meal_Type
ORDER BY total_claims DESC;

-- 14) Total quantity donated by each provider
SELECT p.Name, SUM(f.Quantity) AS total_quantity
FROM food_listings f
JOIN providers p ON f.Provider_ID = p.Provider_ID
GROUP BY p.Name
ORDER BY total_quantity DESC;

-- 15) Listings expiring in the next 48 hours
SELECT *
FROM food_listings
WHERE datetime(Expiry_Date) BETWEEN datetime('now') AND datetime('now', '+2 days')
ORDER BY Expiry_Date;
