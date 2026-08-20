-- =======================================================
-- Financial Analytics Schema & Decision Intelligence Queries
-- Deliverable for Task 4: Financial Analytics Dashboard
-- =======================================================

-- 1. Create Financial Transactions Table
CREATE TABLE IF NOT EXISTS Financial_Transactions (
    TransactionID VARCHAR(20) PRIMARY KEY,
    TransactionDate DATE,
    BusinessUnit VARCHAR(50),
    Region VARCHAR(30),
    ExpenseCategory VARCHAR(50),
    Revenue DECIMAL(12,2),
    COGS DECIMAL(12,2),
    OperatingExpenses DECIMAL(12,2),
    GrossProfit DECIMAL(12,2),
    OperatingProfit_EBIT DECIMAL(12,2),
    NetProfit DECIMAL(12,2),
    OperatingCashFlow DECIMAL(12,2)
);

-- 2. Executive Financial KPI Summary
SELECT 
    ROUND(SUM(Revenue), 2) AS Total_Revenue,
    ROUND(SUM(COGS), 2) AS Total_COGS,
    ROUND(SUM(OperatingExpenses), 2) AS Total_Operating_Expenses,
    ROUND(SUM(GrossProfit), 2) AS Total_Gross_Profit,
    ROUND((SUM(GrossProfit) / SUM(Revenue)) * 100, 2) AS Gross_Profit_Margin_Pct,
    ROUND(SUM(NetProfit), 2) AS Total_Net_Income,
    ROUND((SUM(NetProfit) / SUM(Revenue)) * 100, 2) AS Net_Profit_Margin_Pct,
    ROUND(SUM(OperatingCashFlow), 2) AS Total_Operating_Cash_Flow
FROM Financial_Transactions;

-- 3. Revenue, Profitability & Margins by Business Unit
SELECT 
    BusinessUnit,
    COUNT(TransactionID) AS Transaction_Count,
    ROUND(SUM(Revenue), 2) AS Total_Revenue,
    ROUND(SUM(GrossProfit), 2) AS Gross_Profit,
    ROUND(SUM(NetProfit), 2) AS Net_Profit,
    ROUND((SUM(NetProfit) / SUM(Revenue)) * 100, 2) AS Net_Margin_Percentage,
    ROUND(SUM(OperatingCashFlow), 2) AS Total_Cash_Flow
FROM Financial_Transactions
GROUP BY BusinessUnit
ORDER BY Total_Revenue DESC;

-- 4. Regional Profitability & Expense Breakdown
SELECT 
    Region,
    ROUND(SUM(Revenue), 2) AS Total_Revenue,
    ROUND(SUM(OperatingExpenses), 2) AS Total_OpEx,
    ROUND(SUM(NetProfit), 2) AS Net_Profit,
    ROUND((SUM(NetProfit) / SUM(Revenue)) * 100, 2) AS Net_Profit_Margin_Pct
FROM Financial_Transactions
GROUP BY Region
ORDER BY Net_Profit DESC;

-- 5. Monthly Revenue and Net Profit Trend
SELECT 
    DATE_FORMAT(TransactionDate, '%Y-%m') AS Financial_Month,
    ROUND(SUM(Revenue), 2) AS Monthly_Revenue,
    ROUND(SUM(OperatingExpenses), 2) AS Monthly_OpEx,
    ROUND(SUM(NetProfit), 2) AS Monthly_Net_Profit,
    ROUND(SUM(OperatingCashFlow), 2) AS Monthly_Cash_Flow
FROM Financial_Transactions
GROUP BY DATE_FORMAT(TransactionDate, '%Y-%m')
ORDER BY Financial_Month ASC;