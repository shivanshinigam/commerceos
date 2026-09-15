import os
import json
import asyncio
from fastapi import APIRouter, Request
from sse_starlette.sse import EventSourceResponse
from pydantic import BaseModel
import time

router = APIRouter(prefix="/api/agent")

class AgentRunRequest(BaseModel):
    query: str

async def stream_agent_run(query: str):
    """
    Generator that yields Server-Sent Events (SSE) representing
    the agent's thought process and final tool calls.
    """
    
    # 1. Initialize
    yield {"data": json.dumps({"type": "log", "msg": f"> Initializing agent for query: '{query}'..."})}
    await asyncio.sleep(1)
    
    # 2. Check for API key
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        yield {"data": json.dumps({
            "type": "error", 
            "msg": "GEMINI_API_KEY not found in environment. Please add it to your Hugging Face Space secrets to enable true LLM reasoning."
        })}
        
        # Fallback to deterministic mock if no key
        yield {"data": json.dumps({"type": "log", "msg": "> Falling back to deterministic simulation..."})}
        await asyncio.sleep(1)
        
        # Fake intent parsing
        intent = {"category": "running_shoes", "budget": {"max": 8000}}
        if "laptop" in query.lower():
            intent = {"category": "laptop", "budget": {"max": 80000}}
        elif "tv" in query.lower() or "television" in query.lower():
            intent = {"category": "tv", "budget": {"max": 60000}}
            
        yield {"data": json.dumps({"type": "log", "msg": f"[✓] Intent extracted: {json.dumps(intent)}", "status": "success"})}
        await asyncio.sleep(1)
        
        yield {"data": json.dumps({"type": "log", "msg": f"> Broadcasting SEARCH request to UCP network..."})}
        await asyncio.sleep(1)
        
        # Fake result completion
        yield {"data": json.dumps({"type": "complete", "intent": intent})}
        return

    from google import genai
    from google.genai import types
    from typing import List, Optional, Dict
    
    class IntentSchema(BaseModel):
        category: Optional[str]
        budget: Dict[str, float]
        brand_preference: List[str]
        size: Optional[str]
        surface: Optional[str]
        use_case: List[str]
        keywords: List[str]

    yield {"data": json.dumps({"type": "log", "msg": "> Connected to Gemini 2.5 Flash..."})}
    await asyncio.sleep(0.5)
    
    yield {"data": json.dumps({"type": "log", "msg": "> Parsing natural language to Universal Commerce Protocol JSON..."})}
    
    try:
        # We use asyncio.to_thread because the genai client might be blocking
        client = genai.Client(api_key=api_key)
        
        prompt = f"""
        Extract the shopping intent from this query: "{query}"
        
        Map it to the following fields:
        - category: e.g. 'running_shoes', 'laptop', 'tv', 'smartphone', 'headphones'
        - budget: dict with 'max' key if a price limit is specified. e.g. {{"max": 8000}}
        - brand_preference: list of brands
        - size: string if size specified
        - surface: 'road', 'trail', 'street' (for shoes mostly)
        - use_case: list of use cases (e.g. ['daily_running', 'office'])
        - keywords: list of other important keywords
        """
        
        def run_gemini():
            return client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=IntentSchema,
                    temperature=0.0
                )
            )
            
        response = await asyncio.to_thread(run_gemini)
        
        # The response is guaranteed to match the schema
        intent_dict = json.loads(response.text)
        
        # Ensure budget.max is a number or null, not 0 if empty
        if not intent_dict.get("budget"):
            intent_dict["budget"] = {"max": None}
            
        yield {"data": json.dumps({"type": "log", "msg": f"[✓] Intent parsed by Gemini: {json.dumps(intent_dict)}", "status": "success"})}
        
        # Fallback completion
        yield {"data": json.dumps({"type": "complete", "intent": intent_dict})}
        
    except Exception as e:
        yield {"data": json.dumps({"type": "error", "msg": f"Gemini Error: {str(e)}"})}


@router.post("/run")
async def agent_run(req: AgentRunRequest):
    return EventSourceResponse(stream_agent_run(req.query))
