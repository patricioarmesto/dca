import pandas as pd
from data_loader import fetch_data, calculate_indicators
from strategies import StandardDCA, SmaDCA, RsiDCA, SmaThresholdDCA
from backtester import run_backtest

def main():
    # Configuration
    TICKER = "SPY"
    START_DATE = "2000-01-01"
    END_DATE = "2023-12-31"
    MONTHLY_BUDGET = 1000.0
    
    print(f"--- Adaptive DCA Backtester ---")
    print(f"Ticker: {TICKER}")
    print(f"Period: {START_DATE} to {END_DATE}")
    print(f"Base Monthly Budget: ${MONTHLY_BUDGET}")
    print("-" * 30)
    
    # 1. Fetch Data
    try:
        df = fetch_data(TICKER, START_DATE, END_DATE)
        df = calculate_indicators(df)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return

    # 2. Define Strategies
    strategies = [
        StandardDCA(),
        SmaDCA(),
        SmaThresholdDCA(),
        RsiDCA()
    ]
    
    # 3. Run Backtests
    results = []
    for strategy in strategies:
        print(f"Running {strategy.name}...")
        res = run_backtest(strategy, df, MONTHLY_BUDGET)
        results.append(res)
        
    # 4. Display Results
    results_df = pd.DataFrame(results)
    
    # Formatting for better readability
    pd.options.display.float_format = '{:,.2f}'.format
    
    print(results_df[['Strategy', 'Total Invested', 'Final Value', 'Profit/Loss', 'ROI (%)']])
    print("-" * 30)

if __name__ == "__main__":
    main()
