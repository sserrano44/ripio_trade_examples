#!/usr/bin/env python3
import json
import time
from datetime import datetime, timedelta
from ripio_api_utils import make_request, get_api_credentials

def get_withdrawal_fees(api_key, api_secret, currency_code):
    """Get withdrawal fees for a specific cryptocurrency.
    
    Args:
        api_key: API key
        api_secret: API secret
        currency_code: Currency code (e.g., 'BTC', 'ETH', 'USDC')
        
    Returns:
        dict: API response with fee information
    """
    endpoint = f"/withdrawals/estimate-fee/{currency_code}"
    
    print(f"\nFetching withdrawal fees for {currency_code}...")
    
    # Make the request using the utility function
    response = make_request(api_key, api_secret, "GET", endpoint)
    
    if response and 'data' in response:
        fee_data = response['data']
        print(f"\n----- {currency_code} Withdrawal Fees -----")
        
        # The API returns fee data with 'amount' and 'network' fields
        if isinstance(fee_data, dict):
            print(f"Currency: {currency_code}")
            
            # Get fee amount and network
            fee_amount = fee_data.get('amount')
            network = fee_data.get('network')
            
            if fee_amount is not None:
                print(f"Estimated Fee: {fee_amount} {currency_code}")
            
            if network:
                print(f"Network: {network}")
            
            # Check for any additional fields that might be present
            for key, value in fee_data.items():
                if key not in ['amount', 'network'] and value is not None:
                    print(f"{key.replace('_', ' ').title()}: {value}")
        else:
            print(f"Unexpected fee data format: {type(fee_data)}")
            print(f"Raw response: {fee_data}")
        
        print("--------------------------------")
    
    return response

def create_withdrawal(api_key, api_secret, currency_code, amount, destination_address, 
                     tag=None, network=None, memo=None, external_id=None):
    """Create a new cryptocurrency withdrawal.
    
    Args:
        api_key: API key
        api_secret: API secret
        currency_code: Currency code (e.g., 'BTC', 'ETH', 'USDC')
        amount: Amount to withdraw
        destination_address: Blockchain address to send funds to
        tag: Optional tag for currencies that require it (e.g., XRP)
        network: Optional network specification if multiple are supported
        memo: Optional memo field
        external_id: Optional external ID for tracking
        
    Returns:
        dict: API response with withdrawal details
    """
    endpoint = "/withdrawals"
    
    # Prepare withdrawal data according to API documentation
    withdrawal_data = {
        "currency_code": currency_code,
        "amount": str(amount),  # Convert to string like other endpoints
        "destination": destination_address  # API expects 'destination'
    }
    
    # Only add optional parameters if they have values (not None)
    if network:
        withdrawal_data["network"] = network
        
    if tag:
        withdrawal_data["tag"] = tag
        
    if memo:
        withdrawal_data["memo"] = memo
        
    if external_id:
        withdrawal_data["external_id"] = external_id
    
    print(f"\nCreating withdrawal for {amount} {currency_code}...")
    print(f"Destination: {destination_address}")
    if network:
        print(f"Network: {network}")
    
    # Make the request using the utility function
    response = make_request(api_key, api_secret, "POST", endpoint, data=withdrawal_data)
    
    if response:
        print("Withdrawal request created successfully!")
    else:
        print("Failed to create withdrawal request!")
        
    return response

def get_withdrawal_status(api_key, api_secret, withdrawal_id):
    """Get the status of a specific withdrawal.
    
    Args:
        api_key: API key
        api_secret: API secret
        withdrawal_id: ID of the withdrawal to check
        
    Returns:
        dict: API response with withdrawal status
    """
    endpoint = f"/withdrawals/{withdrawal_id}"
    
    print(f"\nChecking status for withdrawal ID: {withdrawal_id}...")
    
    # Make the request using the utility function
    response = make_request(api_key, api_secret, "GET", endpoint)
    
    if response and 'data' in response:
        withdrawal = response['data']
        print(f"\n----- Withdrawal Status -----")
        print(f"ID: {withdrawal.get('id')}")
        print(f"Status: {withdrawal.get('status')}")
        print(f"Amount: {withdrawal.get('amount')} {withdrawal.get('currency_code')}")
        print(f"Transaction Hash: {withdrawal.get('transaction_hash', 'Pending')}")
        print(f"Created: {withdrawal.get('created_at')}")
        print("-----------------------------")
    
    return response

