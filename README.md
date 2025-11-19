# Adaptive DCA Strategy Suite

## Project Overview
This repository implements a **monthly Dollar‑Cost Averaging (DCA)** framework with several adaptive variations:

1. **Standard DCA** – fixed $1,000 purchase each month.
2. **Price‑Deviation DCA (SMA)** – compares price to a 200‑day Simple Moving Average (SMA).  
   - **Tolerance:** ±5 % of the SMA is considered *neutral* (regular $1,000 purchase).  
   - **Below SMA – 5 %** → invest **2×** ($2,000).  
   - **Above SMA + 5 %** → invest **0.5×** ($500).
3. **SMA Threshold DCA (10 %)** – same SMA but with a stricter 10 % band.
4. **RSI‑Based DCA** – uses the 14‑day Relative Strength Index.

The framework backtests each strategy on historical price data and reports performance metrics **and** a breakdown of how many purchases occurred in each market phase.

---

## Installation (uses `uv`)
```bash
# Clone the repo (if not already cloned)
git clone https://github.com/patricioarmesto/dca.git
cd dca4

# Install dependencies in a virtual environment managed by uv
uv sync
```

## Running the Backtest
```bash
uv run main.py
```
The script prints a table with the following columns:
- **Strategy** – name of the strategy.
- **Total Invested** – cumulative cash spent.
- **Final Value** – portfolio value at the end of the period.
- **Profit/Loss** – absolute gain.
- **ROI (%)** – percentage return.
- **Phase Counts** – how many monthly purchases fell into each defined phase.

---

## Sample Results (SPY, 2000‑01‑01 → 2023‑12‑31)
```
--- Adaptive DCA Backtester ---
Ticker: SPY
Period: 2000-01-01 to 2023-12-31
Base Monthly Budget: $1000.0
------------------------------
Running Standard DCA...
Running Price-Deviation DCA (SMA)...
Running SMA Threshold DCA (10%)...
Running RSI-Based DCA...

--- Performance Report ---
                    Strategy  Total Invested  Final Value  Profit/Loss  ROI (%)                                       Phase Counts
0               Standard DCA      288,000.00 1,155,432.08   867,432.08   301.19                                  {'Standard': 288}
1  Price-Deviation DCA (SMA)      264,000.00 1,155,034.86   891,034.86   337.51  {'Neutral': 114, 'Below SMA': 42, 'Above SMA': 132}
2    SMA Threshold DCA (10%)      285,000.00 1,186,168.15   901,168.15   316.20  {'Neutral': 228, 'Significantly Below SMA': 18, 'Significantly Above SMA': 39}
3              RSI-Based DCA      274,500.00 1,112,143.22   837,643.22   305.15  {'Neutral': 225, 'Overbought': 51, 'Oversold': 12}
------------------------------
```

### Interpreting the Phase Counts
- **Standard DCA** – always `Standard` (one purchase per month).
- **Price‑Deviation DCA (SMA)** – with a **5 % tolerance** you see a substantial number of *neutral* purchases (114 out of 288 months).  
  - `Below SMA` (42) and `Above SMA` (132) represent the months where the algorithm aggressively bought more or less, respectively.
- **SMA Threshold DCA (10 %)** – uses a stricter 10 % band, so most months fall into the `Neutral` bucket (228), with fewer extreme moves.
- **RSI‑Based DCA** – `Oversold` (12) and `Overbought` (51) indicate the months where the RSI triggered larger or smaller buys.

---

## Extending the Framework
- **Adjust SMA window** – change `SMA_200` to another period in `data_loader.py`.
- **Change tolerance** – modify the `tolerance = 0.05 * sma` line in `strategies.py` for the SMA strategy.
- **Add new indicators** – e.g., MACD, Bollinger Bands, and create a new strategy class following the `Strategy` interface.
- **Different assets** – set `TICKER` in `main.py` to any symbol supported by `yfinance` (e.g., `BTC-USD`, `ETH-USD`).

---

## License
MIT – feel free to fork, modify, and experiment.
