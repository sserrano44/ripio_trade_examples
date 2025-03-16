#!/usr/bin/env python3
import time
import json
from datetime import datetime
from ripio_api_utils import make_request, get_api_credentials

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
    endpoint = "/orders"
    
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
    
    print(f"\nCreating {order_type} {side} order for {pair}...")
    print(f"Amount: {amount}, Price: {price}")
    
    # Make the request using the utility function
    response = make_request(api_key, api_secret, "POST", endpoint, data=order_data)
    
    if response:
        print("Order created successfully!")
    else:
        print("Failed to create order!")
        
    return response

def cancel_order(api_key, api_secret, order_id):
    """Cancel an existing order on Ripio Trade.
    
    Args:
        api_key: API key
        api_secret: API secret
        order_id: ID of the order to cancel
        
    Returns:
        dict: API response with cancellation details
    """
    endpoint = "/orders"
    
    # Prepare cancel data
    cancel_data = {
        "id": order_id
    }
    
    print(f"\nCanceling order with ID: {order_id}...")
    
    # Make the request using the utility function
    response = make_request(api_key, api_secret, "DELETE", endpoint, data=cancel_data)
    
    if response:
        print("Order canceled successfully!")
    else:
        print("Failed to cancel order!")
        
    return response

def test_create_and_cancel_order():
    """Test creating and canceling an order on Ripio Trade."""
    # Get API credentials from environment variables
    api_key, api_secret = get_api_credentials()
    
    if not api_key or not api_secret:
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
