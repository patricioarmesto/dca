# Adaptive DCA Strategies

from abc import ABC, abstractmethod
import pandas as pd


class Strategy(ABC):
    @abstractmethod
    def calculate_investment_amount(self, row: pd.Series, base_amount: float) -> float:
        """Determine how much to invest based on the strategy logic."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def get_phase(self, row: pd.Series) -> str:
        """Return a string indicating the market phase for this purchase."""
        pass


class StandardDCA(Strategy):
    @property
    def name(self) -> str:
        return "Standard DCA"

    def calculate_investment_amount(self, row: pd.Series, base_amount: float) -> float:
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
            return base_amount
        # 5% tolerance band around SMA
        tolerance = 0.05 * sma
        lower = sma - tolerance
        upper = sma + tolerance
        if price < lower:
            return base_amount * 2.0
        elif price > upper:
            return base_amount * 0.5
        else:
            return base_amount

    def get_phase(self, row: pd.Series) -> str:
        price = row['Close']
        sma = row['SMA_200']
        if pd.isna(sma):
            return "Neutral"
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
        diff_pct = (price - sma) / sma * 100
        if diff_pct > 10:
            multiplier = 0.8
        elif diff_pct >= 0:
            multiplier = 1.0
        elif diff_pct >= -10:
            multiplier = 1.2
        elif diff_pct >= -20:
            multiplier = 1.4
        elif diff_pct >= -30:
            multiplier = 1.6
        elif diff_pct >= -40:
            multiplier = 1.8
        else:
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


class BuyTheDip(Strategy):
    @property
    def name(self) -> str:
        return "Buy-the-dip"

    def calculate_investment_amount(self, row: pd.Series, base_amount: float) -> float:
        price = row['Close']
        sma = row['SMA_200']
        if pd.isna(sma):
            return base_amount
        diff_pct = (price - sma) / sma * 100
        if diff_pct > 10:
            multiplier = 0.5  # Euphoria Zone (reduce buying)
        elif diff_pct >= 0:
            multiplier = 1.0  # Normal
        elif diff_pct >= -10:
            multiplier = 2.0  # 10% Discount
        elif diff_pct >= -20:
            multiplier = 4.0  # 20% Discount
        elif diff_pct >= -30:
            multiplier = 8.0  # 30% Discount
        elif diff_pct >= -40:
            multiplier = 16.0  # 40% Discount
        else:
            multiplier = 32.0  # Max Discount
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
            return base_amount * 2.0
        elif rsi > 70:
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

class CapeRatioDCA(Strategy):
    @property
    def name(self) -> str:
        return "CAPE Ratio DCA"

    def calculate_investment_amount(self, row: pd.Series, base_amount: float) -> float:
        """Adjust investment based on the Shiller CAPE ratio.
        - CAPE > 25 (overvalued) → reduce buying (0.5×).
        - CAPE < 15 (undervalued) → increase buying (2.0×).
        - Otherwise → normal amount (1.0×).
        """
        cape = row.get('CAPE')
        if pd.isna(cape):
            return base_amount
        if cape > 25:
            multiplier = 0.5
        elif cape < 15:
            multiplier = 2.0
        else:
            multiplier = 1.0
        return base_amount * multiplier

    def get_phase(self, row: pd.Series) -> str:
        cape = row.get('CAPE')
        if pd.isna(cape):
            return "Neutral"
        if cape > 25:
            return "High CAPE"
        elif cape < 15:
            return "Low CAPE"
        else:
            return "Normal CAPE"
