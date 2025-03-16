#!/usr/bin/env python3
import os
import asyncio
import json
import websockets
import requests
import base64
import hmac
import hashlib
import time
from datetime import datetime

# WebSocket URL
WSS_URL = "wss://ws.ripiotrade.co"

async def get_websocket_ticket(api_key, api_secret):
    """
    Get a WebSocket ticket by making an authenticated REST API call
    """
    # API endpoint for getting a WebSocket ticket
    base_url = "https://api.ripiotrade.co/v4"
    endpoint = "/ticket"
    url = base_url + endpoint
    
    # Create authentication headers (same as in test_ripio_api.py)
    timestamp = str(int(time.time() * 1000))
    method = "POST"
    path = "ticket"
    
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
    
    print(f"Making request to {url} to get WebSocket ticket...")
    
    try:
        # Make the request
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        
        # Parse the response
        data = response.json()
        
        if 'data' in data and 'ticket' in data['data']:
            ticket = data['data']['ticket']
            print(f"Successfully obtained WebSocket ticket: {ticket[:10]}...")
            return ticket
        else:
            print(f"Unexpected response format: {json.dumps(data, indent=2)}")
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

async def connect_and_subscribe(ticket, api_key, api_secret):
    """
    Connect to WebSocket and subscribe to a private channel using the ticket
    """
    try:
        # Create authentication headers for WebSocket connection
        timestamp = str(int(time.time() * 1000))
        method = "GET"  # WebSocket connection typically uses GET
        path = "ws"
        
        # Create signature (timestamp + method + '/v4/' + path)
        message = timestamp + method + '/v4/' + path
        signature = base64.b64encode(
            hmac.new(
                api_secret.encode(),
                message.encode(),
                hashlib.sha256
            ).digest()
        ).decode()
        
        # Create headers for WebSocket connection
        headers = {
            'Authorization': api_key,
            'timestamp': timestamp,
            'signature': signature,
        }
        
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
    api_key = os.environ.get('RIPIO_API_KEY')
    api_secret = os.environ.get('RIPIO_API_SECRET')
    
    if not api_key or not api_secret:
        print("Error: RIPIO_API_KEY and RIPIO_API_SECRET environment variables must be set")
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
