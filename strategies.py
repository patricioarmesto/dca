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

    @abstractmethod
    def get_phase(self, row: pd.Series) -> str:
        """
        Returns a string indicating the current market phase according to the strategy.
        """
        pass

class StandardDCA(Strategy):
    @property
    def name(self) -> str:
        return "Standard DCA"

    def calculate_investment_amount(self, row: pd.Series, base_amount: float) -> float:
        # Always invest the fixed base amount
        return base_amount

    def get_phase(self, row: pd.Series) -> str:
        return "Standard"

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
        
        # Define a 5% tolerance band around the SMA as neutral
        tolerance = 0.05 * sma
        lower = sma - tolerance
        upper = sma + tolerance
        
        if price < lower:
            # Significantly below SMA → buy more
            return base_amount * 2.0
        elif price > upper:
            # Significantly above SMA → buy less
            return base_amount * 0.5
        else:
            # Within tolerance → normal purchase
            return base_amount

    def get_phase(self, row: pd.Series) -> str:
        price = row['Close']
        sma = row['SMA_200']
        
        if pd.isna(sma):
            return "Neutral"
        # Use the same 5% tolerance band as in calculate_investment_amount
        tolerance = 0.05 * sma
        lower = sma - tolerance
        upper = sma + tolerance
        if price < lower:
            return "Below SMA"
        elif price > upper:
            return "Above SMA"
        else:
            return "Neutral"

class SmaThresholdDCA(Strategy):
    @property
    def name(self) -> str:
        return "SMA Threshold DCA (10%)"

    def calculate_investment_amount(self, row: pd.Series, base_amount: float) -> float:
        price = row['Close']
        sma = row['SMA_200']

        if pd.isna(sma):
            return base_amount

        # percentage difference from SMA
        diff_pct = (price - sma) / sma * 100

        if diff_pct > 10:
            # Euphoria Zone: reduce buying
            multiplier = 0.8
        elif diff_pct >= 0:
            # Normal
            multiplier = 1.0
        elif diff_pct >= -10:
            # 10% Discount
            multiplier = 1.2
        elif diff_pct >= -20:
            multiplier = 1.4
        elif diff_pct >= -30:
            multiplier = 1.6
        elif diff_pct >= -40:
            multiplier = 1.8
        else:
            # > -40% below SMA (i.e., more than 40% below)
            multiplier = 2.0

        return base_amount * multiplier

    def get_phase(self, row: pd.Series) -> str:
        price = row['Close']
        sma = row['SMA_200']

        if pd.isna(sma):
            return "Neutral"

        diff_pct = (price - sma) / sma * 100

        if diff_pct > 10:
            return "Euphoria Zone"
        elif diff_pct >= 0:
            return "Normal"
        elif diff_pct >= -10:
            return "10% Discount"
        elif diff_pct >= -20:
            return "20% Discount"
        elif diff_pct >= -30:
            return "30% Discount"
        elif diff_pct >= -40:
            return "40% Discount"
        else:
            return "Max Discount"

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

    def get_phase(self, row: pd.Series) -> str:
        rsi = row['RSI_14']
        
        if pd.isna(rsi):
            return "Neutral"
            
        if rsi < 30:
            return "Oversold"
        elif rsi > 70:
            return "Overbought"
        else:
            return "Neutral"
