from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from backend.database import Base
from datetime import datetime

class Animal(Base):
    __tablename__ = "animals"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    breed = Column(String, nullable=False)
    age = Column(Float, nullable=False)
    state = Column(String, nullable=False)  # 'lactating' or 'dry'
    baseline_milk = Column(Float, default=20.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    health_records = relationship("HealthRecord", back_populates="animal")

class HealthRecord(Base):
    __tablename__ = "health_records"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    animal_id = Column(String, ForeignKey("animals.id"), nullable=False)
    date = Column(Date, default=datetime.utcnow().date)
    milk_yield = Column(Float, nullable=True)
    feed_intake = Column(String, nullable=False)
    activity_level = Column(String, nullable=False)
    temperature = Column(Float, nullable=False)
    risk_score = Column(Float, nullable=False)
    risk_level = Column(String, nullable=False)
    ph = Column(Float, nullable=True)
    heart_rate = Column(Float, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    animal = relationship("Animal", back_populates="health_records")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    phone = Column(String, unique=True, index=True, nullable=False)
    address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    preferred_language = Column(String, default="en")  # 'en' or 'hi'
    created_at = Column(DateTime, default=datetime.utcnow)
