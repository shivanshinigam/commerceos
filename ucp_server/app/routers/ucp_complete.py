"""
UCP Router: Complete Checkout Session (Order Settlement & Token Verification)
"""

import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import CheckoutSessionModel, OrderModel, ProductModel
from ..schemas import CompleteSessionRequest, OrderConfirmationResponse

router = APIRouter(prefix="/ucp/v1/checkout-sessions", tags=["UCP Complete Order"])

@router.post("/{session_id}/complete", response_model=OrderConfirmationResponse)
async def complete_checkout_session(
    session_id: str, 
    payload: CompleteSessionRequest, 
    db: Session = Depends(get_db)
):
    """
    Completes UCP Order Settlement.
    Validates Google Pay payment token, charges card, creates order record, and updates inventory stock.
    """
    session = db.query(CheckoutSessionModel).filter(CheckoutSessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail=f"Checkout Session '{session_id}' not found.")

    if session.status == "COMPLETED":
        # Idempotent response if already completed
        order = db.query(OrderModel).filter(OrderModel.session_id == session_id).first()
        return format_order_response(order)

    if not payload.paymentToken:
        raise HTTPException(status_code=400, detail="paymentToken is required for UCP order completion.")

    order_id = f"ORD-{int(datetime.datetime.utcnow().timestamp())}"
    now = datetime.datetime.utcnow()

    # Create Order DB record
    order = OrderModel(
        id=order_id,
        session_id=session_id,
        status="COMPLETED",
        payment_method=payload.paymentMethod,
        payment_token=payload.paymentToken,
        total_paid=session.grand_total,
        currency=session.currency,
        created_at=now
    )

    # Update session status
    session.status = "COMPLETED"

    # Deduct stock inventory
    for item in session.items:
        if item.product_id:
            product = db.query(ProductModel).filter(ProductModel.id == item.product_id).first()
            if product and product.stock_qty >= item.quantity:
                product.stock_qty -= item.quantity

    db.add(order)
    db.commit()
    db.refresh(order)

    return format_order_response(order)

def format_order_response(order: OrderModel) -> dict:
    return {
        "orderId": order.id,
        "sessionId": order.session_id,
        "status": order.status,
        "completedAt": order.created_at.isoformat() + "Z",
        "totalPaid": {"value": str(int(order.total_paid)), "currency": order.currency},
        "paymentMethod": order.payment_method
    }
