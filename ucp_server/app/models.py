"""
SQLAlchemy ORM Models for Products, Checkout Sessions, Session Items, and Orders
"""

import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base

class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(64), unique=True, index=True, nullable=False)
    title = Column(String(255), nullable=False)
    brand = Column(String(100), nullable=False)
    category = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    rating = Column(Float, default=4.5)
    stock_qty = Column(Integer, default=50)
    image_url = Column(Text, nullable=True)

class CheckoutSessionModel(Base):
    __tablename__ = "checkout_sessions"

    id = Column(String(64), primary_key=True, index=True)
    status = Column(String(32), default="REQUIRES_PAYMENT")  # REQUIRES_PAYMENT, COMPLETED, EXPIRED
    currency = Column(String(3), default="INR")
    subtotal = Column(Float, nullable=False)
    tax_total = Column(Float, nullable=False)
    shipping_total = Column(Float, nullable=False)
    grand_total = Column(Float, nullable=False)
    user_email = Column(String(255), nullable=True)
    shipping_address = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)

    items = relationship("SessionItemModel", back_populates="session", cascade="all, delete-orphan")
    order = relationship("OrderModel", back_populates="session", uselist=False)

class SessionItemModel(Base):
    __tablename__ = "session_items"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(64), ForeignKey("checkout_sessions.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    offer_id = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    unit_price = Column(Float, nullable=False)
    quantity = Column(Integer, default=1)
    total_price = Column(Float, nullable=False)

    session = relationship("CheckoutSessionModel", back_populates="items")
    product = relationship("ProductModel")

class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(String(64), primary_key=True, index=True)
    session_id = Column(String(64), ForeignKey("checkout_sessions.id"), nullable=False, unique=True)
    status = Column(String(32), default="COMPLETED")
    payment_method = Column(String(64), default="GOOGLE_PAY")
    payment_token = Column(String(255), nullable=False)
    total_paid = Column(Float, nullable=False)
    currency = Column(String(3), default="INR")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    session = relationship("CheckoutSessionModel", back_populates="order")
