from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
import os

app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "ok", "env": os.getenv("ENV", "dev")}

class Signup(BaseModel):
    email: str
    password: str

@app.post("/auth/signup")
async def signup(payload: Signup):
    # placeholder: add hashing + DB insert
    return {"message": "signup ok (implement DB)"}
