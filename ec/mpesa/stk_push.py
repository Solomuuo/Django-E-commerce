import requests
import base64
import json
import os
import logging
from datetime import datetime
from .auth import get_access_token

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
MPESA_ENVIRONMENT = os.getenv("MPESA_ENVIRONMENT", "sandbox")
MPESA_EXPRESS_SHORTCODE = os.getenv("MPESA_EXPRESS_SHORTCODE")
MPESA_PASSKEY = os.getenv("MPESA_PASSKEY")
CALLBACK_URL = os.getenv("CALLBACK_URL", "http://127.0.0.1:8000/mpesa/callback/")

# Set Safaricom API base URL
MPESA_BASE_URL = "https://sandbox.safaricom.co.ke" if MPESA_ENVIRONMENT == "sandbox" else "https://api.safaricom.co.ke"
LNM_API_URL = f"{MPESA_BASE_URL}/mpesa/stkpush/v1/processrequest"

def stk_push_request(amount, phone_number, receipt_number):
    """ Initiates an STK Push request """
    access_token = get_access_token()

    # Get Timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Generate Password
    password = base64.b64encode(f"{MPESA_EXPRESS_SHORTCODE}{MPESA_PASSKEY}{timestamp}".encode()).decode()

    # Construct request payload
    payload = {
        "BusinessShortCode": MPESA_EXPRESS_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": MPESA_EXPRESS_SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": "https://your-server.com/mpesa/stk_callback/",
        "AccountReference": receipt_number,  # This helps in tracking the transaction
        "TransactionDesc": "Payment for goods"
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(LNM_API_URL, json=payload, headers=headers)
    return response.json()