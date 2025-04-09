import pandas as pd

# Load SPX data
file_path = "/Users/yuchen/Desktop/PROJECT_441/SPX_data.csv"
df = pd.read_csv(file_path)

# Clean and prepare
df.columns = [col.strip() for col in df.columns]
df['Date'] = pd.to_datetime(df['Date'])
df.sort_values('Date', inplace=True)

# Filter data to your analysis window
start_date = pd.to_datetime("2025-01-15")
end_date = pd.to_datetime("2025-03-20")
df_filtered = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)].copy()

# Convert 'Close/Last' to float
df_filtered['Close/Last'] = df_filtered['Close/Last'].replace('[\$,]', '', regex=True).astype(float)

# Compute daily returns
df_filtered['Daily Return'] = df_filtered['Close/Last'].pct_change()

# Compute average daily return (excluding NaN)
average_market_return = df_filtered['Daily Return'].mean()

# Output as a percentage
print(f"Average daily market return (SPX): {average_market_return:.4%}")
