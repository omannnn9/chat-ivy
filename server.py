from fastapi import FastAPI
from pydantic import BaseModel

class LoanCalcParams(BaseModel):
    amount: float
    rate_pct: float
    term_years: int

app = FastAPI()

@app.post("/loan_calc")
def loan_calc(params: LoanCalcParams):
    r = params.rate_pct / 100 / 12
    n = params.term_years * 12
    payment = (params.amount * r) / (1 - (1 + r) ** -n)
    return {"monthly_payment": round(payment, 2)}