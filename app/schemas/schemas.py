from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional


# Request schemas
class ChemicalCreate(BaseModel):
    name: str
    cas_number: str
    quantity: float
    unit: str


class ChemicalUpdate(BaseModel):
    name: Optional[str] = None
    cas_number: Optional[str] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None


class InventoryLogCreate(BaseModel):
    action_type: str  # Must validate: "add", "remove", "update"
    quantity: float
    
    @validator('action_type')
    def validate_action_type(cls, v):
        if v not in ['add', 'remove', 'update']:
            raise ValueError('action_type must be one of: add, remove, update')
        return v


# Response schemas
class ChemicalResponse(BaseModel):
    id: int
    name: str
    cas_number: str
    quantity: float
    unit: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class InventoryLogResponse(BaseModel):
    id: int
    chemical_id: int
    action_type: str
    quantity: float
    timestamp: datetime
    
    class Config:
        from_attributes = True