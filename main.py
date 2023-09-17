import json
from datetime import date, timedelta
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from sqlalchemy import Boolean
from sqlalchemy import create_engine, Column, Integer, String, extract
from sqlalchemy import Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_

with open('config.json', 'r') as f:
    config = json.load(f)

DAY_THRESHOLD = config.get("day_threshold", 1)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = "sqlite:///./household.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    amount = Column(Integer)
    is_income = Column(Boolean)
    date = Column(Date, default=date.today())
    category = Column(String, default="その他")

Base.metadata.create_all(bind=engine)

class TransactionCreate(BaseModel):
    name: str
    amount: int
    is_income: bool
    date: Optional[date]
    category: Optional[str] = "その他"

class TransactionResponse(BaseModel):
    id: int
    name: str
    amount: int
    is_income: bool
    category: str

class SummaryResponse(BaseModel):
    income: int
    expense: int
    difference: int

@app.get("/config/")
def read_config():
    return {"day_threshold": DAY_THRESHOLD}

@app.post("/transactions/", response_model=TransactionCreate)
def create_transaction(transaction: TransactionCreate):
    db = SessionLocal()
    try:
        db_transaction = Transaction(**transaction.dict())
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
    finally:
        db.close()
    return db_transaction

@app.get("/transactions/", response_model=List[TransactionResponse])
def read_transactions(year: int, month: int, day: int, skip: int = 0, limit: int = 10):
    db = SessionLocal()
    if day < DAY_THRESHOLD:
        start_date = date(year, month - 1, DAY_THRESHOLD) if month != 1 else date(year - 1, 12, DAY_THRESHOLD)
        end_date = date(year, month, DAY_THRESHOLD - 1)
    else:
        start_date = date(year, month, DAY_THRESHOLD)
        end_date = date(year, month % 12 + 1, DAY_THRESHOLD - 1) if month != 12 else date(year + 1, 1, DAY_THRESHOLD - 1)

    transactions = db.query(Transaction).filter(
        and_(
            Transaction.date >= start_date,
            Transaction.date <= end_date
        )
    ).offset(skip).limit(limit).all()
    db.close()
    return transactions

@app.get("/summary/{year}/{month}/{day}", response_model=SummaryResponse)
def read_summary(year: int, month: int, day: int):
    db = SessionLocal()
    if day < DAY_THRESHOLD:
        start_date = date(year, month - 1, DAY_THRESHOLD) if month != 1 else date(year - 1, 12, DAY_THRESHOLD)
        end_date = date(year, month, DAY_THRESHOLD - 1)
    else:
        start_date = date(year, month, DAY_THRESHOLD)
        end_date = date(year, month % 12 + 1, DAY_THRESHOLD - 1) if month != 12 else date(year + 1, 1, DAY_THRESHOLD - 1)

    transactions = db.query(Transaction).filter(
        and_(
            Transaction.date >= start_date,
            Transaction.date <= end_date
        )
    ).all()

    income = sum(t.amount for t in transactions if t.is_income)
    expense = sum(t.amount for t in transactions if not t.is_income)
    difference = income - expense
    db.close()
    return {"income": income, "expense": expense, "difference": difference}

@app.delete("/transactions/{transaction_id}", response_model=TransactionResponse)
def delete_transaction(transaction_id: int):
    db = SessionLocal()
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if db_transaction is None:
        db.close()
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(db_transaction)
    db.commit()
    db.close()
    return db_transaction
