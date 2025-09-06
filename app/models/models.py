from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Chemical(Base):
    __tablename__ = "chemicals"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    cas_number = Column(String, nullable=False)  # Chemical Abstract Service number
    quantity = Column(Float, nullable=False)
    unit = Column(String, nullable=False)  # e.g., "kg", "L", "g"
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to inventory logs
    inventory_logs = relationship("InventoryLog", back_populates="chemical")


class InventoryLog(Base):
    __tablename__ = "inventory_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    chemical_id = Column(Integer, ForeignKey("chemicals.id"), nullable=False)
    action_type = Column(String, nullable=False)  # Must be: "add", "remove", or "update"
    quantity = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to chemical
    chemical = relationship("Chemical", back_populates="inventory_logs")