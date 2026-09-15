"""
Automated Integration Test Suite for UCP Backend Server
Executes end-to-end UCP 2026 Protocol verification.
"""

import requests
import time

BASE_URL = "http://127.0.0.1:8000"

def run_tests():
    print("=" * 60)
    print("   RUNNING AUTOMATED UCP 2026 PROTOCOL INTEGRATION TESTS")
    print("=" * 60)

    # 1. Health Check
    res = requests.get(f"{BASE_URL}/")
    assert res.status_code == 200, "Health check failed"
    print("✅ 1. Health Check OK:", res.json()["service"])

    # 2. UCP Profile Discovery
    res = requests.get(f"{BASE_URL}/.well-known/ucp")
    assert res.status_code == 200, "Profile endpoint failed"
    profile = res.json()
    assert profile["@type"] == "MerchantPublisherProfile", "Invalid profile type"
    assert "direct_buying" in profile["ucp"]["capabilities"], "direct_buying capability missing"
    print("✅ 2. Merchant UCP Profile Verified:")
    print("   Version:", profile["ucp"]["version"])
    print("   Capabilities:", profile["ucp"]["capabilities"])

    # 3. Create Checkout Session
    payload = {
        "lineItems": [
            {"offerId": "SKU-IPH15-128", "quantity": 1}
        ],
        "userContext": {
            "locale": "en-IN",
            "currency": "INR",
            "email": "customer@example.com"
        }
    }
    res = requests.post(f"{BASE_URL}/ucp/v1/checkout-sessions", json=payload)
    assert res.status_code == 201, f"Create session failed: {res.text}"
    session = res.json()
    session_id = session["sessionId"]
    assert session["status"] == "REQUIRES_PAYMENT", "Invalid session status"
    print("✅ 3. UCP Checkout Session Created:")
    print("   SessionID:", session_id)
    print("   Status:", session["status"])
    print("   Grand Total:", session["pricingSummary"]["grandTotal"]["value"], session["pricingSummary"]["grandTotal"]["currency"])

    # 4. Get Checkout Session Details
    res = requests.get(f"{BASE_URL}/ucp/v1/checkout-sessions/{session_id}")
    assert res.status_code == 200, "Get session failed"
    print("✅ 4. Session Retrieval Verified:", res.json()["sessionId"])

    # 5. Complete Order Settlement
    complete_payload = {
        "paymentToken": "tok_gp_demo_987654321",
        "paymentMethod": "GOOGLE_PAY"
    }
    res = requests.post(f"{BASE_URL}/ucp/v1/checkout-sessions/{session_id}/complete", json=complete_payload)
    assert res.status_code == 200, f"Complete session failed: {res.text}"
    order = res.json()
    assert order["status"] == "COMPLETED", "Order completion status failed"
    print("✅ 5. UCP Order Settlement Complete:")
    print("   OrderId:", order["orderId"])
    print("   Status:", order["status"])
    print("   Total Paid:", order["totalPaid"]["value"], order["totalPaid"]["currency"])

    print("\n🎉 ALL 5 UCP PROTOCOL INTEGRATION TESTS PASSED CLEANLY!")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
