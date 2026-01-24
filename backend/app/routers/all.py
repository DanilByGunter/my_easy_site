from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.services.all_data import AllDataService

router = APIRouter()


@router.get("/api/v1/all")
async def get_all_data(db: AsyncSession = Depends(get_db)):
    """Get all site data in frontend-compatible format"""
    service = AllDataService(db)
    return await service.get_all_data()
