from fastapi import FastAPI
from main import download
app=FastAPI()
@app.get("/")
def home():
    return {"message":"fraud api backend running "}
@app.get("/company/{Name}")
def get_company(Name: str):
    download(Name)
    return {
        "ticker":Name,
        "fraud_score": -2.5,
        "Risk":"medium"
        }
