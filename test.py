import yfinance as yf

t = yf.Ticker("RELIANCE.NS")
print(t.financials.shape)