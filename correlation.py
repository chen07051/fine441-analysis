import pandas as pd

# File paths for 6 stocks
file_paths = {
    'AMZN': "/Users/yuchen/Desktop/PROJECT_441/AMZN_data.csv",
    'JPM': "/Users/yuchen/Desktop/PROJECT_441/JPM_data.csv",
    'MCD': "/Users/yuchen/Desktop/PROJECT_441/MCD_data.csv",
    'NFLX': "/Users/yuchen/Desktop/PROJECT_441/NFLX_data.csv",
    'PFE': "/Users/yuchen/Desktop/PROJECT_441/PFE_data.csv",
    'XOM': "/Users/yuchen/Desktop/PROJECT_441/XOM_data.csv"
}

# Create empty DataFrame to store monthly closing prices
monthly_prices = pd.DataFrame()

# Step 1: Load, clean, and prepare each dataset
for ticker, file_path in file_paths.items():
    df = pd.read_csv(file_path)

    # Clean 'Close/Last' and convert 'Date' to datetime
    df['Close/Last'] = df['Close/Last'].replace('[\$,]', '', regex=True).astype(float)
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    df.sort_index(inplace=True)

    # Step 2: Filter to keep only complete months (ending on 28th or later)
    def is_month_complete(group):
        return group.index.max().day >= 28

    complete_months = df.groupby([df.index.year, df.index.month]).filter(is_month_complete)

    # Step 3: Resample to month-end closing prices
    monthly_close = complete_months['Close/Last'].resample('ME').last()

    # Store in combined DataFrame
    monthly_prices[ticker] = monthly_close

# Step 4: Drop months with missing values (incomplete across any stock)
monthly_prices.dropna(inplace=True)

# Step 5: Calculate monthly returns
monthly_returns = monthly_prices.pct_change().dropna()

# Step 6: Compute correlation matrix
correlation_matrix = monthly_returns.corr()

# Output the correlation matrix
print(correlation_matrix.round(4))
