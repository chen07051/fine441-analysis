import pandas as pd

# File paths for 6 stocks + market
file_paths = {
    'AMZ': "/Users/yuchen/Desktop/PROJECT_441/AMZN_data.csv",
    'JPM': "/Users/yuchen/Desktop/PROJECT_441/JPM_data.csv",
    'MCD': "/Users/yuchen/Desktop/PROJECT_441/MCD_data.csv",
    'NFLX': "/Users/yuchen/Desktop/PROJECT_441/NFLX_data.csv",
    'AMZN': "/Users/yuchen/Desktop/PROJECT_441/PFE_data.csv",
    'XOM': "/Users/yuchen/Desktop/PROJECT_441/XOM_data.csv",
    'SPX': "/Users/yuchen/Desktop/PROJECT_441/SPX_data.csv" 
}

# Create empty DataFrame to store monthly closing prices
monthly_prices = pd.DataFrame()

# Step 1–3: Load, clean, filter, and resample
for ticker, file_path in file_paths.items():
    df = pd.read_csv(file_path)

    # Clean 'Close/Last' and convert 'Date' to datetime
    df['Close/Last'] = df['Close/Last'].replace('[\$,]', '', regex=True).astype(float)
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    df.sort_index(inplace=True)

    # Filter to keep only complete months (ending on 28th or later)
    def is_month_complete(group):
        return group.index.max().day >= 28

    complete_months = df.groupby([df.index.year, df.index.month]).filter(is_month_complete)

    # Resample to month-end closing prices
    monthly_close = complete_months['Close/Last'].resample('ME').last()
    # Store in combined DataFrame
    monthly_prices[ticker] = monthly_close

# Step 4: Drop months with missing values
monthly_prices.dropna(inplace=True)

# Step 5: Calculate monthly returns
monthly_returns = monthly_prices.pct_change().dropna()

# Step 6: Compute covariances between each stock and the market (SPX)
market_returns = monthly_returns['SPX']
covariances = {}

for ticker in monthly_returns.columns:
    if ticker != 'SPX':
        cov = monthly_returns[ticker].cov(market_returns)
        covariances[ticker] = cov

# Step 7: Output covariances
print("Covariance between each stock and the market (SPX):\n")
for ticker, cov in covariances.items():
    print(f"{ticker} and SPX: {cov:.6f}")
