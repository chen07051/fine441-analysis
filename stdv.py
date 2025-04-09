import pandas as pd

# Load data
file_path = "/Users/yuchen/Desktop/market_data.csv"
df = pd.read_csv(file_path)

# Step 1: Clean and prepare
df['Close/Last'] = df['Close/Last'].replace('[\$,]', '', regex=True).astype(float)
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)
df.sort_index(inplace=True)

# Step 2: Group by month and check if each month contains a date near the month-end (28th or later)
def is_month_complete(group):
    return group.index.max().day >= 28

# Filter to keep only complete months
complete_months = df.groupby([df.index.year, df.index.month]).filter(is_month_complete)

# Step 3: Resample complete data to month-end closing prices
monthly_prices = complete_months['Close/Last'].resample('M').last()

# Step 4: Calculate month-over-month returns
monthly_returns = monthly_prices.pct_change()
print(monthly_returns)

# Step 5: Compute standard deviation
monthly_std_dev = monthly_returns.std()

# Output results
print(f"\nStandard deviation of monthly returns: {monthly_std_dev:.4%}")

