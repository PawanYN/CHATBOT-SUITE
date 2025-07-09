from app.core.logger import logger
logger.info("mango enter")
import app.core.config 

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient(app.core.config.get_mango_uri())
db = client["chatbot_db"]

logger.info("mango out")