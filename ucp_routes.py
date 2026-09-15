from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import time
from database import db

router = APIRouter(prefix="/ucp/v1")

class SearchIntent(BaseModel):
    category: Optional[str] = None
    budget: Optional[Dict[str, float]] = None

class SearchRequest(BaseModel):
    query: str
    intent: Optional[SearchIntent] = None

@router.post("/search")
async def ucp_search(req: SearchRequest):
    """
    Mock UCP Search Endpoint. 
    In reality, this would broadcast to multiple merchants.
    """
    cat = req.intent.category if req.intent else None
    max_price = req.intent.budget.get('max') if req.intent and req.intent.budget else None
    
    results = db.search_catalog(category=cat, max_price=max_price)
    
    # Format according to UCP schema
    formatted_results = []
    for item in results:
        # For simplicity, we just return the item as-is
        formatted_results.append(item)
        
    return {
        "status": "success",
        "results": formatted_results[:10], # limit to 10 for demo
        "metadata": {
            "merchants_queried": ["nova", "velomart", "urbancart"],
            "total_matches": len(results)
        }
    }

class CartItem(BaseModel):
    merchant_id: str
    product_id: str
    qty: int

class CartRequest(BaseModel):
    cart_id: Optional[str] = None
    items: List[CartItem]

@router.post("/cart")
async def ucp_cart(req: CartRequest):
    return {
        "status": "success",
        "cart_id": req.cart_id or f"cart_{int(time.time())}",
        "items": [item.dict() for item in req.items]
    }

class CheckoutPayload(BaseModel):
    shipping_address: Optional[Dict[str, Any]] = None
    payment_token: Optional[str] = None

class CheckoutRequest(BaseModel):
    cart_id: str
    action: str
    payload: Optional[CheckoutPayload] = None

@router.post("/checkout")
async def ucp_checkout(req: CheckoutRequest):
    if req.action == "INITIALIZE":
        return {"status": "success", "state": "AWAITING_SHIPPING"}
    elif req.action == "ADVANCE":
        if req.payload and req.payload.shipping_address:
            return {"status": "success", "state": "AWAITING_PAYMENT"}
        elif req.payload and req.payload.payment_token:
            return {"status": "success", "state": "AUTHORIZED", "order_id": f"ORD-{int(time.time())}"}
    return {"status": "error", "message": "Invalid state transition"}
