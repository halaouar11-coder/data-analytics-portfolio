
-- 1. View a sample of sales records
SELECT *
FROM sales_analyzed
LIMIT 10;


-- 2. Overall business KPIs
SELECT
    COUNT(DISTINCT OrderID) AS TotalOrders,
    SUM(Quantity) AS UnitsSold,
    ROUND(SUM(Revenue), 2) AS TotalRevenue,
    ROUND(SUM(TotalCost), 2) AS TotalCost,
    ROUND(SUM(Profit), 2) AS TotalProfit,
    ROUND(
        100.0 * SUM(Profit) / NULLIF(SUM(Revenue), 0),
        2
    ) AS ProfitMarginPercent
FROM sales_analyzed;


-- 3. Performance by product
SELECT
    Product,
    SUM(Quantity) AS UnitsSold,
    ROUND(SUM(Revenue), 2) AS Revenue,
    ROUND(SUM(Profit), 2) AS Profit
FROM sales_analyzed
GROUP BY Product
ORDER BY Revenue DESC;


-- 4. Performance by region
SELECT
    Region,
    COUNT(DISTINCT OrderID) AS TotalOrders,
    ROUND(SUM(Revenue), 2) AS Revenue,
    ROUND(SUM(Profit), 2) AS Profit
FROM sales_analyzed
GROUP BY Region
ORDER BY Revenue DESC;


-- 5. Monthly sales trend
SELECT
    Month,
    ROUND(SUM(Revenue), 2) AS Revenue,
    ROUND(SUM(Profit), 2) AS Profit
FROM sales_analyzed
GROUP BY Month
ORDER BY Month;


-- 6. Products generating more than 100000 MAD in revenue
SELECT
    Product,
    ROUND(SUM(Revenue), 2) AS Revenue
FROM sales_analyzed
GROUP BY Product
HAVING SUM(Revenue) > 100000
ORDER BY Revenue DESC;