def list_withdrawals(api_key, api_secret, currency_code=None, status=None, 
                    from_date=None, to_date=None, limit=10, offset=0):
    """List withdrawals with optional filters.
    
    Args:
        api_key: API key
        api_secret: API secret
        currency_code: Optional filter by currency
        status: Optional filter by status ('pending', 'processing', 'completed', 'failed')
        from_date: Optional start date filter (ISO format)
        to_date: Optional end date filter (ISO format)
        limit: Number of results to return (default: 10)
        offset: Pagination offset (default: 0)
        
    Returns:
        dict: API response with list of withdrawals
    """
    endpoint = "/withdrawals"
    
    # Build query parameters
    params = {
        "limit": limit,
        "offset": offset
    }
    
    if currency_code:
        params["currency_code"] = currency_code
    if status:
        params["status"] = status
    if from_date:
        params["from_date"] = from_date
    if to_date:
        params["to_date"] = to_date
    
    print("\nFetching withdrawals...")
    
    # Make the request using the utility function
    response = make_request(api_key, api_secret, "GET", endpoint, params=params)
    
    return response

def display_withdrawals_table(withdrawals):
    """Display withdrawals in a formatted table.
    
    Args:
        withdrawals: List of withdrawal objects
    """
    if not withdrawals:
        print("No withdrawals found.")
        return
    
    # Check if withdrawals is a list of dictionaries or something else
    if isinstance(withdrawals, list) and len(withdrawals) > 0:
        # If the first item is a string, the API might be returning a different format
        if isinstance(withdrawals[0], str):
            print("Unexpected withdrawal format - received strings instead of objects")
            for item in withdrawals[:5]:  # Show first 5 items
                print(f"  - {item}")
            return
    
    # Print table header
    print(f"\n{'ID':<12} {'Currency':<8} {'Amount':<15} {'Status':<12} {'Address':<30} {'Created':<20}")
    print("-" * 105)
    
    # Print each withdrawal
    for withdrawal in withdrawals:
        if isinstance(withdrawal, dict):
            withdrawal_id = str(withdrawal.get('id', 'N/A'))[:12]
            currency = withdrawal.get('currency_code', 'N/A')
            amount = float(withdrawal.get('amount', 0))
            status = withdrawal.get('status', 'N/A')
            address = str(withdrawal.get('destination_address', 'N/A'))[:30]
            created = str(withdrawal.get('created_at', 'N/A'))[:20]
            
            print(f"{withdrawal_id:<12} {currency:<8} {amount:<15.8f} {status:<12} {address:<30} {created:<20}")
        else:
            print(f"Unexpected withdrawal format: {type(withdrawal)}")

def demo_withdrawal_workflow():
    """Demonstrate the withdrawal workflow with safety checks."""
    # Get API credentials from environment variables
    api_key, api_secret = get_api_credentials()
    
    if not api_key or not api_secret:
        return
    
    print("===== RIPIO TRADE WITHDRAWAL EXAMPLE =====")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("==========================================")
    
    print("\n⚠️  WARNING: This example uses TEST addresses.")
    print("⚠️  Never send real funds to these addresses!")
    print("⚠️  Always verify addresses before making real withdrawals!")
    
    # Step 1: Try to get withdrawal fees (may not be available for all currencies)
    currency = "USDC"
    print("\nNote: Withdrawal fees endpoint may not be available for all currencies.")
    fees_response = get_withdrawal_fees(api_key, api_secret, currency)
    
    if not fees_response:
        # Try with a different currency
        print("\nTrying with BTC instead...")
        currency = "BTC"
        fees_response = get_withdrawal_fees(api_key, api_secret, currency)
    
    # Step 2: Create a test withdrawal (with dummy address)
    # WARNING: This is a TEST address - DO NOT use in production!
    test_address = "0x0000000000000000000000000000000000000000"  # Ethereum null address
    test_amount = 10.0
    
    print(f"\n⚠️  DEMO: Creating TEST withdrawal of {test_amount} {currency}")
    print(f"⚠️  To address: {test_address}")
    print("⚠️  This is for demonstration only!")
    
    # Uncomment the following lines to actually create a withdrawal
    # BE VERY CAREFUL - only use with test addresses!
    """
    create_response = create_withdrawal(
        api_key,
        api_secret,
        currency,
        test_amount,
        test_address,
        network="ethereum" if currency == "USDC" else "bitcoin"  # Specify appropriate network
    )
    
    if create_response and 'data' in create_response:
        withdrawal_id = create_response['data'].get('id')
        
        # Step 3: Check withdrawal status
        if withdrawal_id:
            print("\nWaiting 2 seconds before checking status...")
            time.sleep(2)
            get_withdrawal_status(api_key, api_secret, withdrawal_id)
    """
    
    # Step 4: List recent withdrawals
    print("\n\n===== RECENT WITHDRAWALS =====")
    
    # Get withdrawals from the last 30 days
    to_date = datetime.now()
    from_date = to_date - timedelta(days=30)
    
    list_response = list_withdrawals(
        api_key,
        api_secret,
        from_date=from_date.isoformat(),
        to_date=to_date.isoformat(),
        limit=20
    )
    
    if list_response and 'data' in list_response:
        response_data = list_response['data']
        
        # Check if response has pagination structure
        if isinstance(response_data, dict) and 'withdrawals' in response_data:
            withdrawals = response_data['withdrawals']
            pagination = response_data.get('pagination', {})
            
            # Display pagination info if available
            if pagination:
                print(f"\nPage {pagination.get('current_page', 1)} of {pagination.get('total_pages', 1)}")
                print(f"Total withdrawals: {pagination.get('registers_count', 0)}")
        else:
            # Fallback to direct list format
            withdrawals = response_data if isinstance(response_data, list) else []
        
        # Display the withdrawals table
        display_withdrawals_table(withdrawals)
        
        # Only show summary if we have actual withdrawal objects
        if isinstance(withdrawals, list) and withdrawals and isinstance(withdrawals[0], dict):
            print(f"\nTotal withdrawals shown: {len(withdrawals)}")
            
            # Group by status
            status_counts = {}
            for w in withdrawals:
                if isinstance(w, dict):
                    status = w.get('status', 'unknown')
                    status_counts[status] = status_counts.get(status, 0) + 1
            
            if status_counts:
                print("\nWithdrawals by status:")
                for status, count in status_counts.items():
                    print(f"  {status}: {count}")
    
    print("\n==========================================")

