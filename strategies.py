from abc import ABC, abstractmethod
import pandas as pd

class Strategy(ABC):
    @abstractmethod
    def calculate_investment_amount(self, row: pd.Series, base_amount: float) -> float:
        """
        Determines how much to invest based on the strategy logic.
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

class StandardDCA(Strategy):
    @property
    def name(self) -> str:
        return "Standard DCA"

    def calculate_investment_amount(self, row: pd.Series, base_amount: float) -> float:
        # Always invest the fixed base amount
        return base_amount

class SmaDCA(Strategy):
    @property
    def name(self) -> str:
        return "Price-Deviation DCA (SMA)"

    def calculate_investment_amount(self, row: pd.Series, base_amount: float) -> float:
        price = row['Close']
        sma = row['SMA_200']
        
        if pd.isna(sma):
            # If SMA is not available (first 200 days), fallback to standard DCA
            return base_amount
            
        if price < sma:
            # Price is below SMA (cheap) -> Buy more
            return base_amount * 2.0
        elif price > sma:
            # Price is above SMA (expensive) -> Buy less
            return base_amount * 0.5
        else:
            return base_amount

class SmaThresholdDCA(Strategy):
    @property
    def name(self) -> str:
        return "SMA Threshold DCA (10%)"

    def calculate_investment_amount(self, row: pd.Series, base_amount: float) -> float:
        price = row['Close']
        sma = row['SMA_200']
        
        if pd.isna(sma):
            return base_amount
            
        if price < (sma * 0.9):
            # Price is >10% below SMA -> Buy more
            return base_amount * 2.0
        elif price > (sma * 1.1):
            # Price is >10% above SMA -> Buy less
            return base_amount * 0.5
        else:
            return base_amount

class RsiDCA(Strategy):
    @property
    def name(self) -> str:
        return "RSI-Based DCA"

    def calculate_investment_amount(self, row: pd.Series, base_amount: float) -> float:
        rsi = row['RSI_14']
        
        if pd.isna(rsi):
            return base_amount
            
        if rsi < 30:
            # Oversold -> Buy more
            return base_amount * 2.0
        elif rsi > 70:
            # Overbought -> Buy less
            return base_amount * 0.5
        else:
            return base_amount
