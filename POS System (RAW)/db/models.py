from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class Produk(Base):
    __tablename__ = 'produk'
    product_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    category = Column(String)
    expiry_date = Column(DateTime)
    stock_quantity = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class Transaksi(Base):
    __tablename__ = 'transaksi'
    transaction_id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    total_amount = Column(Float, nullable=False)
    payment_method = Column(String, nullable=False)
    synced = Column(Boolean, default=False)
    details = relationship("DetailTransaksi", back_populates="transaksi")

class DetailTransaksi(Base):
    __tablename__ = 'detail_transaksi'
    detail_id = Column(Integer, primary_key=True)
    transaction_id = Column(Integer, ForeignKey('transaksi.transaction_id'))
    product_id = Column(Integer, ForeignKey('produk.product_id'))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)

    transaksi = relationship("Transaksi", back_populates="details")
    produk = relationship("Produk")

class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)  # e.g., 'admin', 'kasir'
    is_active = Column(Boolean, default=True)
    creation_date = Column(DateTime, default=datetime.datetime.utcnow)

class LogSinkronisasi(Base):
    __tablename__ = 'log_sinkronisasi'
    sync_id = Column(Integer, primary_key=True)
    sync_time = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String)
    message = Column(Text)


class InventoryAdjustment(Base):
    __tablename__ = 'inventory_adjustment'
    adjustment_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('produk.product_id'))
    adjusted_by = Column(String)  # could be a username or user_id
    change = Column(Integer)  # positive or negative
    reason = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    produk = relationship("Produk")
