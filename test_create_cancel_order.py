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
    
    return headers

def create_order(api_key, api_secret, pair, side, order_type, amount, price, 
                 external_id=None, post_only=False, immediate_or_cancel=False, 
                 fill_or_kill=False, expiration=None):
    """Create a new order on Ripio Trade.
    
    Args:
        api_key: API key
        api_secret: API secret
        pair: Currency pair code (e.g., 'BTCUSD')
        side: Order side ('buy' or 'sell')
        order_type: Order type ('limit', 'market')
        amount: Order amount
        price: Order price
        external_id: Optional external identifier
        post_only: If True, order will be added to order book without matching
        immediate_or_cancel: If True, order will be canceled if not filled immediately
        fill_or_kill: If True, order will be either completely filled or canceled
        expiration: Optional expiration timestamp
        
    Returns:
        dict: API response with order details
    """
    base_url = "https://api.ripiotrade.co/v4"
    endpoint = "/orders"
    url = base_url + endpoint
    path = "/v4" + endpoint
    method = "POST"
    
    # Prepare order data
    order_data = {
        "pair": pair,
        "side": side,
        "type": order_type,
        "amount": str(amount),
        "price": str(price)
    }
    
    # Add optional parameters if provided
    if external_id:
        order_data["external_id"] = external_id
    if post_only:
        order_data["post_only"] = True
    if immediate_or_cancel:
        order_data["immediate_or_cancel"] = True
    if fill_or_kill:
        order_data["fill_or_kill"] = True
    if expiration:
        order_data["expiration"] = expiration
    
    # Convert order data to JSON
    payload = json.dumps(order_data, separators=(',', ':'))
    
    # Create authentication headers
    headers = create_auth_headers(api_key, api_secret, method, path, payload)
    
    print(f"\nCreating {order_type} {side} order for {pair}...")
    print(f"Amount: {amount}, Price: {price}")
    
    try:
        # Make the request
        response = requests.post(url, headers=headers, data=payload)
        
        # Print response status
        print(f"Response status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Order created successfully!")
            return data
        else:
            print("Failed to create order!")
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

def cancel_order(api_key, api_secret, order_id):
    """Cancel an existing order on Ripio Trade.
    
    Args:
        api_key: API key
        api_secret: API secret
        order_id: ID of the order to cancel
        
    Returns:
        dict: API response with cancellation details
    """
    base_url = "https://api.ripiotrade.co/v4"
    endpoint = "/orders"
    url = base_url + endpoint
    path = "/v4" + endpoint
    method = "DELETE"
    
    # Prepare cancel data
    cancel_data = {
        "id": order_id
    }
    
    # Convert cancel data to JSON
    payload = json.dumps(cancel_data, separators=(',', ':'))
    
    # Create authentication headers
    headers = create_auth_headers(api_key, api_secret, method, path, payload)
    
    print(f"\nCanceling order with ID: {order_id}...")
    
    try:
        # Make the request
        response = requests.delete(url, headers=headers, data=payload)
        
        # Print response status
        print(f"Response status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Order canceled successfully!")
            return data
        else:
            print("Failed to cancel order!")
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

def test_create_and_cancel_order():
    """Test creating and canceling an order on Ripio Trade."""
    # Get API credentials from environment variables
    api_key = os.environ.get('RIPIO_API_KEY')
    api_secret = os.environ.get('RIPIO_API_SECRET')
    
    if not api_key or not api_secret:
        print("Error: RIPIO_API_KEY and RIPIO_API_SECRET environment variables must be set")
        return False
    
    print("===== RIPIO TRADE ORDER TEST =====")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=================================")
    
    # Create a test order (limit buy order)
    pair = "USDC_ARS"  # USDC/Argentine Peso
    side = "buy"
    order_type = "limit"
    amount = 10  # Buy 10 USDC
    price = 1200  # At 1200 ARS per USDC
    
    # Create the order
    create_response = create_order(
        api_key, 
        api_secret, 
        pair, 
        side, 
        order_type, 
        amount, 
        price,
        external_id=f"test-{int(time.time())}",  # Use timestamp as external ID
        post_only=True  # Ensure the order just goes to the order book
    )
    
    if not create_response or 'data' not in create_response:
        print("Test failed: Could not create order")
        return False
    
    # Extract order details
    order_data = create_response['data']
    order_id = order_data.get('id')
    
    if not order_id:
        print("Test failed: Order created but no ID returned")
        return False
    
    # Display order details
    print("\n----- Created Order Details -----")
    print(f"Order ID: {order_id}")
    print(f"Pair: {order_data.get('pair')}")
    print(f"Side: {order_data.get('side')}")
    print(f"Type: {order_data.get('type')}")
    print(f"Amount: {order_data.get('amount')}")
    print(f"Price: {order_data.get('price')}")
    print(f"Status: {order_data.get('status')}")
    print("--------------------------------")
    
    # Wait a moment before canceling
    print("\nWaiting 2 seconds before canceling...")
    time.sleep(2)
    
    # Cancel the order
    cancel_response = cancel_order(api_key, api_secret, order_id)
    
    if not cancel_response or 'data' not in cancel_response:
        print("Test failed: Could not cancel order")
        return False
    
    # Extract cancellation details
    cancel_data = cancel_response['data']
    
    # Display cancellation details
    print("\n----- Cancellation Details -----")
    print(f"Order ID: {cancel_data.get('id')}")
    print(f"Status: {cancel_data.get('status', 'Unknown')}")
    print("--------------------------------")
    
    print("\nTest completed successfully!")
    return True

if __name__ == "__main__":
    print("Testing Ripio Trade order creation and cancellation...")
    success = test_create_and_cancel_order()
    
    if success:
        print("\nTest completed successfully!")
    else:
        print("\nTest failed!")
