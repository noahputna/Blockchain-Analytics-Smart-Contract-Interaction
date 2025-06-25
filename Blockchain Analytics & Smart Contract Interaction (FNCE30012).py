# Import Libraries.
# Note: Some of these Libraries will NOT load given they are University of Melbourne provided.
# Designed to simulate a real-world Blockchain interface.
from bmmnet import *
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import time

# Connect to network and store credentials.
# Connect to the simulated Ethereum network provided by The University of Melbourne.
node_connection = connect()
address = "0x251c32506Aa9Af8AA06E462464296cFEa5BcB25B"
private_key = "5b5568a222de364c796cb26c7308eefca5da48ac4caca74164eabdbcafac9aca"

# Contract addresses.
# Retrieve deployed smart contract addresses for BMMCoin and BMM Market
bmmcoin_address = get_bmmcoin_address()
bmm_market_address = get_market_address()

print(f"BMM Coin Contract: {bmmcoin_address}")
print(f"BMM Market Contract: {bmm_market_address}")

# Establish connection and gather smart contract information.
market_contract = get_market_contract(node_connection)

# Get list of available products from the market smart contract.
products = market_contract.functions.getProducts().call()

# Get fee required to purchase each product.
fees = {product: market_contract.functions.getFee(product).call() for product in products}

# Request BMM tokens from the token contract.
requested_amount = fees.get('C')

# Get the number of transactions sent from this address (used as a nonce).
nonce_request = node_connection.eth.get_transaction_count(address)
coin_contract = get_bmm_contract(node_connection)

# Request Ether from the wallet if the balance is too low (testnet only).
if node_connection.eth.get_balance(address) <= 1000000:
    request_ether(address, 10000000)

# Set the initial and maximum gas price for the transaction.
gas_price = 1
max_gas_price = 10

# Attempt to send the transaction with increasing gas prices until it succeeds or max is reached.
for price in range(max_gas_price):
    try:

        # Build the transaction parameters.
        tx_data = {
            "from": address,                # Sender address.
            "nonce": nonce_request,         # Unique idenetifier for transaction order.
            "gas":100000,                   # Maximum gas allowed for execution.
            "gasPrice": gas_price           # Current gas price to offer (in Wei).
        }
        
        # Construct the token request transaction from the smart contract.
        txn = coin_contract.functions.request(requested_amount).build_transaction(tx_data)

        # Sign the transaction using the private key of the sender.
        signed_tx = node_connection.eth.account.sign_transaction(txn, private_key=private_key)

        # Broadcast the signed transaction to the Ethereum network.
        tx_hash = node_connection.eth.send_raw_transaction(signed_tx.rawTransaction)

        # Store the resulting transaction hash in hexidecimal format.
        bmm_request_hash = to_hex(tx_hash)

        # Exit loop once transaction is succesfully sent.
        break

    except ValueError as e:

        # Handle case where transaction nonce is outdated (another tx likely mined already).
        # Increment nonce and try again.
        if 'OldNonce' in str(e):
            nonce_request += 1
        
        # Handle case whhere gas price is too low and rejected by the network.
        # Increase gas price and delay transaction resend.
        elif 'FeeTooLowToCompete' in str(e):
            gas_price += 1
            time.sleep(10)
        
        # Handle any other unexpected error and exit loop.
        else:
            print("Error:", e)
            break

# --- Step 1: Approve BMM spend --- 

# Get the current nonce (transaction count) for the wallet to ensure tx uniqueness.
nonce_approve = node_connection.eth.get_transaction_count(address)

# Get the fee required for purchasing product 'C'.
fee = fees['C']

# Get the m arket contract address that will be approved to spend tokens.
market_address = get_market_address()

# Attempt to send the approval transaction with retries at increasing gas prices.
for price in range(max_gas_price):
    try:

        tx_data = {
            "from": address,                # Sender address.
            "nonce": nonce_request,         # Unique idenetifier for transaction order.
            "gas":100000,                   # Maximum gas allowed for execution.
            "gasPrice": gas_price           # Current gas price to offer (in Wei).
        }

        # Construct the token request transaction from the smart contract.
        txn = coin_contract.functions.approve(market_address, fee).build_transaction(tx_data)

        # Sign the transaction using the private key of the sender.
        signed_tx = node_connection.eth.account.sign_transaction(txn, private_key=private_key)

        # Broadcast the signed transaction to the Ethereum network.
        tx_hash = node_connection.eth.send_raw_transaction(signed_tx.rawTransaction)

        # Exit loop once transaction is succesfully sent.
        break

    except ValueError as e:

        # Handle case where transaction nonce is outdated (another tx likely mined already).
        # Increment nonce and try again.
        if 'OldNonce' in str(e):
            nonce_approve += 1

        # Handle case whhere gas price is too low and rejected by the network.
        # Increase gas price and delay transaction resend.
        elif 'FeeTooLowToCompete' in str(e):
            gas_price += 1
            time.sleep(10)

        # Handle any other unexpected error and exit loop.
        else:
            print("Error:", e)
            break

# --- Step 2: Buy Product --- 

# Access a new nonce for the new transaction (purchase the product).
nonce_buy = node_connection.eth.get_transaction_count(address)

# Define the product we want to purchase.
product = "C"

