from fastapi import FastAPI
from main import download
from main import compute_benish
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