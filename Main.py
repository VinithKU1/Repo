from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests


app = FastAPI()

# Allow CORS from any origin (so your frontend can access this API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

EXCHANGE_API_URL = "https://api.exchangerate-api.com/v4/latest/"

@app.get("/exchange-rate")
def get_exchange_rate(from_currency: str, to_currency: str):
    try:
        response = requests.get(f"{EXCHANGE_API_URL}{from_currency.upper()}")
        data = response.json()
        rate = data["rates"].get(to_currency.upper())
        if not rate:
            raise HTTPException(status_code=404, detail="Currency not supported")
        return {"from": from_currency, "to": to_currency, "rate": rate}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/currencies")
def list_supported_currencies():
    response = requests.get(f"{EXCHANGE_API_URL}USD")
    data = response.json()
    return {"currencies": list(data["rates"].keys())}
