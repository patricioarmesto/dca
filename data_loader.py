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

def fetch_cape_data() -> pd.DataFrame:
    """Fetch the Shiller CAPE ratio data from Yale website.
    Returns a DataFrame with a Date index and a 'CAPE' column.
    """
    import pandas as pd
    
    url = "http://www.econ.yale.edu/~shiller/data/ie_data.xls"
    print(f"Fetching CAPE data from {url}...")
    
    # Read Excel file, skipping header rows. 
    # Shiller's file typically has data starting around row 8.
    # We'll read a few rows to find the header.
    try:
        # Try reading with header at row 7 (0-indexed)
        df = pd.read_excel(url, sheet_name="Data", header=7)
        
        # The columns are usually: Date, P, D, E, CPI, Fraction, Rate, Real Price, Real Dividend, Real Earnings, CAPE
        # We need 'Date' and 'CAPE' (often labeled 'CAPE' or 'P/E10' or similar)
        
        # Rename columns to standard names if needed or select by index
        # Date is usually col 0, CAPE is usually col 10
        cape_col_idx = 10
        date_col_idx = 0
        
        # Select only needed columns
        cape_df = df.iloc[:, [date_col_idx, cape_col_idx]].copy()
        cape_df.columns = ["Date", "CAPE"]
        
        # Drop rows with NaN Date or CAPE
        cape_df = cape_df.dropna()
        
        # Convert Date column to datetime
        # Shiller's dates are float like 2023.01, 2023.1 etc.
        # We need to convert 2023.1 to 2023-02-01 approx? 
        # Actually 2023.01 is Jan, 2023.1 is Oct? No.
        # Format is Year.Month (e.g. 2023.01 = Jan 2023, 2023.10 = Oct 2023)
        # Let's parse it carefully.
        
        def parse_shiller_date(d):
            try:
                year = int(d)
                # residue is the month part. .01 to .12 approx
                # 2023.01 -> 0.01 * 100 = 1
                # 2023.1 -> 0.1 * 100 = 10
                month_part = round((d - year) * 100)
                if month_part == 0: month_part = 1 # Handle 1871.0 case?
                return pd.Timestamp(year=year, month=month_part, day=1)
            except:
                return pd.NaT

        cape_df["Date"] = cape_df["Date"].apply(parse_shiller_date)
        cape_df = cape_df.dropna(subset=["Date"])
        cape_df = cape_df.set_index("Date")
        
        # Ensure CAPE is numeric
        cape_df["CAPE"] = pd.to_numeric(cape_df["CAPE"], errors='coerce')
        cape_df = cape_df.dropna()
        
        return cape_df
        
    except Exception as e:
        print(f"Error parsing CAPE data: {e}")
        # Fallback to empty df or raise
        return pd.DataFrame(columns=["CAPE"])


def merge_cape(df: pd.DataFrame) -> pd.DataFrame:
    """Merge CAPE data into the price DataFrame based on date.
    The CAPE data is monthly; we forward-fill to align with daily rows.
    """
    cape_df = fetch_cape_data()
    # Resample CAPE to daily frequency, forward fill
    cape_daily = cape_df.resample('D').ffill()
    # Align with price df index
    merged = df.join(cape_daily, how='left')
    # Forward fill any missing CAPE values
    merged['CAPE'] = merged['CAPE'].ffill()
    return merged
