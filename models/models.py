from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    price = Column(Float)
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="products")
    inventory = relationship("Inventory", back_populates="product")
    sales = relationship("Sale", back_populates="product")
    inventory_changes = relationship("InventoryChangeLog", back_populates="product")


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    sale_timestamp = Column(DateTime(timezone=True))
    quantity_sold = Column(Integer)

    product = relationship("Product", back_populates="sales")


class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    current_stock = Column(Integer)
    low_stock_alert_threshold = Column(Integer)

    product = relationship("Product", back_populates="inventory")


class InventoryChangeLog(Base):
    __tablename__ = "inventory_change_log"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    timestamp = Column(DateTime(timezone=True))
    quantity_change = Column(Integer)
    new_quantity = Column(Integer)

    product = relationship("Product", back_populates="inventory_changes")
