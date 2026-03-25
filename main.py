import yfinance as yf
from alias import FINANCIAL_ALIASES
import pandas as pd
import os
from database import engine,SessionLocal
from model import Base,FraudScore

Base.metadata.create_all(bind=engine)
mapping=pd.read_csv("Company_mapping.csv")
def resolve_symbol(Name:str):
    Name=Name.lower().strip()
    for _,row in mapping.iterrows():
        company=str(row["company_name"]).lower().strip()
        if Name==company or Name in company:
            return row["symbol"]
        alias_str=str(row["aliases"]).lower().strip()
        if alias_str!='nan':
            alias=alias_str.split("|")
            for ali in alias:
                if Name==ali.strip():
                    return row["symbol"]
            
    return None
    
def download(Name):
    Name=Name.lower().strip()
    symbol=resolve_symbol(Name)
    if symbol is None:
        return "Comapny not found"
    os.makedirs('flagr',exist_ok=True)
    ticker=yf.Ticker(symbol)
    ticker.financials.to_csv(f"flagr/income_{symbol}.csv")
    ticker.balance_sheet.to_csv(f"flagr/balance_sheet_{symbol}.csv")
    ticker.cash_flow.to_csv(f"flagr/cash_flow_{symbol}.csv")

def clean_data(df):
    df=df.dropna(axis=0,how="all")
    df=df.dropna(axis=1,how="all")
    df.columns=pd.to_datetime(df.columns,errors="coerce")
    df=df.sort_index(axis=1,ascending=False)
    df=df.fillna(0)
    return df

def get_value(df,alias,idx=0):
    for name in alias:
        if name in df.index:
            return df.loc[name].iloc[idx]
    return 0
    
def compute_benish(Name:str):
    symbol = resolve_symbol(Name)
    if symbol is None:
        return {"error": "company not found"}
    file_path = f"flagr/income_{symbol}.csv"
    if not os.path.exists(file_path):
        return {"error": "financials not downloaded"}
    income=pd.read_csv(f"flagr/income_{symbol}.csv",index_col=0)
    balance=pd.read_csv(f"flagr/balance_sheet_{symbol}.csv",index_col=0)
    cash_flow=pd.read_csv(f"flagr/cash_flow_{symbol}.csv",index_col=0)
    
    income=clean_data(income)
    balance=clean_data(balance)
    cash_flow=clean_data(cash_flow)
    
    rev_t=get_value(income,FINANCIAL_ALIASES["revenue"],0)
    rev_t1=get_value(income,FINANCIAL_ALIASES["revenue"],1)
    
    ar_t = get_value(balance, FINANCIAL_ALIASES["receivables"], 0)
    ar_t1 = get_value(balance, FINANCIAL_ALIASES["receivables"], 1)

    ni_t = get_value(income, FINANCIAL_ALIASES["net_income"], 0)

    ta_t = get_value(balance, FINANCIAL_ALIASES["total_assets"], 0)
    ta_t1 = get_value(balance, FINANCIAL_ALIASES["total_assets"], 1)

    cfo_t = get_value(cash_flow, FINANCIAL_ALIASES["operating_cashflow"], 0)
    
    ltd_t = get_value(balance, FINANCIAL_ALIASES["long_term_debt"], 0)
    ltd_t1 = get_value(balance, FINANCIAL_ALIASES["long_term_debt"], 1)
    
    cl_t = get_value(balance, FINANCIAL_ALIASES["current_liabilities"], 0)
    cl_t1 = get_value(balance, FINANCIAL_ALIASES["current_liabilities"], 1)
    def safe_div(a,b):
        return a/b if b!=0 else 0
    dsri = safe_div(
    safe_div(ar_t, rev_t),
    safe_div(ar_t1, rev_t1)
    )
    sgi = safe_div(rev_t, rev_t1)
    tata = safe_div(ni_t - cfo_t, ta_t)
    
    lvgi = safe_div(
    safe_div(ltd_t + cl_t, ta_t),
    safe_div(ltd_t1 + cl_t1, ta_t1)
    )
    
    m = -4.84 + 0.92*dsri + 0.89*sgi + 4.67*tata - 0.32*lvgi
    risk="high" if m>-1.78 else "low"
    db = SessionLocal()
    record = FraudScore(
    symbol=symbol,
    company=Name,
    m_score=m,
    risk=risk
)
    db.add(record)
    db.commit()
    db.close()
    
    return{
        "Company ": Name,
        "m_score ": m,
        "Risk ": risk
        
    }
    