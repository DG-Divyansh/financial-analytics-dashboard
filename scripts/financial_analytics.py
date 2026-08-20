import os
import numpy as np
import pandas as pd

def generate_financial_data(num_records=1200):
    """Generates monthly corporate financial transactions across departments and business units."""
    np.random.seed(42)
    
    date_range = pd.date_range(start="2024-01-01", end="2025-12-31", freq="D")
    business_units = ['Enterprise Solutions', 'Cloud Services', 'Consumer Hardware', 'SaaS Subscriptions', 'Consulting']
    regions = ['North America', 'EMEA', 'APAC', 'LATAM']
    expense_categories = ['R&D', 'Sales & Marketing', 'COGS', 'Administrative', 'Operations']
    
    dates = np.random.choice(date_range, size=num_records)
    revenue = np.random.uniform(50000, 350000, size=num_records)
    cogs_ratio = np.random.uniform(0.30, 0.55, size=num_records)
    cogs = revenue * cogs_ratio
    opex_ratio = np.random.uniform(0.20, 0.35, size=num_records)
    opex = revenue * opex_ratio
    tax_rate = 0.21
    
    data = {
        'TransactionID': [f'TXN{20000 + i}' for i in range(num_records)],
        'Date': pd.to_datetime(dates),
        'BusinessUnit': np.random.choice(business_units, size=num_records),
        'Region': np.random.choice(regions, size=num_records),
        'ExpenseCategory': np.random.choice(expense_categories, size=num_records),
        'Revenue': np.round(revenue, 2),
        'COGS': np.round(cogs, 2),
        'OperatingExpenses': np.round(opex, 2),
        'Receivables': np.round(revenue * np.random.uniform(0.05, 0.20, size=num_records), 2),
        'Payables': np.round(opex * np.random.uniform(0.05, 0.15, size=num_records), 2),
        'TaxRate': tax_rate
    }
    
    df = pd.DataFrame(data)
    
    # Introduce random missing values for data cleaning demonstration
    df.loc[df.sample(frac=0.015, random_state=42).index, 'OperatingExpenses'] = np.nan
    return df

def clean_financial_data(df):
    """Cleans missing data, removes duplicates, and derives primary financial KPIs."""
    # Impute missing OpEx by median within the same ExpenseCategory
    df['OperatingExpenses'] = df.groupby('ExpenseCategory')['OperatingExpenses'].transform(lambda x: x.fillna(x.median()))
    
    # Deduplicate
    df.drop_duplicates(subset=['TransactionID'], inplace=True)
    
    # Derived Financial Metrics
    df['GrossProfit'] = np.round(df['Revenue'] - df['COGS'], 2)
    df['OperatingProfit_EBIT'] = np.round(df['GrossProfit'] - df['OperatingExpenses'], 2)
    df['TaxAmount'] = np.round(np.where(df['OperatingProfit_EBIT'] > 0, df['OperatingProfit_EBIT'] * df['TaxRate'], 0), 2)
    df['NetProfit'] = np.round(df['OperatingProfit_EBIT'] - df['TaxAmount'], 2)
    
    # Margins (%)
    df['GrossMargin_%'] = np.round((df['GrossProfit'] / df['Revenue']) * 100, 2)
    df['NetMargin_%'] = np.round((df['NetProfit'] / df['Revenue']) * 100, 2)
    
    # Estimated Operating Cash Flow (Net Profit + Working Capital Delta)
    df['OperatingCashFlow'] = np.round(df['NetProfit'] + df['Payables'] - df['Receivables'], 2)
    
    # Date hierarchy helpers
    df['Year'] = df['Date'].dt.year
    df['YearMonth'] = df['Date'].dt.to_period('M').astype(str)
    
    return df

def generate_monthly_summary(df):
    """Calculates aggregated monthly summary metrics for executive reporting."""
    summary = df.groupby('YearMonth').agg(
        Total_Revenue=('Revenue', 'sum'),
        Total_COGS=('COGS', 'sum'),
        Total_OpEx=('OperatingExpenses', 'sum'),
        Total_Net_Profit=('NetProfit', 'sum'),
        Total_Cash_Flow=('OperatingCashFlow', 'sum')
    ).reset_index()
    
    summary['Net_Profit_Margin_%'] = np.round((summary['Total_Net_Profit'] / summary['Total_Revenue']) * 100, 2)
    return summary

if __name__ == "__main__":
    raw_df = generate_financial_data(1200)
    cleaned_df = clean_financial_data(raw_df)
    monthly_summary = generate_monthly_summary(cleaned_df)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    output_dir = os.path.join(project_root, "data")
    os.makedirs(output_dir, exist_ok=True)
    
    cleaned_csv_path = os.path.join(output_dir, "cleaned_financial_data.csv")
    summary_csv_path = os.path.join(output_dir, "monthly_financial_summary.csv")
    
    cleaned_df.to_csv(cleaned_csv_path, index=False)
    monthly_summary.to_csv(summary_csv_path, index=False)
    
    print(f"[SUCCESS] Financial dataset exported to: {cleaned_csv_path}")
    print(f"[SUCCESS] Monthly summary exported to: {summary_csv_path}")