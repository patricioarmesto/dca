# Adaptive DCA Backtester

A Python tool to backtest and compare different Dollar Cost Averaging (DCA) strategies against historical market data.

## Overview

Standard DCA involves investing a fixed amount at regular intervals. This project explores **Adaptive DCA** strategies that adjust the investment amount based on market conditions (Price vs SMA, RSI, etc.) to potentially improve returns.

## Strategies Implemented

1.  **Standard DCA**
    -   Invests a fixed base amount (e.g., $1,000) every month regardless of price.

2.  **Price-Deviation DCA (SMA)**
    -   **Buy More**: If Price < 200-day SMA, invest **2x**.
    -   **Buy Less**: If Price > 200-day SMA, invest **0.5x**.
    -   **Neutral**: Otherwise, invest **1x**.

3.  **SMA Threshold DCA (10%)**
    -   **Buy More**: If Price is **>10% below** the 200-day SMA, invest **2x**.
    -   **Buy Less**: If Price is **>10% above** the 200-day SMA, invest **0.5x**.
    -   **Neutral**: Otherwise, invest **1x**.

4.  **RSI-Based DCA**
    -   **Buy More**: If RSI < 30 (Oversold), invest **2x**.
    -   **Buy Less**: If RSI > 70 (Overbought), invest **0.5x**.
    -   **Neutral**: Otherwise, invest **1x**.

## Installation

This project uses `uv` for fast dependency management.

1.  **Install uv** (if not already installed):
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

2.  **Sync dependencies**:
    ```bash
    uv sync
    ```

## Usage

Run the backtester using `uv`:

```bash
uv run main.py
```

### Configuration

You can modify the configuration variables in `main.py` to change the asset, date range, or budget:

```python
def main():
    # Configuration
    TICKER = "SPY"          # Ticker symbol (e.g., BTC-USD, SPY, AAPL)
    START_DATE = "2000-01-01"
    END_DATE = "2023-12-31"
    MONTHLY_BUDGET = 1000.0
    ...
```

## Example Results

**Ticker**: SPY | **Period**: 2000-01-01 to 2023-12-31

| Strategy | Total Invested | Final Value | Profit/Loss | ROI (%) |
| :--- | :--- | :--- | :--- | :--- |
| **Price-Deviation DCA (SMA)** | $259,500 | $1,164,316 | $904,816 | **348.68%** |
| **SMA Threshold DCA (10%)** | $285,000 | $1,186,168 | $901,168 | **316.20%** |
| **RSI-Based DCA** | $274,500 | $1,112,143 | $837,643 | **305.15%** |
| **Standard DCA** | $288,000 | $1,155,432 | $867,432 | **301.19%** |

*Disclaimer: Past performance is not indicative of future results. This tool is for educational purposes only.*
