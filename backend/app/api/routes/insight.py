from fastapi import APIRouter
from app.services.knowledge_base import knowledge_base
from app.utils.logger import get_logs

router = APIRouter(prefix="/insight", tags=["insight"])

@router.get("/stats")
async def get_stats():
    """Get knowledge base statistics"""
    return knowledge_base.get_summary_stats()

@router.get("/logs")
async def get_app_logs(lines: int = 100):
    """Get application logs"""
    return {"logs": get_logs(lines)}
