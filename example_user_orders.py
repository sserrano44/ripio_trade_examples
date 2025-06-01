#!/usr/bin/env python3
import json
from datetime import datetime
from ripio_api_utils import make_request, get_api_credentials

def get_user_orders(api_key, api_secret, status=None, pair=None, side=None, 
                   order_type=None, start_time=None, end_time=None, limit=None, 
                   offset=None):
    """Get user orders from Ripio Trade API with optional filters.
    
    Args:
        api_key: API key
        api_secret: API secret
        status: Optional filter by order status ('open', 'closed', 'canceled', etc.)
        pair: Optional filter by currency pair (e.g., 'BTCUSD')
        side: Optional filter by order side ('buy' or 'sell')
        order_type: Optional filter by order type ('limit', 'market')
        start_time: Optional filter by start time (ISO format)
        end_time: Optional filter by end time (ISO format)
        limit: Optional limit for number of orders to return
        offset: Optional offset for pagination
        
    Returns:
        dict: API response with user orders
    """
    endpoint = "/orders"
    
    # Add query parameters
    params = {}
    if status:
        params['status'] = status
    if pair:
        params['pair'] = pair
    if side:
        params['side'] = side
    if order_type:
        params['type'] = order_type
    if start_time:
        params['start_time'] = start_time
    if end_time:
        params['end_time'] = end_time
    if limit:
        params['limit'] = limit
    if offset:
        params['offset'] = offset
    
    print(f"\nGetting user orders...")
    if params:
        print("Filters applied:")
        for key, value in params.items():
            print(f"  {key}: {value}")
    
    # Make the request using the utility function
    return make_request(api_key, api_secret, "GET", endpoint, params=params)

def display_orders(orders_data):
    """Display orders data in a readable format.
    
    Args:
        orders_data: Orders data from API response
    """
    # Print the raw response for debugging
    print("\nAPI Response:")
    print(json.dumps(orders_data, indent=2))
    
    if not orders_data:
        print("No orders data to display")
        return
    
    # Check if 'data' key exists and has 'orders' key
    if 'data' not in orders_data:
        print("Unexpected response format: 'data' key not found")
        return
    
    if 'orders' not in orders_data['data']:
        print("Unexpected response format: 'orders' key not found in data")
        return
    
    orders = orders_data['data']['orders']
    
    print("\n===== USER ORDERS =====")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=======================")
    
    if not orders:
        print("No orders found.")
        return
    
    # Format as a table
    print(f"{'ID':<12} {'Pair':<10} {'Side':<6} {'Type':<8} {'Status':<10} {'Price':<15} {'Amount':<15} {'Filled':<15} {'Created At':<25}")
    print("-" * 120)
    
    for order in orders:
        # Get values with defaults and convert to string to ensure proper formatting
        order_id = str(order.get('id', 'N/A'))
        pair = str(order.get('pair', 'N/A'))
        side = str(order.get('side', 'N/A'))
        order_type = str(order.get('type', 'N/A'))
        status = str(order.get('status', 'N/A'))
        
        # Format numeric values
        try:
            price = float(order.get('price', 0))
            price_str = f"{price:.8f}"
        except (ValueError, TypeError):
            price_str = str(order.get('price', 'N/A'))
            
        try:
            amount = float(order.get('amount', 0))
            amount_str = f"{amount:.8f}"
        except (ValueError, TypeError):
            amount_str = str(order.get('amount', 'N/A'))
            
        try:
            filled = float(order.get('filled_amount', 0))
            filled_str = f"{filled:.8f}"
        except (ValueError, TypeError):
            filled_str = str(order.get('filled_amount', 'N/A'))
        
        created_at = str(order.get('created_at', 'N/A'))
        
        # Truncate long strings to fit in columns
        if len(order_id) > 11:
            order_id = order_id[:9] + ".."
        if len(pair) > 9:
            pair = pair[:7] + ".."
        if len(side) > 5:
            side = side[:3] + ".."
        if len(order_type) > 7:
            order_type = order_type[:5] + ".."
        if len(status) > 9:
            status = status[:7] + ".."
        if len(price_str) > 14:
            price_str = price_str[:12] + ".."
        if len(amount_str) > 14:
            amount_str = amount_str[:12] + ".."
        if len(filled_str) > 14:
            filled_str = filled_str[:12] + ".."
        if len(created_at) > 24:
            created_at = created_at[:22] + ".."
        
        print(f"{order_id:<12} {pair:<10} {side:<6} {order_type:<8} {status:<10} {price_str:<15} {amount_str:<15} {filled_str:<15} {created_at:<25}")
    
    print("=======================")

def test_get_user_orders():
    """Test getting user orders from Ripio Trade API."""
    # Get API credentials from environment variables
    api_key, api_secret = get_api_credentials()
    
    if not api_key or not api_secret:
        return False
    
    print("===== RIPIO TRADE USER ORDERS TEST =====")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=======================================")
    
    # Example 1: Get all orders for a specific pair
    # Note: The API requires a pair parameter
    print("\nExample 1: Getting all user orders for USDC/ARS pair...")
    all_orders = get_user_orders(api_key, api_secret, pair="USDC_ARS")
    
    if not all_orders:
        print("Test failed: Could not retrieve user orders")
        return False
    
    display_orders(all_orders)
    
    # Example 2: Get open orders for a specific pair
    print("\nExample 2: Getting open orders for USDC/ARS pair...")
    open_orders = get_user_orders(api_key, api_secret, status="open", pair="USDC_ARS")
    
    if not open_orders:
        print("Could not retrieve open orders")
    else:
        display_orders(open_orders)
    
    # Example 3: Get buy orders for a specific pair with limit
    print("\nExample 3: Getting buy orders for USDC/ARS pair (limit: 5)...")
    buy_orders = get_user_orders(api_key, api_secret, pair="USDC_ARS", side="buy", limit=5)
    
    if not buy_orders:
        print("Could not retrieve buy orders")
    else:
        display_orders(buy_orders)
    
    print("\nTest completed successfully!")
    return True

if __name__ == "__main__":
    print("Testing Ripio Trade user orders retrieval...")
    success = test_get_user_orders()
    
    if success:
        print("\nTest completed successfully!")
    else:
        print("\nTest failed!")