# Attempt to send the purchase transaction with increasing gas prices if needed.
for price in range(max_gas_price):
    try:

        # Build the transaction parameters.
        tx_data = {
            "from": address, 
            "nonce": nonce_buy, 
            "gas":150000, 
            "gasPrice": gas_price
        }

        # Build the transaction to invoke the 'buyProduct' function on the market contract.
        txn = market_contract.functions.buyProduct(product).build_transaction(tx_data)

        # Sign the transaction using the seneder's private key.
        signed_tx = node_connection.eth.account.sign_transaction(txn, private_key=private_key)

        # Submit the signed transaction to the network.
        tx_hash = node_connection.eth.send_raw_transaction(signed_tx.rawTransaction)

        # Convert the transaction has to hex and store it.
        buy_product_hash = to_hex(tx_hash)

        # Exit loop once transaction is succesfully sent.
        break
    
    except ValueError as e:
        if 'OldNonce' in str(e):
            nonce_buy += 1
        elif 'FeeTooLowToCompete' in str(e):
            gas_price += 1
            time.sleep(10)
        else:
            print("Error:", e)
            break

# Extract purchase information from a blockchain transaction hash.
def get_purchase_details(tx_hash):
    try:

        # Retrieve the full transaction details from the Ethereum network using its hash.
        transaction_information = node_connection.eth.get_transaction(tx_hash)

        # Decode the transaction input data to identify which contract function was called.
        function_name, function_inputs = market_contract.decode_function_input(
            transaction_information["input"]
        )
    
    # If the transaction can't be decoded (e.g., invalid hash or non contract call)
    except ValueError:
        return None

    # Check if the function that was called is 'buyProduct'
    if function_name.fn_name == "buyProduct":

        # Extract and return the sender address and the product name from the transaction.
        return {
            'from': transaction_information['from'], 
            'product': function_inputs.get('product')
        }
    
    return None

# Define the range of Ethereum block numbers to analyse.
start_block = 184
end_block = 190

# Define the products available in the market.
products = ['A', 'B', 'C']

# To store purchase and fee data for each block.
data = {}

# Look over each block in the specified range.
for i in range(start_block, end_block + 1):

    # Retrieve the fill block data from the Ethereum network.
    block = node_connection.eth.get_block(i)

    # Initialise structure for storing buys and fees per product for the current block.
    data[i] = {
        'buys': {p: 0 for p in products}, 
        'fee': {p: 0 for p in products}
    }

    # For each product, retrieve the historical fee set at this specific block.
    for product in products:
        data[i]['fee'][product] = market_contract.functions.getFee(product).call(block_identifier=i)
    
    # Iterate through all transaction included in this block.
    for tx in block.transactions:

        # Convert the transaction hash from bytes to hex format.
        tx_hash = to_hex(tx)

        # Extract product details from the transaction
        details = get_purchase_details(tx_hash)

        # If this was a buyProduct transaction, increment the corresponding count.
        if details:
            data[i]['buys'][details['product']] += 1

# Calculate the total demand (total BMM tokens spent) per product in each block.
demand = {
    block: {
        p: data[block]['fee'][p] * data[block]['buys'][p]
        for p in products
    } 
    for block in data
}

# Store fee history per product.
product_fees = {
    p: [] for p in products
}

# Populate fee history from each block.
for block in data:
    for product in products:
        product_fees[product].append(data[block]['fee'][product])

# Plot fee time series for each product.
for product, series in product_fees.items():
    plt.plot(series, label=product)

plt.xlabel("Block")
plt.ylabel("Fee")
plt.title("Product Fees Over Time")
plt.legend()
plt.show()

# Store purchase count per product.
product_buys = {
    p: [] for p in products
}

# Populate purchase counts from each block
for block in data:
    for product in products:
        product_buys[product].append(data[block]['buys'][product])

# Plot purchase volume over time.
for product, series in product_buys.items():
    plt.plot(series, label=product)

plt.xlabel("Block")
plt.ylabel("Units Purchased")
plt.title("Product Purchases Over Time")
plt.legend()
plt.show()

# Store total currency spent per product.
product_spent = {
    p: [] for p in products
}

# Populate spending data from the 'demand' structure.
for block in data:
    for product in products:
        product_spent[product].append(demand[block][product])

# Plot BMM coin spending per product over time.
for product, series in product_spent.items():
    plt.plot(series, label=product)

plt.xlabel("Block")
plt.ylabel("Currency Spent")
plt.title("Total BMM Coin Spent per Product")
plt.legend()
plt.show()

# Convert BMM Coin to AUD using product price ratios
def bmm_aud(a_bmm, a_aud, b_bmm, b_aud, c_bmm, c_aud):
    
    # Calculate exchange rate implied by Product 'A', 'B' & 'C'.
    exchange_rate_product_a = 1 / (a_bmm / a_aud)
    exchange_rate_product_b = 1 / (b_bmm / b_aud)
    exchange_rate_product_c = 1 / (c_bmm / c_aud)

    # Average of the three implied exchange rates.
    bmm_to_aud_exchange_rate = round(
        (exchange_rate_product_a + exchange_rate_product_b + exchange_rate_product_c) / 3,
          3
    )

    return bmm_to_aud_exchange_rate