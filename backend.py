from fastapi import FastAPI
from main import download
from main import compute_benish
from database import SessionLocal
from model import FraudScore

app=FastAPI()
@app.get("/")
def home():
    return {"message":"fraud api backend running "}
@app.get("/company/{Name}")
def get_company(Name:str):
    status=download(Name)
    if status=="Company not found":
        return {"error":"Company not found"}
    return{
        "Download":"Success",
        "Company":Name.lower().strip()
    }
    
@app.get("/benish/{Name}")
def benish_score(Name):
    result=compute_benish(Name)
    return {
        "Company":Name.lower().strip(),
        "Result":result
    }

@app.get("/scores")
def get_scores():

    db = SessionLocal()

    data = db.query(FraudScore).all()

    db.close()

    return data

@app.get("/scores/top-risk")
def top_risk():

    db = SessionLocal()

    data = db.query(FraudScore)\
             .order_by(FraudScore.m_score.desc())\
             .all()

    db.close()

    return data