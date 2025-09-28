from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.db import SessionLocal

router = APIRouter(tags=["health"])

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.get("/db-check")
async def check_db(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(text("SELECT 1"))
        value = result.scalar()
        return {"status": "ok", "db_response": value}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB connection failed: {str(e)}")
