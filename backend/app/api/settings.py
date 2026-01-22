from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from ..services.config_service import config_service

router = APIRouter()

class ConfigUpdate(BaseModel):
    provider: str
    aws_region: Optional[str] = None
    aws_access_key: Optional[str] = None
    aws_secret_key: Optional[str] = None
    bedrock_model_id: Optional[str] = None
    openai_api_key: Optional[str] = None
    openai_model: Optional[str] = None
    gemini_api_key: Optional[str] = None
    gemini_model: Optional[str] = None

@router.get("/config")
def get_config():
    # Return config but mask valid keys for security
    config = config_service.get_config()
    safe_config = config.copy()
    
    if safe_config.get("aws_secret_key"):
        safe_config["aws_secret_key"] = "********"
    if safe_config.get("openai_api_key"):
        safe_config["openai_api_key"] = "sk-..." + safe_config["openai_api_key"][-4:]
    if safe_config.get("gemini_api_key"):
        safe_config["gemini_api_key"] = "********"
        
    return safe_config

@router.post("/config")
def update_config(update: ConfigUpdate):
    current = config_service.get_config()
    
    # Update fields if provided
    current["provider"] = update.provider
    
    if update.aws_region: current["aws_region"] = update.aws_region
    if update.aws_access_key: current["aws_access_key"] = update.aws_access_key
    if update.aws_secret_key and update.aws_secret_key != "********": 
        current["aws_secret_key"] = update.aws_secret_key
    if update.bedrock_model_id: current["bedrock_model_id"] = update.bedrock_model_id
        
    if update.openai_api_key and not update.openai_api_key.startswith("sk-..."): 
        current["openai_api_key"] = update.openai_api_key
    if update.openai_model: current["openai_model"] = update.openai_model
        
    if update.gemini_api_key and update.gemini_api_key != "********": 
        current["gemini_api_key"] = update.gemini_api_key
    if update.gemini_model: current["gemini_model"] = update.gemini_model
    
    try:
        config_service.save_config(current)
        return {"status": "success", "message": "Configuration updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
