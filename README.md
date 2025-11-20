# Adaptive DCA Strategy Suite

## Project Overview
This repository provides a **monthly Dollar‑Cost Averaging (DCA)** framework with several adaptive variations that adjust the monthly investment based on market conditions.

### Implemented Strategies
1. **Standard DCA** – Fixed $1,000 purchase each month.
2. **Price‑Deviation DCA (SMA)** – Uses a 200‑day SMA with a **±5 % tolerance** to decide whether to buy more, less, or the normal amount.
3. **Buy‑the‑dip** – Tiered‑multiplier strategy based on the price’s deviation from the SMA:
   | Zone | Price relative to SMA | Multiplier | Phase label |
   |------|-----------------------|------------|-------------|
   | **Euphoria Zone** | > +10 % above SMA | **0.5×** | "Euphoria Zone" |
   | **Normal** | 0 % to +10 % above SMA | **1.0×** | "Normal" |
   | **10 % Discount** | 0 % to –10 % below SMA | **2.0×** | "10% Discount" |
   | **20 % Discount** | –10 % to –20 % below SMA | **4.0×** | "20% Discount" |
   | **30 % Discount** | –20 % to –30 % below SMA | **8.0×** | "30% Discount" |
   | **40 % Discount** | –30 % to –40 % below SMA | **16.0×** | "40% Discount" |
   | **Max Discount** | > –40 % below SMA (i.e., > 40 % below SMA) | **32.0×** | "Max Discount" |
4. **CAPE Ratio DCA** – Adjusts based on the Shiller CAPE (Cyclically Adjusted Price-to-Earnings) ratio:
   - **High CAPE (> 25)**: Invest **0.5×** (Overvalued).
   - **Low CAPE (< 15)**: Invest **2.0×** (Undervalued).
   - **Normal**: Invest **1.0×**.
   *(Data is fetched dynamically from Robert Shiller's website)*.
5. **RSI‑Based DCA** – Uses the 14‑day Relative Strength Index to increase or decrease the monthly purchase.

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
- **Zone** – the market zone/phase for today (e.g., "Normal", "Above SMA", "High CAPE").
- **Today's Amount** – exact dollar amount the algorithm recommends buying today.
- **CAGR (%)** – Compound Annual Growth Rate over the back‑test period.
- **SMA 200** – the latest 200‑day SMA value used for the calculations.

> **Note:** `END_DATE` in `main.py` is now set automatically to the system’s current date using `date.today().isoformat()`, so the back‑test always runs up to today without manual changes.

---

## Sample Results (SPY, 2015‑01‑01 → today)
```
--- Adaptive DCA Backtester ---
Ticker: SPY
Period: 2015-01-01 to 2025-11-19
Base Monthly Budget: $1000.0
------------------------------
Running Standard DCA...
Running Price‑Deviation DCA (SMA)...
Running Buy‑the‑dip...
Running CAPE Ratio DCA...
Running RSI‑Based DCA...

                    Strategy  Total Invested  Final Value  Profit/Loss  ROI (%)       Zone  Today's Amount  CAGR (%)  SMA 200
0               Standard DCA      131,000.00   304,267.91   173,267.91   132.27   Standard        1,000.00      8.05   611.41
1  Price‑Deviation DCA (SMA)      104,000.00   251,343.68   147,343.68   141.68  Above SMA          500.00      8.45   611.41
2                Buy‑the‑dip      146,000.00   347,749.47   201,749.47   138.18     Normal        1,000.00      8.30   611.41
3             CAPE Ratio DCA      131,000.00   304,267.91   173,267.91   132.27  High CAPE          500.00      8.05   611.41
4              RSI‑Based DCA      125,000.00   288,303.63   163,303.63   130.64   Oversold        2,000.00      7.98   611.41
```
*(Note: Sample values for CAPE strategy are illustrative as they depend on the live data fetch)*

### Interpretation
- **Standard DCA** – baseline performance.
- **Price‑Deviation DCA (SMA)** – benefits from buying less when the price is significantly above the SMA.
- **Buy‑the‑dip** – the most aggressive strategy, scaling purchases up to **32×** the base amount when the price is far below the SMA.
- **CAPE Ratio DCA** – adjusts based on long-term valuation metrics.
- **RSI‑Based DCA** – adjusts exposure based on oversold/overbought conditions.

---

## Extending the Framework
- **Adjust SMA window** – modify `SMA_200` in `data_loader.py`.
- **Change tolerance** – edit the `tolerance = 0.05 * sma` line in `strategies.py` for the SMA‑based strategy.
- **Add new indicators** – e.g., MACD, Bollinger Bands, and create a new strategy class following the `Strategy` interface.
- **Different assets** – set `TICKER` in `main.py` to any symbol supported by `yfinance` (e.g., `BTC-USD`).

---

## License
MIT – feel free to fork, modify, and experiment.
