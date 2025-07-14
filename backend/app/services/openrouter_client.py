from app.core.logger import logger
logger.info("service/openrouter_client enter")
import app.core.config 

from openai import OpenAI


#------------------------Model---------------------

async def assistant(messages:list):
    # print(app.core.config.get_api_key())
    client=OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=app.core.config.get_api_key(), 
    )
     
    try:
        response=client.chat.completions.create(
            model=app.core.config.default_model.model,
            messages=messages,
        )
        
        return response.choices[0].message.content 
    except Exception as e:
        logger.exception("OpenRouter call failed")
        return None 
    
logger.info("service/openrouter_client out") 