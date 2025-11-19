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
4. **RSI‑Based DCA** – Uses the 14‑day Relative Strength Index to increase or decrease the monthly purchase.

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
- **Today's Action** – a plain‑language recommendation for the current month ("Buy normal amount", "Buy more", or "Buy less").
- **Today's Amount** – the exact dollar amount the algorithm recommends buying today.

---

## Sample Results (SPY, 2000‑01‑01 → 2023‑12‑31)
```
--- Adaptive DCA Backtester ---
Ticker: SPY
Period: 2000-01-01 to 2023-12-31
Base Monthly Budget: $1000.0
------------------------------
Running Standard DCA...
Running Price‑Deviation DCA (SMA)...
Running Buy-the-dip...
Running RSI‑Based DCA...

                    Strategy  Total Invested  Final Value  Profit/Loss  ROI (%)  Today's Action      Today's Amount
0               Standard DCA      288,000.00 1,155,432.16   867,432.16   301.19  Buy normal amount        1,000.00
1  Price‑Deviation DCA (SMA)      264,000.00 1,155,034.94   891,034.94   337.51  Buy less                 500.00
2                Buy‑the‑dip      413,000.00 1,424,703.71 1,011,703.71   374.33  Buy less                 500.00
3              RSI‑Based DCA      274,500.00 1,112,143.30   837,643.30   305.15  Buy normal amount        500.00
```

### Interpretation
- **Standard DCA** – baseline performance.
- **Price‑Deviation DCA (SMA)** – benefits from buying less when the price is significantly above the SMA.
- **Buy‑the‑dip** – the most aggressive strategy, scaling purchases up to **32×** the base amount when the price is far below the SMA, delivering the highest ROI in this sample.
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
