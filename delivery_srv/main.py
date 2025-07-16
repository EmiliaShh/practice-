from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Delivery
import os

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@delivery_db:5432/delivery_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

app = FastAPI()

class DeliveryCreate(BaseModel):
    address: str
    status: str

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/deliveries")
def get_deliveries():
    session = SessionLocal()
    deliveries = session.query(Delivery).all()
    session.close()
    return [{"id": d.id, "address": d.address, "status": d.status} for d in deliveries]

@app.post("/deliveries")
def add_delivery(delivery: DeliveryCreate):
    session = SessionLocal()
    delivery_obj = Delivery(address=delivery.address, status=delivery.status)
    session.add(delivery_obj)
    session.commit()
    session.refresh(delivery_obj)
    session.close()
    return {"id": delivery_obj.id, "address": delivery_obj.address, "status": delivery_obj.status}