def create_real_withdrawal_with_confirmation():
    """Create a real withdrawal with user confirmation.
    
    This function includes safety checks and requires explicit user confirmation.
    """
    # Get API credentials from environment variables
    api_key, api_secret = get_api_credentials()
    
    if not api_key or not api_secret:
        return
    
    print("===== CREATE REAL WITHDRAWAL =====")
    print("⚠️  WARNING: This will create a REAL withdrawal!")
    print("⚠️  Funds will be sent to the specified address!")
    print("==================================\n")
    
    # Get withdrawal parameters from user
    currency = input("Enter currency code (e.g., BTC, ETH, USDC): ").upper()
    
    # Get fees first
    fees_response = get_withdrawal_fees(api_key, api_secret, currency)
    
    if not fees_response:
        print("Failed to get withdrawal fees. Aborting.")
        return
    
    amount = float(input("\nEnter amount to withdraw: "))
    address = input("Enter destination address: ")
    
    # Optional parameters
    network = input("Enter network (press Enter to skip): ") or None
    tag = input("Enter tag if required (e.g., for XRP) (press Enter to skip): ") or None
    memo = input("Enter memo if required (press Enter to skip): ") or None
    
    # Display summary and confirm
    print("\n===== WITHDRAWAL SUMMARY =====")
    print(f"Currency: {currency}")
    print(f"Amount: {amount}")
    print(f"Destination: {address}")
    if network:
        print(f"Network: {network}")
    if tag:
        print(f"Tag: {tag}")
    if memo:
        print(f"Memo: {memo}")
    print("==============================")
    
    confirmation = input("\n⚠️  Are you SURE you want to proceed? Type 'YES' to confirm: ")
    
    if confirmation != "YES":
        print("Withdrawal cancelled.")
        return
    
    # Create the withdrawal
    response = create_withdrawal(
        api_key,
        api_secret,
        currency,
        amount,
        address,
        tag=tag,
        network=network,
        memo=memo
    )
    
    if response and 'data' in response:
        withdrawal = response['data']
        print("\n✅ Withdrawal created successfully!")
        print(f"Withdrawal ID: {withdrawal.get('id')}")
        print(f"Status: {withdrawal.get('status')}")
        print("\nPlease check your email for confirmation if required.")
    else:
        print("\n❌ Failed to create withdrawal.")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--real":
        # Run the real withdrawal function with confirmations
        create_real_withdrawal_with_confirmation()
    else:
        # Run the demo workflow
        demo_withdrawal_workflow()
        print("\nTo create a real withdrawal, run: python example_withdrawals.py --real")
