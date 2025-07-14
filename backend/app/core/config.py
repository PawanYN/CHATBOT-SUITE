from app.core.logger import logger
logger.info("core/config enter")

from dotenv import load_dotenv
import os
from pydantic import BaseModel


#----------------------- 1. API Key ---------------------
load_dotenv(".env",override=True)

logger.debug("OPENROUTER_API_KEY (first 8 chars): %s", 
             os.getenv("OPENROUTER_API_KEY")[:8] if os.getenv("OPENROUTER_API_KEY") else "NONE")

def get_api_key():
    try:
      print(os.getenv("OPENROUTER_API_KEY"))
      return os.getenv("OPENROUTER_API_KEY")    
    except KeyError:
      logger.critical("OPENROUTER_API_KEY not found in .env — shutting down.")
      raise SystemExit(1)

# ----------------------2. Model Configuration -----------
class model_confi(BaseModel):
    
    # Required by OpenRouter
    model:str
    system_content:str
    
    #Common tuning knobs
    temperature: float = 0.7
    max_tokens: int = 1024
    stream: bool = False

#-----------------------3. different models--------------
GPT4O_MINI=model_confi(model="openai/gpt-4o-mini",system_content= "You are a good assistant, you answer the question very precisely")


#-----------------------4. Default model-----------------
default_model=GPT4O_MINI

logger.info("core/config out")



#--------------------MONGO_URI--------------
def get_mango_uri():
    try:
      return os.getenv("MONGO_URI")
    except KeyError:
      logger.critical("MONGO_URI not found in .env — shutting down.")
      raise SystemExit(1)