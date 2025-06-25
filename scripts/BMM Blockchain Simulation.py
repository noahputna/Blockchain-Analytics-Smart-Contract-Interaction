# Import Libraries.
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load JSON data from mock file (mock data).
json_path = "data/mock_block_data.json"

# If the file isn't found in the first path, try a fallback.
if not os.path.exists(json_path):
    json_path = "../data/mock_block_data.json"

# Load the JSON file which contains mock blockchain data.
with open(json_path) as f:
    file_data = json.load(f)

# Define available products.
products = ['A', 'B', 'C']

# Calculate demand per product per block by multiplying fee by quantity purchased.
demand = {
    block: {
        p: file_data[block]['fee'][p] * file_data[block]['buys'][p] 
        for p in products
    } 
    for block in file_data
}

# Plot Product Fees overtime.
# Store product fee data over blocks.
product_fees = {
    p: [] for p in products
}

# Loop through blocks and collect fee values for each product.
for block, data in file_data.items():
    for product in products:
        product_fees[product].append(data['fee'][product])

# Plot fee evolution per product over blocks.
for product, series in product_fees.items():
    plt.plot(series, label=product)

plt.xlabel("Block")
plt.ylabel("Fee")
plt.title("Product Fees Over Time")
plt.legend()
plt.show()

# Plot product purchased over time.
# Store product purchase volume over blocks.
product_buys = {
    p: [] for p in products
}

# Loop through blocks and collect buy counts per product.
for block, data in file_data.items():
    for product in products:
        product_buys[product].append(data['buys'][product])

# Plot number of units bough per product over blocks.
for product, series in product_buys.items():
    plt.plot(series, label=product)

plt.xlabel("Block")
plt.ylabel("Units Purchased")
plt.title("Product Purchases Over Time")
plt.legend()
plt.show()

# Plot BMM Coin Spent (Demand) Over Time
# Store BMM spent per product over blocks.
product_spent = {
    p: [] for p in products
}

# Loop through blocks and collect total spend (fee x quantity)
for block in file_data:
    for product in products:
        product_spent[product].append(demand[block][product])

# Plot total BMM coin spent on each product over time.
for product, series in product_spent.items():
    plt.plot(series, label=product)

plt.xlabel("Block")
plt.ylabel("BMM Coins Spent")
plt.title("Total BMM Coin Spent per Product")
plt.legend()
plt.show()