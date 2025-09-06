from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from typing import List
from datetime import datetime

from app.database.database import get_db
from app.database.connection import get_asyncpg_connection
from app.models.models import Chemical
from app.schemas.schemas import (
    ChemicalCreate, 
    ChemicalUpdate, 
    ChemicalResponse,
    InventoryLogCreate,
    InventoryLogResponse
)

router = APIRouter()


@router.post("/chemicals/", response_model=ChemicalResponse)
async def create_chemical(chemical: ChemicalCreate, db: AsyncSession = Depends(get_db)):
    """Create a new chemical - USE ORM"""
    db_chemical = Chemical(
        name=chemical.name,
        cas_number=chemical.cas_number,
        quantity=chemical.quantity,
        unit=chemical.unit
    )
    db.add(db_chemical)
    await db.commit()
    await db.refresh(db_chemical)
    return db_chemical


@router.get("/chemicals/", response_model=List[ChemicalResponse])
async def get_all_chemicals(db: AsyncSession = Depends(get_db)):
    """Get all chemicals - USE ORM"""
    result = await db.execute(select(Chemical))
    chemicals = result.scalars().all()
    return chemicals


@router.get("/chemicals/{chemical_id}", response_model=ChemicalResponse)
async def get_chemical_by_id(chemical_id: int):
    """Get chemical by ID - USE ASYNCPG DIRECTLY"""
    conn = await get_asyncpg_connection()
    try:
        query = """
        SELECT id, name, cas_number, quantity, unit, created_at, updated_at 
        FROM chemicals 
        WHERE id = $1
        """
        row = await conn.fetchrow(query, chemical_id)
        if not row:
            raise HTTPException(status_code=404, detail="Chemical not found")
        
        return {
            "id": row["id"],
            "name": row["name"],
            "cas_number": row["cas_number"],
            "quantity": row["quantity"],
            "unit": row["unit"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"]
        }
    finally:
        await conn.close()


@router.put("/chemicals/{chemical_id}", response_model=ChemicalResponse)
async def update_chemical(
    chemical_id: int, 
    chemical_update: ChemicalUpdate, 
    db: AsyncSession = Depends(get_db)
):
    """Update chemical - USE ORM"""
    # First check if chemical exists
    result = await db.execute(select(Chemical).where(Chemical.id == chemical_id))
    db_chemical = result.scalar_one_or_none()
    
    if not db_chemical:
        raise HTTPException(status_code=404, detail="Chemical not found")
    
    # Update fields if provided
    update_data = chemical_update.dict(exclude_unset=True)
    if update_data:
        update_data["updated_at"] = datetime.utcnow()
        await db.execute(
            update(Chemical)
            .where(Chemical.id == chemical_id)
            .values(**update_data)
        )
        await db.commit()
        
        # Fetch updated chemical
        result = await db.execute(select(Chemical).where(Chemical.id == chemical_id))
        db_chemical = result.scalar_one()
    
    return db_chemical


@router.delete("/chemicals/{chemical_id}")
async def delete_chemical(chemical_id: int, db: AsyncSession = Depends(get_db)):
    """Delete chemical - USE ORM"""
    # First check if chemical exists
    result = await db.execute(select(Chemical).where(Chemical.id == chemical_id))
    db_chemical = result.scalar_one_or_none()
    
    if not db_chemical:
        raise HTTPException(status_code=404, detail="Chemical not found")
    
    await db.execute(delete(Chemical).where(Chemical.id == chemical_id))
    await db.commit()
    
    return {"message": "Chemical deleted successfully"}


@router.post("/chemicals/{chemical_id}/log", response_model=InventoryLogResponse)
async def create_inventory_log(
    chemical_id: int, 
    log: InventoryLogCreate, 
    db: AsyncSession = Depends(get_db)
):
    """Create inventory log entry - USE ORM"""
    # First check if chemical exists
    result = await db.execute(select(Chemical).where(Chemical.id == chemical_id))
    db_chemical = result.scalar_one_or_none()
    
    if not db_chemical:
        raise HTTPException(status_code=404, detail="Chemical not found")
    
    from app.models.models import InventoryLog
    
    db_log = InventoryLog(
        chemical_id=chemical_id,
        action_type=log.action_type,
        quantity=log.quantity
    )
    db.add(db_log)
    await db.commit()
    await db.refresh(db_log)
    
    return db_log


@router.get("/chemicals/{chemical_id}/logs", response_model=List[InventoryLogResponse])
async def get_chemical_logs(chemical_id: int):
    """Get all logs for chemical - USE ASYNCPG DIRECTLY"""
    conn = await get_asyncpg_connection()
    try:
        # First check if chemical exists
        chemical_query = "SELECT id FROM chemicals WHERE id = $1"
        chemical_row = await conn.fetchrow(chemical_query, chemical_id)
        if not chemical_row:
            raise HTTPException(status_code=404, detail="Chemical not found")
        
        # Get logs for the chemical
        logs_query = """
        SELECT id, chemical_id, action_type, quantity, timestamp 
        FROM inventory_logs 
        WHERE chemical_id = $1
        ORDER BY timestamp DESC
        """
        rows = await conn.fetch(logs_query, chemical_id)
        
        return [
            {
                "id": row["id"],
                "chemical_id": row["chemical_id"],
                "action_type": row["action_type"],
                "quantity": row["quantity"],
                "timestamp": row["timestamp"]
            }
            for row in rows
        ]
    finally:
        await conn.close()