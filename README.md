# Ripio Trade API Examples

This repository contains Python examples for interacting with the [Ripio Trade API](https://apidocs.ripiotrade.co/). These examples demonstrate how to authenticate, retrieve market data, manage orders, and use WebSockets for real-time updates.

## Overview

Ripio Trade is a cryptocurrency exchange platform that provides a comprehensive API for trading and accessing market data. This repository includes examples for:

- Authentication and account information
- Market data retrieval (order book)
- Order management (create, cancel)
- User orders retrieval with filtering
- Real-time updates via WebSocket

## Prerequisites

- Python 3.6+
- Required packages:
  - `requests`
  - `websockets`
  - `asyncio`

You can install the required packages using pip:

```bash
pip install requests websockets asyncio
```

## Authentication

To use the Ripio Trade API, you need to:

1. Create an account on [Ripio Trade](https://www.ripiotrade.co/)
2. Generate API keys in your account settings
3. Set your API credentials as environment variables:

```bash
export RIPIO_API_KEY="your_api_key"
export RIPIO_API_SECRET="your_api_secret"
```

The examples in this repository use these environment variables to authenticate API requests.

## API Authentication Process

The Ripio Trade API uses HMAC-SHA256 signatures for authentication. The authentication process involves:

1. Creating a message string: `timestamp + HTTP Method + Path + JSON Payload`
2. Generating an HMAC-SHA256 signature using your API secret
3. Encoding the signature in Base64
4. Including the API key, timestamp, and signature in the request headers

The `ripio_api_utils.py` file provides utility functions to handle this authentication process.

## Examples

### Utility Module

- **ripio_api_utils.py**: Contains utility functions for API authentication, making requests, and handling responses.

### REST API Examples

1. **example_auth.py**: Demonstrates authentication and retrieves account balances.

2. **example_balances.py**: Retrieves and displays account balances for all currencies.

3. **example_order_book_level2.py**: Retrieves and displays the order book (level 2) for a specific trading pair.

4. **example_create_cancel_order.py**: Creates a limit order and then cancels it, demonstrating the order lifecycle.

5. **example_user_orders.py**: Retrieves user orders with various filters (status, pair, side, etc.).

### WebSocket Example

- **example_websocket.py**: Demonstrates how to connect to the WebSocket API, authenticate, and subscribe to real-time balance updates.

## Usage

Each example can be run as a standalone Python script:

```bash
python example_auth.py
python example_balances.py
python example_order_book_level2.py
python example_create_cancel_order.py
python example_user_orders.py
python example_websocket.py
```

Make sure to set your API credentials as environment variables before running the examples.

## API Endpoints

The examples in this repository use the following API endpoints:

- `/user/balances/`: Get account balances
- `/book/orders/level-2`: Get order book data
- `/orders`: Create, cancel, and retrieve orders
- `/ticket`: Get WebSocket authentication ticket

## WebSocket API

The WebSocket API allows you to receive real-time updates for:

- Balance changes
- Order updates
- Market data

The WebSocket connection requires authentication using a ticket obtained from the REST API.

## Error Handling

The examples include basic error handling for API requests. Common errors include:

- Authentication failures
- Invalid parameters
- Rate limiting
- Server errors

Check the API response for error details if a request fails.

## Additional Resources

- [Ripio Trade API Documentation](https://apidocs.ripiotrade.co/)
- [Ripio Trade Website](https://www.ripiotrade.co/)

## Disclaimer

These examples are provided for educational purposes only. Use them at your own risk when trading with real funds.

## License

This repository is available for public use. Please refer to Ripio Trade's terms of service for API usage limitations.
