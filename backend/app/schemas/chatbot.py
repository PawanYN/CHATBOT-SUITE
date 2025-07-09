from app.core.logger import logger
logger.info("schema/chatbot enter")

from pydantic import BaseModel
from typing import Optional

class Createchat(BaseModel):
    messages:list[dict]
    session_id: Optional[str]

logger.info("schema/chatbot out")