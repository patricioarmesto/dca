import yfinance as yf
import pandas as pd

def fetch_data(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetches historical daily data for a given ticker.
    """
    print(f"Fetching data for {ticker} from {start_date} to {end_date}...")
    df = yf.download(ticker, start=start_date, end=end_date, progress=False)
    
    if df.empty:
        raise ValueError(f"No data found for {ticker}. Please check the ticker symbol and date range.")
    
    # Ensure we have a flat index if MultiIndex is returned (common in new yfinance versions)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
        
    return df

def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates technical indicators required for the strategies:
    - SMA_200: 200-day Simple Moving Average
    - RSI_14: 14-day Relative Strength Index
    """
    df = df.copy()
    
    # Calculate SMA 200
    df['SMA_200'] = df['Close'].rolling(window=200).mean()
    
    # Calculate RSI 14
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    
    rs = gain / loss
    df['RSI_14'] = 100 - (100 / (1 + rs))
    
    # Fill NaN values that result from rolling windows (optional, but good for safety)
    # For backtesting, we just need to make sure we don't trade on NaNs
    
    return df
