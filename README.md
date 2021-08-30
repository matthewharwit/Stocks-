# Algo Stock Trading Bot-

List of daily execution scripts - Actual data analysis not included (I can't be giving my secrets away!)  

Includes:

Connecting to IBKR API, grabbing list of tickers from Schwab (post-filtered), automation scripts (time-specific scripts), historic data returns (at various thresholds), downloading EOD data, etc. 

Schwab_Gap_Up/Down grabs filtered tickers from StreetSmartEdge and downloads as a csv.

Pre/Postopen are scripts for connecting to the IB TWS API and placing orders. Preopen is ran prior to market open and Postopen at market open. 

Also includes some webscrapers for preliminary stock filtering (don't want to trade highly non-liquid, small market cap tickers - simply not scalable.) 

   
