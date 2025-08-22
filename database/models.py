import os
from sqlalchemy import (create_engine, Column, Integer, String,
                        Float, Text, DateTime, JSON, ForeignKey, Enum)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import enum


Base = declarative_base()


class OrderStatus(enum.Enum):
    NEW = "new"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(100))
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone = Column(String(20))
    created_at = Column(DateTime, default=datetime.now)

    orders = relationship("Order", back_populates="user")


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    size = Column(String(50), nullable=False)
    cost = Column(Float, nullable=False)
    description = Column(Text)
    references = Column(JSON)
    status = Column(Enum(OrderStatus), default=OrderStatus.NEW)
    tracking_number = Column(String(100))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(
        DateTime, default=datetime.now, onupdate=datetime.now)

    user = relationship("User", back_populates="orders")


engine = create_engine(os.getenv('DATABASE_URL'))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)
