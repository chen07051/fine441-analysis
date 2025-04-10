import pandas as pd

# Define file paths for each stock
file_paths = {
    'AMZN': '/Users/yuchen/Desktop/PROJECT_441/AMZN_data.csv',
    'JPM': '/Users/yuchen/Desktop/PROJECT_441/JPM_data.csv',
    'MCD': '/Users/yuchen/Desktop/PROJECT_441/MCD_data.csv',
    'NFLX': '/Users/yuchen/Desktop/PROJECT_441/NFLX_data.csv',
    'PFE': '/Users/yuchen/Desktop/PROJECT_441/PFE_data.csv',
    'XOM': '/Users/yuchen/Desktop/PROJECT_441/XOM_data.csv',
    'SPX': '/Users/yuchen/Desktop/PROJECT_441/SPX_data.csv',
}

# Define date range
start_date = pd.to_datetime("2025-01-15")
end_date = pd.to_datetime("2025-03-20")

# Store results
std_devs = {}

# Loop through each stock and calculate standard deviation
for ticker, path in file_paths.items():
    df = pd.read_csv(path)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)].copy()
    df['Close/Last'] = df['Close/Last'].replace('[\$,]', '', regex=True).astype(float)
    df['Daily Return'] = df['Close/Last'].pct_change()
    std_dev = df['Daily Return'].std()
    std_devs[ticker] = std_dev

# Print results
for ticker, std in std_devs.items():
    print(f"{ticker}: {std:.4%}")
