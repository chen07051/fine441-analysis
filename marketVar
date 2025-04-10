import pandas as pd

# Load data
file_path = "/Users/yuchen/Desktop/PROJECT_441/SPX_data.csv"
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
monthly_prices = complete_months['Close/Last'].resample('ME').last()

# Step 4: Calculate month-over-month returns
monthly_returns = monthly_prices.pct_change()

# Step 5: Compute monthly variance
monthly_var = monthly_returns.var()

# Output result
print(f"\nMonthly variance of returns: {monthly_var:.6f}")
