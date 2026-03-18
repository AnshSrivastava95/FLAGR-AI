import yfinance as yf
import pandas as pd
import os
mapping=pd.read_csv("Company_mapping.csv")
def resolve_symbol(Name:str):
    Name=Name.lower().strip()
    for _,row in mapping.iterrows():
        company=str(row["company_name"]).lower().strip()
        if Name==company :
            return row["symbol"]
    return None
    
def download(Name):
    symbol=resolve_symbol(Name)
    if symbol is None:
        return "Comapny not found"
    os.makedirs('flagr',exist_ok=True)
    ticker=yf.Ticker(symbol)
    ticker.financials.to_csv(f"flagr/income_{Name}.csv")
    ticker.balance_sheet.to_csv(f"flagr/balance_sheet_{Name}.csv")
    ticker.cash_flow.to_csv(f"flagr/cash_flow_{Name}.csv")