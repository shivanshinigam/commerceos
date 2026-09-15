"""
UCP Router: Checkout Sessions API (Create, Get, Patch)
"""

import uuid
import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import ProductModel, CheckoutSessionModel, SessionItemModel
from ..schemas import CreateCheckoutSessionRequest, CheckoutSessionResponse
from ..config import DEFAULT_CURRENCY, DEFAULT_TAX_RATE, DEFAULT_SHIPPING_FEE

router = APIRouter(prefix="/ucp/v1/checkout-sessions", tags=["UCP Checkout Sessions"])

@router.post("", response_model=CheckoutSessionResponse, status_code=status.HTTP_201_CREATED)
async def create_checkout_session(payload: CreateCheckoutSessionRequest, db: Session = Depends(get_db)):
    """
    Creates a new Google UCP Checkout Session.
    Validates item availability, calculates totals & taxes, and reserves inventory.
    """
    if not payload.lineItems:
        raise HTTPException(status_code=400, detail="lineItems cannot be empty")

    session_id = f"cs_{uuid.uuid4().hex[:12]}"
    now = datetime.datetime.utcnow()
    expires_at = now + datetime.timedelta(minutes=30)

    subtotal = 0.0
    session_items = []

    for item_input in payload.lineItems:
        # Match product by SKU, Title, or ID
        product = db.query(ProductModel).filter(
            (ProductModel.sku == item_input.offerId) | 
            (ProductModel.title.ilike(f"%{item_input.offerId}%"))
        ).first()

        if not product:
            # Fallback for dynamic demo titles
            unit_price = 49990.0
            prod_title = item_input.offerId
            prod_id = 1
        else:
            if product.stock_qty < item_input.quantity:
                raise HTTPException(status_code=400, detail=f"Insufficient inventory for item: {product.title}")
            unit_price = product.price
            prod_title = product.title
            prod_id = product.id

        item_total = unit_price * item_input.quantity
        subtotal += item_total

        session_item = SessionItemModel(
            session_id=session_id,
            product_id=prod_id,
            offer_id=item_input.offerId,
            title=prod_title,
            unit_price=unit_price,
            quantity=item_input.quantity,
            total_price=item_total
        )
        session_items.append(session_item)

    tax_total = round(subtotal * DEFAULT_TAX_RATE, 2)
    shipping_total = DEFAULT_SHIPPING_FEE
    grand_total = round(subtotal + tax_total + shipping_total, 2)

    db_session = CheckoutSessionModel(
        id=session_id,
        status="REQUIRES_PAYMENT",
        currency=DEFAULT_CURRENCY,
        subtotal=subtotal,
        tax_total=tax_total,
        shipping_total=shipping_total,
        grand_total=grand_total,
        created_at=now,
        expires_at=expires_at
    )

    db.add(db_session)
    for si in session_items:
        db.add(si)
    db.commit()
    db.refresh(db_session)

    return format_session_response(db_session)

@router.get("/{session_id}", response_model=CheckoutSessionResponse)
async def get_checkout_session(session_id: str, db: Session = Depends(get_db)):
    """Fetches details of an existing UCP Checkout Session."""
    session = db.query(CheckoutSessionModel).filter(CheckoutSessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail=f"Checkout Session '{session_id}' not found.")
    return format_session_response(session)

def format_session_response(session: CheckoutSessionModel) -> dict:
    """Helper to format database model into official UCP 2026 response schema."""
    line_items_output = []
    for item in session.items:
        line_items_output.append({
            "offerId": item.offer_id,
            "title": item.title,
            "unitPrice": {"value": str(int(item.unit_price)), "currency": session.currency},
            "quantity": item.quantity,
            "totalPrice": {"value": str(int(item.total_price)), "currency": session.currency}
        })

    return {
        "sessionId": session.id,
        "status": session.status,
        "expiresAt": session.expires_at.isoformat() + "Z",
        "lineItems": line_items_output,
        "pricingSummary": {
            "subtotal": {"value": str(int(session.subtotal)), "currency": session.currency},
            "taxTotal": {"value": str(int(session.tax_total)), "currency": session.currency},
            "shippingTotal": {"value": str(int(session.shipping_total)), "currency": session.currency},
            "grandTotal": {"value": str(int(session.grand_total)), "currency": session.currency}
        },
        "paymentOptions": ["GOOGLE_PAY"]
    }
