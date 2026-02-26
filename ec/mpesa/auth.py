import requests
import os
from requests.auth import HTTPBasicAuth

def get_access_token():
    """
    Fetches an access token from Safaricom M-Pesa API.
    """
    # Determine the API base URL
    environment = os.getenv("MPESA_ENVIRONMENT", "sandbox")
    base_url = "https://sandbox.safaricom.co.ke" if environment == "sandbox" else "https://api.safaricom.co.ke"
    
    url = f"{base_url}/oauth/v1/generate?grant_type=client_credentials"
    consumer_key = os.getenv("MPESA_CONSUMER_KEY")
    consumer_secret = os.getenv("MPESA_CONSUMER_SECRET")

    response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret))

    if response.status_code == 200:
        access_token = response.json().get("access_token")
        return access_token
    else:
        raise Exception("Failed to obtain access token: " + response.text)
