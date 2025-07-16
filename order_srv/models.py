from sqlalchemy import Column, Integer, String

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer)
    delivery_id = Column(Integer)
    quantity = Column(Integer)
    status = Column(String, default="created")