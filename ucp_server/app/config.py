"""
Google UCP Backend Server Configuration
Spec Version: 2026-04-08
"""

import os

# UCP Metadata
UCP_VERSION = "2026-04-08"
MERCHANT_NAME = "CommerceOS Merchant Labs"
MERCHANT_DOMAIN = "http://localhost:8000"
SUPPORTED_CAPABILITIES = ["direct_buying", "price_availability", "inventory_reservation"]
DEFAULT_CURRENCY = "INR"
DEFAULT_TAX_RATE = 0.18  # 18% GST for India
DEFAULT_SHIPPING_FEE = 150.0  # ₹150 standard shipping

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ucp_database.db")

# Google Pay & Payment Gateway Config
GOOGLE_PAY_MERCHANT_ID = os.getenv("GOOGLE_PAY_MERCHANT_ID", "BCR2DN6TZXXXXXXX")
ALLOW_DEMO_TOKENS = True
