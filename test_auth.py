#!/usr/bin/env python3
import json
from datetime import datetime
from ripio_api_utils import make_request, get_api_credentials

def get_balances():
    """Get account balances from Ripio Trade API."""
    # Get API credentials from environment variables
    api_key, api_secret = get_api_credentials()
    
    if not api_key or not api_secret:
        return False
    
    # API endpoint for fetching balances
    endpoint = "/user/balances/"
    
    print(f"Making request to get balances with authentication...")
    
    # Make the request using the utility function
    response = make_request(api_key, api_secret, "GET", endpoint)
    
    if not response:
        print("Authentication failed!")
        return False
    
    print("Authentication successful!")
    
    # Parse the response
    if 'data' in response:
        balances = response['data']
        
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
        print(json.dumps(response, indent=2))
    
    return True

if __name__ == "__main__":
    print("Testing Ripio authentication and getting balances...")
    success = get_balances()
    
    if success:
        print("\nTest completed successfully!")
    else:
        print("\nTest failed!")
