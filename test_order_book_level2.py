#!/usr/bin/env python3
import json
from datetime import datetime
from ripio_api_utils import make_request, get_api_credentials

def get_order_book_level2(api_key, api_secret, pair, limit=None, aggregation=None):
    """Get order book level 2 data from Ripio Trade API.
    
    Args:
        api_key: API key
        api_secret: API secret
        pair: Currency pair code (e.g., 'BTCUSD')
        limit: Optional limit for number of orders to return
        aggregation: Optional price aggregation level
        
    Returns:
        dict: API response with order book data
    """
    endpoint = "/book/orders/level-2"
    
    # Add query parameters
    params = {'pair': pair}
    if limit:
        params['limit'] = limit
    if aggregation:
        params['aggregation'] = aggregation
    
    print(f"\nGetting order book level 2 data for {pair}...")
    if limit:
        print(f"Limit: {limit}")
    if aggregation:
        print(f"Aggregation: {aggregation}")
    
    # Make the request using the utility function
    return make_request(api_key, api_secret, "GET", endpoint, params=params)

def display_order_book(order_book_data):
    """Display order book data in a readable format.
    
    Args:
        order_book_data: Order book data from API response
    """
    if not order_book_data or 'data' not in order_book_data:
        print("No order book data to display")
        return
    
    data = order_book_data['data']
    
    # Extract bids and asks
    bids = data.get('bids', [])
    asks = data.get('asks', [])
    
    # Display pair and timestamp
    pair = data.get('pair', 'Unknown')
    timestamp = data.get('timestamp', 'Unknown')
    
    print("\n===== ORDER BOOK LEVEL 2 =====")
    print(f"Pair: {pair}")
    print(f"Timestamp: {timestamp}")
    print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("==============================")
    
    # Display bids
    print("\n----- BIDS (Buy Orders) -----")
    if not bids:
        print("No bids found")
    else:
        print(f"{'Price':<15} {'Amount':<15} {'Count':<10}")
        print("-" * 40)
        for bid in bids:
            price = bid.get('price', 'N/A')
            amount = bid.get('amount', 'N/A')
            count = bid.get('count', 'N/A')
            print(f"{price:<15} {amount:<15} {count:<10}")
    
    # Display asks
    print("\n----- ASKS (Sell Orders) -----")
    if not asks:
        print("No asks found")
    else:
        print(f"{'Price':<15} {'Amount':<15} {'Count':<10}")
        print("-" * 40)
        for ask in asks:
            price = ask.get('price', 'N/A')
            amount = ask.get('amount', 'N/A')
            count = ask.get('count', 'N/A')
            print(f"{price:<15} {amount:<15} {count:<10}")
    
    print("\n==============================")

def test_order_book_level2():
    """Test getting order book level 2 data from Ripio Trade API."""
    # Get API credentials from environment variables
    api_key, api_secret = get_api_credentials()
    
    if not api_key or not api_secret:
        return False
    
    print("===== RIPIO TRADE ORDER BOOK TEST =====")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("======================================")
    
    # Get order book data for BTC/USDC pair
    pair = "BTC_USDC"  # Bitcoin/USDC
    limit = 10  # Get top 10 orders on each side
    
    # Get the order book data
    order_book_data = get_order_book_level2(api_key, api_secret, pair, limit)
    
    if not order_book_data:
        print("Test failed: Could not retrieve order book data")
        return False
    
    # Display the order book data
    display_order_book(order_book_data)
    
    print("\nTest completed successfully!")
    return True

if __name__ == "__main__":
    print("Testing Ripio Trade order book level 2 data retrieval...")
    success = test_order_book_level2()
    
    if success:
        print("\nTest completed successfully!")
    else:
        print("\nTest failed!")
