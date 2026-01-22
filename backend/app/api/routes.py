from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import logging
from ..services.ai_service import ai_service
from ..services.analytics_service import analytics_service
from ..services.zabbix_service import zabbix_service

logger = logging.getLogger(__name__)

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    context_filter: Optional[str] = None

class ChatResponse(BaseModel):
    reply: str

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # Fetch context from Zabbix to pass to AI
    context = {}
    
    try:
        # Get active problems
        problems = zabbix_service.get_problems()
        if problems:
            context["active_problems_count"] = len(problems)
            context["active_problems"] = []
            for problem in problems[:10]:  # Limit to 10 most recent
                context["active_problems"].append({
                    "name": problem.get("name", "Unknown"),
                    "severity": problem.get("severity", "0"),
                    "age": problem.get("age", "Unknown"),
                    "acknowledged": problem.get("acknowledged", "0")
                })
        
        # Get hosts summary
        hosts = zabbix_service.get_hosts()
        if hosts:
            context["total_hosts"] = len(hosts)
            context["hosts_summary"] = []
            for host in hosts[:5]:  # First 5 hosts
                context["hosts_summary"].append({
                    "name": host.get("name", "Unknown"),
                    "status": "Enabled" if host.get("status") == "0" else "Disabled"
                })
    except Exception as e:
        logger.error(f"Error fetching Zabbix context: {e}")
        context["error"] = f"Could not connect to Zabbix: {str(e)}"

    response = ai_service.chat(request.message, context)
    return ChatResponse(reply=response)

@router.get("/analytics/predictions")
async def get_predictions():
    return analytics_service.predict_failures()

@router.get("/status")
async def get_zabbix_status():
    try:
        # Check connection
        hosts = zabbix_service.get_hosts()
        return {"connected": True, "host_count": len(hosts)}
    except Exception as e:
        return {"connected": False, "error": str(e)}
