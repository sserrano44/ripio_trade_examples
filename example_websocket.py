#!/usr/bin/env python3
import asyncio
import json
import websockets
import requests
import time
from datetime import datetime
from ripio_api_utils import make_request, get_api_credentials, create_auth_headers

# WebSocket URL
WSS_URL = "wss://ws.ripiotrade.co"

async def get_websocket_ticket(api_key, api_secret):
    """
    Get a WebSocket ticket by making an authenticated REST API call
    """
    # API endpoint for getting a WebSocket ticket
    endpoint = "/ticket"
    
    print(f"Making request to get WebSocket ticket...")
    
    # Make the request using the utility function
    response = make_request(api_key, api_secret, "POST", endpoint)
    
    if response and 'data' in response and 'ticket' in response['data']:
        ticket = response['data']['ticket']
        print(f"Successfully obtained WebSocket ticket: {ticket[:10]}...")
        return ticket
    else:
        print(f"Failed to get WebSocket ticket")
        return None

async def connect_and_subscribe(ticket, api_key, api_secret):
    """
    Connect to WebSocket and subscribe to a private channel using the ticket
    """
    try:
        # Create authentication headers for WebSocket connection
        path = "ws"
        headers, timestamp = create_auth_headers(api_key, api_secret, "GET", path)
        
        print(f"Connecting to WebSocket at {WSS_URL} with authentication headers...")
        async with websockets.connect(WSS_URL, extra_headers=headers) as websocket:
            print("Connected to WebSocket")
            
            # Subscribe to balance channel with ticket
            balance_payload = {
                "method": "subscribe",
                "topics": ["balance"],
                "ticket": ticket,  # Include ticket for authentication
                "id": int(time.time() * 1000)
            }
            
            print(f"Subscribing to balance channel with ticket...")
            await websocket.send(json.dumps(balance_payload))
            
            # Wait for subscription response
            response = await websocket.recv()
            print(f"Subscription response: {response}")
            
            # Keep connection open for a while to receive updates
            print("Waiting for balance updates (will timeout after 3 seconds)...")
            for _ in range(3):  # Try to receive 3 messages or timeout
                try:
                    message = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                    print(f"Received message: {message}")
                except asyncio.TimeoutError:
                    print("No message received (timeout)")
            
            print("Test completed")
            
    except Exception as e:
        print(f"Error in WebSocket connection: {e}")

async def main():
    # Get API credentials from environment variables
    api_key, api_secret = get_api_credentials()
    
    if not api_key or not api_secret:
        return
    
    # Get a WebSocket ticket
    ticket = await get_websocket_ticket(api_key, api_secret)
    
    if ticket:
        # Connect to WebSocket and subscribe to a private channel
        await connect_and_subscribe(ticket, api_key, api_secret)
    else:
        print("Failed to get WebSocket ticket. Cannot proceed with WebSocket test.")

if __name__ == "__main__":
    print("Testing Ripio WebSocket authentication with ticket...")
    asyncio.run(main())
