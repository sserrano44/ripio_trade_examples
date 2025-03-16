#!/usr/bin/env python3
import os
import base64
import hmac
import hashlib
import time
import json
import requests
from datetime import datetime

def get_balances():
    # Get API credentials from environment variables
    api_key = os.environ.get('RIPIO_API_KEY')
    api_secret = os.environ.get('RIPIO_API_SECRET')
    
    if not api_key or not api_secret:
        print("Error: RIPIO_API_KEY and RIPIO_API_SECRET environment variables must be set")
        return False
    
    # API endpoint for fetching balances
    base_url = "https://api.ripiotrade.co/v4"
    endpoint = "/user/balances/"
    url = base_url + endpoint
    
    # Create authentication headers
    timestamp = str(int(time.time() * 1000))
    method = "GET"
    path = "user/balances/"
    
    # Create signature (timestamp + method + '/v4/' + path)
    message = timestamp + method + '/v4/' + path
    signature = base64.b64encode(
        hmac.new(
            api_secret.encode(),
            message.encode(),
            hashlib.sha256
        ).digest()
    ).decode()
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': api_key,
        'timestamp': timestamp,
        'signature': signature,
    }
    
    try:
        # Make the request
        print(f"Making request to {url} with authentication...")
        print(f"Headers: Authorization: {api_key[:5]}...{api_key[-5:] if len(api_key) > 10 else ''}")
        print(f"         timestamp: {timestamp}")
        print(f"         signature: {signature[:10]}...")
        
        response = requests.get(url, headers=headers)
        
        # Print response status
        print(f"\nResponse status code: {response.status_code}")
        
        if response.status_code == 200:
            print("Authentication successful!")
            
            # Parse the response
            data = response.json()
            
            if 'data' in data:
                balances = data['data']
                
                # Print balances
                print("\n===== RIPIO ACCOUNT BALANCES =====")
                print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print("=================================")
                
                if not balances:
                    print("No balances found.")
                else:
                    # Format as a table
                    print(f"{'Currency':<10} {'Available':<15} {'Locked':<15} {'Last Update':<25}")
                    print("-" * 65)
                    
                    for balance in balances:
                        currency = balance.get('currency_code', 'N/A')
                        available = float(balance.get('available_amount', 0))
                        locked = float(balance.get('locked_amount', 0))
                        last_update = balance.get('last_update', 'N/A')
                        
                        print(f"{currency:<10} {available:<15.8f} {locked:<15.8f} {last_update:<25}")
                    
                    print("=================================")
            else:
                print("Unexpected response format:")
                print(json.dumps(data, indent=2))
            
            return True
        else:
            print("Authentication failed!")
            try:
                error_data = response.json()
                print(f"Error response: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Error response text: {response.text}")
            
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response status code: {e.response.status_code}")
            try:
                error_data = e.response.json()
                print(f"Error response: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Error response text: {e.response.text}")
        
        return False

if __name__ == "__main__":
    print("Testing Ripio authentication and getting balances...")
    success = get_balances()
    
    if success:
        print("\nTest completed successfully!")
    else:
        print("\nTest failed!")
