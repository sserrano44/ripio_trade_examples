#!/usr/bin/env python3
import os
import base64
import hmac
import hashlib
import time
import json
import requests
from datetime import datetime

def generate_signature(api_secret, timestamp, method, path, payload=""):
    """Generate signature for Ripio Trade API.
    
    Args:
        api_secret: API secret key
        timestamp: Current timestamp in milliseconds
        method: HTTP method (GET, POST, DELETE)
        path: API endpoint path
        payload: JSON payload for POST requests
        
    Returns:
        str: Base64 encoded signature
    """
    # Create message string: Timestamp + HTTP Method + Path + JSON Payload
    message = f"{timestamp}{method}{path}{payload}"
    
    # Create HMAC SHA256 signature
    signature = hmac.new(
        api_secret.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).digest()
    
    # Encode in Base64
    return base64.b64encode(signature).decode('utf-8')

def create_auth_headers(api_key, api_secret, method, path, payload=""):
    """Create authentication headers for Ripio Trade API.
    
    Args:
        api_key: API key
        api_secret: API secret
        method: HTTP method (GET, POST, DELETE)
        path: API endpoint path
        payload: JSON payload for POST requests
        
    Returns:
        dict: Headers for API request
    """
    timestamp = str(int(time.time() * 1000))
    
    signature = generate_signature(api_secret, timestamp, method, path, payload)
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': api_key,
        'timestamp': timestamp,
        'signature': signature,
    }
    
    return headers, timestamp

def make_request(api_key, api_secret, method, endpoint, params=None, data=None):
    """Make a request to Ripio Trade API with authentication.
    
    Args:
        api_key: API key
        api_secret: API secret
        method: HTTP method (GET, POST, DELETE)
        endpoint: API endpoint (should start with /)
        params: Query parameters for GET requests
        data: Data payload for POST/DELETE requests
        
    Returns:
        dict: API response
    """
    base_url = "https://api.ripiotrade.co/v4"
    url = base_url + endpoint
    path = "/v4" + endpoint
    
    # Prepare payload
    payload = ""
    if data:
        payload = json.dumps(data, separators=(',', ':'))
    
    # Create authentication headers
    headers, timestamp = create_auth_headers(api_key, api_secret, method, path, payload)
    
    try:
        # Make the request
        if method == "GET":
            response = requests.get(url, headers=headers, params=params)
        elif method == "POST":
            response = requests.post(url, headers=headers, data=payload)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, data=payload)
        else:
            print(f"Unsupported HTTP method: {method}")
            return None
        
        # Print response status
        print(f"Response status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"API request failed with status code: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error response: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Error response text: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response status code: {e.response.status_code}")
            try:
                error_data = e.response.json()
                print(f"Error response: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Error response text: {e.response.text}")
        return None

def get_api_credentials():
    """Get API credentials from environment variables.
    
    Returns:
        tuple: (api_key, api_secret) or (None, None) if not set
    """
    api_key = os.environ.get('RIPIO_API_KEY')
    api_secret = os.environ.get('RIPIO_API_SECRET')
    
    if not api_key or not api_secret:
        print("Error: RIPIO_API_KEY and RIPIO_API_SECRET environment variables must be set")
        return None, None
    
    return api_key, api_secret
