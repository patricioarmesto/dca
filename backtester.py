import pandas as pd
from strategies import Strategy

def run_backtest(strategy: Strategy, data: pd.DataFrame, monthly_budget: float) -> dict:
    """
    Simulates a monthly DCA strategy over the provided data.
    """
    # Resample to monthly to simulate monthly purchases
    # We'll take the first available trading day of each month
    monthly_data = data.resample('MS').first()
    
    total_invested = 0.0
    total_shares = 0.0
    
    # For logging history if needed
    history = []

    for date, row in monthly_data.iterrows():
        price = row['Close']
        
        # Skip if price is NaN (shouldn't happen with resample first, but good safety)
        if pd.isna(price):
            continue
            
        # Ask strategy how much to invest
        amount_to_invest = strategy.calculate_investment_amount(row, monthly_budget)
        
        # Buy shares
        shares_bought = amount_to_invest / price
        
        total_invested += amount_to_invest
        total_shares += shares_bought
        
        history.append({
            'Date': date,
            'Price': price,
            'Invested': amount_to_invest,
            'Shares': shares_bought,
            'Total_Shares': total_shares
        })
        
    # Calculate final metrics
    final_price = data.iloc[-1]['Close']
    final_value = total_shares * final_price
    profit_loss = final_value - total_invested
    roi = (profit_loss / total_invested) * 100 if total_invested > 0 else 0
    
    return {
        'Strategy': strategy.name,
        'Total Invested': total_invested,
        'Final Value': final_value,
        'Profit/Loss': profit_loss,
        'ROI (%)': roi,
        'Total Shares': total_shares
    }
