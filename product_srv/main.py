from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Product
import os
from pydantic import BaseModel

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@product_db:5432/products_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

app = FastAPI()

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

@app.get("/products")
def get_products():
    session = SessionLocal()
    products = session.query(Product).all()
    session.close()
    return [{"id": p.id, "name": p.name, "price": p.price} for p in products]

@app.post("/products")
def add_product(name: str, price: int):
    session = SessionLocal()
    product = Product(name=name, price=price)
    session.add(product)
    session.commit()
    session.refresh(product)
    session.close()
    return {"id": product.id, "name": product.name, "price": product.price}

class ProductUpdate(BaseModel):
    name: str = None
    price: int = None

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    session = SessionLocal()
    # Получим все продукты прямо из базы
    products_all = session.query(Product).all()
    print("Все продукты в базе на момент удаления:", [{"id": p.id, "name": p.name, "price": p.price} for p in products_all])
    product = session.query(Product).filter(Product.id == product_id).first()
    print("Ищем id:", product_id, "Найден:", product)
    if product is None:
        session.close()
        raise HTTPException(status_code=404, detail="Product not found")
    session.delete(product)
    session.commit()
    session.close()
    return {"message": "Product deleted"}
@app.put("/products/{product_id}")
def update_product(product_id: int, product_update: ProductUpdate):
    session = SessionLocal()
    product = session.query(Product).filter(Product.id == product_id).first()
    if product is None:
        session.close()
        raise HTTPException(status_code=404, detail="Product not found")
    if product_update.name is not None:
        product.name = product_update.name
    if product_update.price is not None:
        product.price = product_update.price
    session.commit()
    session.refresh(product)
    session.close()
    return {"id": product.id, "name": product.name, "price": product.price}