"""
UCP Router: GET /.well-known/ucp (Merchant Publisher Profile Endpoint)
"""

from fastapi import APIRouter
from ..config import UCP_VERSION, MERCHANT_NAME, MERCHANT_DOMAIN, SUPPORTED_CAPABILITIES

router = APIRouter()

@router.get("/.well-known/ucp", summary="Google UCP Capability Discovery Profile")
async def get_ucp_profile():
    """
    Standard Google UCP profile discovery route.
    Read by Gemini crawler to verify merchant's direct_buying capability.
    """
    return {
        "@context": "https://schema.org",
        "@type": "MerchantPublisherProfile",
        "name": MERCHANT_NAME,
        "ucp": {
            "version": UCP_VERSION,
            "capabilities": SUPPORTED_CAPABILITIES,
            "checkoutSessionsEndpoint": f"{MERCHANT_DOMAIN}/ucp/v1/checkout-sessions",
            "paymentMethods": ["GOOGLE_PAY"]
        }
    }
