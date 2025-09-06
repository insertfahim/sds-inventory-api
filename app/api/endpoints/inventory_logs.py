from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.database.database import get_db
from app.database.connection import get_asyncpg_connection
from app.models.models import InventoryLog
from app.schemas.schemas import InventoryLogResponse

router = APIRouter()


@router.get("/inventory-logs/", response_model=List[InventoryLogResponse])
async def get_all_inventory_logs(db: AsyncSession = Depends(get_db)):
    """Get all inventory logs - USE ORM"""
    result = await db.execute(select(InventoryLog).order_by(InventoryLog.timestamp.desc()))
    logs = result.scalars().all()
    return logs


@router.get("/inventory-logs/{log_id}", response_model=InventoryLogResponse)
async def get_inventory_log_by_id(log_id: int):
    """Get inventory log by ID - USE ASYNCPG DIRECTLY"""
    conn = await get_asyncpg_connection()
    try:
        query = """
        SELECT id, chemical_id, action_type, quantity, timestamp 
        FROM inventory_logs 
        WHERE id = $1
        """
        row = await conn.fetchrow(query, log_id)
        if not row:
            raise HTTPException(status_code=404, detail="Inventory log not found")
        
        return {
            "id": row["id"],
            "chemical_id": row["chemical_id"],
            "action_type": row["action_type"],
            "quantity": row["quantity"],
            "timestamp": row["timestamp"]
        }
    finally:
        await conn.close()