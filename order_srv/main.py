from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@order_db:5432/orders_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer)
    delivery_id = Column(Integer)
    quantity = Column(Integer)
    status = Column(String, default="created")  # Новое поле!

class OrderCreate(BaseModel):
    product_id: int
    delivery_id: int
    quantity: int
    status: str = "created"

class OrderUpdateStatus(BaseModel):
    status: str

app = FastAPI()

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/orders")
def get_orders():
    session = SessionLocal()
    orders = session.query(Order).all()
    session.close()
    return [
        {
            "id": o.id,
            "product_id": o.product_id,
            "delivery_id": o.delivery_id,
            "quantity": o.quantity,
            "status": o.status
        }
        for o in orders
    ]

@app.post("/orders")
def add_order(order: OrderCreate):
    session = SessionLocal()
    order_obj = Order(
        product_id=order.product_id,
        delivery_id=order.delivery_id,
        quantity=order.quantity,
        status=order.status
    )
    session.add(order_obj)
    session.commit()
    session.refresh(order_obj)
    session.close()
    return {
        "id": order_obj.id,
        "product_id": order_obj.product_id,
        "delivery_id": order_obj.delivery_id,
        "quantity": order_obj.quantity,
        "status": order_obj.status
    }

@app.put("/orders/{order_id}/status")
def update_order_status(order_id: int = Path(...), status_update: OrderUpdateStatus = ...):
    session = SessionLocal()
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        session.close()
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = status_update.status
    session.commit()
    session.refresh(order)
    session.close()
    return {
        "id": order.id,
        "product_id": order.product_id,
        "delivery_id": order.delivery_id,
        "quantity": order.quantity,
        "status": order.status
    }