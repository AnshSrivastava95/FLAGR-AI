from fastapi import FastAPI
from main import download
from main import compute_benish
app=FastAPI()
@app.get("/")
def home():
    return {"message":"fraud api backend running "}
@app.get("/company/{Name}")
def get_company(Name: str):
    download(Name)
    result=compute_benish(Name)
    return result
    