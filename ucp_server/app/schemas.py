"""
Pydantic Schemas for Google Universal Commerce Protocol (UCP 2026-04-08 Spec)
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# --- UCP PROFILE SCHEMAS ---
class UcpMetaSchema(BaseModel):
    version: str = "2026-04-08"
    capabilities: List[str]
    checkoutSessionsEndpoint: str
    paymentMethods: List[str]

class MerchantProfileSchema(BaseModel):
    context: str = Field("https://schema.org", alias="@context")
    type: str = Field("MerchantPublisherProfile", alias="@type")
    name: str
    ucp: UcpMetaSchema

# --- CHECKOUT SESSION SCHEMAS ---
class LineItemInput(BaseModel):
    offerId: str
    quantity: int = Field(1, ge=1)

class UserContextInput(BaseModel):
    locale: Optional[str] = "en-IN"
    currency: Optional[str] = "INR"
    email: Optional[str] = "customer@example.com"
    shippingAddress: Optional[Dict[str, str]] = None

class CreateCheckoutSessionRequest(BaseModel):
    lineItems: List[LineItemInput]
    userContext: Optional[UserContextInput] = None

class SessionLineItemOutput(BaseModel):
    offerId: str
    title: str
    unitPrice: Dict[str, Any]
    quantity: int
    totalPrice: Dict[str, Any]

class PricingSummaryOutput(BaseModel):
    subtotal: Dict[str, Any]
    taxTotal: Dict[str, Any]
    shippingTotal: Dict[str, Any]
    grandTotal: Dict[str, Any]

class CheckoutSessionResponse(BaseModel):
    sessionId: str
    status: str  # REQUIRES_PAYMENT, COMPLETED, EXPIRED
    expiresAt: str
    lineItems: List[SessionLineItemOutput]
    pricingSummary: PricingSummaryOutput
    paymentOptions: List[str]

# --- SESSION COMPLETE & ORDER SCHEMAS ---
class CompleteSessionRequest(BaseModel):
    paymentToken: str
    paymentMethod: str = "GOOGLE_PAY"

class OrderConfirmationResponse(BaseModel):
    orderId: str
    sessionId: str
    status: str
    completedAt: str
    totalPaid: Dict[str, Any]
    paymentMethod: str
