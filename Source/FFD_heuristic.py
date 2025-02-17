import math
import time

# # Stock and order information (provided)
# stocks = {
#     "Type 1": {"length": 80, "cost": 90},
#     "Type 2": {"length": 100, "cost": 110},
#     "Type 3": {"length": 120, "cost": 130},
# }

# order = {
#     "S": {"length": 15, "demand": 20},
#     "M": {"length": 30, "demand": 10},
#     "L": {"length": 34, "demand": 15},
#     "XL": {"length": 47, "demand": 5},
# }
 # Define stock information with their lengths and costs
# stocks = {
#     "Type 1": {"length": 80, "cost": 90},
#     "Type 2": {"length": 100, "cost": 110},
# }

# # Define the order requirements with their lengths and demands
# order = {
#     "A": {"length": 20, "demand": 5},
#     "B": {"length": 30, "demand": 3},
# }

# Steel stock data with more types
# stocks = {
#     "Type 1": {"length": 80, "cost": 90},
#     "Type 2": {"length": 100, "cost": 110},
#     "Type 3": {"length": 120, "cost": 130},
# }

# # Detailed order requirements
# order = {
#     "A": {"length": 20, "demand": 10},
#     "B": {"length": 30, "demand": 8},
#     "C": {"length": 40, "demand": 6},
#     "D": {"length": 50, "demand": 4},
# }

 # Define stock information with their lengths and costs
stocks = {
    "Type 1": {"length": 80, "cost": 100},
    "Type 2": {"length": 100, "cost": 150},
    "Type 3": {"length": 120, "cost": 200},
}
# Define steel stock data with various types
order = {
    "S": {"length": 10, "demand": 50},
    "M": {"length": 20, "demand": 30},
    "L": {"length": 30, "demand": 20},
    "XL": {"length": 40, "demand": 10},
}
def ffd_heuristic(stocks, order):
    """
    Applies the First-Fit Decreasing heuristic to the cutting stock problem.

    Args:
        stocks: A dictionary containing stock types, their lengths, and costs.
        order: A dictionary containing order types, their lengths, and demands.

    Returns:
        A list of cutting patterns, where each pattern is a dictionary
        indicating how many of each order type are cut from a stock type.
    """

    # Sort order items by decreasing length
    order_items = sorted(order.items(), key=lambda x: x[1]["length"], reverse=True)

    # Initialize residual demands
    residual_demands = {item: details["demand"] for item, details in order.items()}

    # Initialize patterns list
    patterns = []

    while any(residual_demands.values()):  # Continue until all demands are met
        for stock_type, stock_details in stocks.items():
            stock_length = stock_details["length"]
            remaining_length = stock_length
            pattern = {item: 0 for item in order}  # Initialize an empty pattern

            for item, _ in order_items:
                item_length = order[item]["length"]
                while remaining_length >= item_length and residual_demands[item] > 0:
                    pattern[item] += 1
                    remaining_length -= item_length
                    residual_demands[item] -= 1

            if any(pattern.values()):  # Add pattern only if it's not empty
                patterns.append({"stock_type": stock_type, "cuts": pattern})

    return patterns
# Start timer
start_time = time.time()

# Get the cutting patterns using FFD heuristic
patterns = ffd_heuristic(stocks, order)

# End timer
end_time = time.time()
execution_time = end_time - start_time

# Prepare the summary output
print("Summary of Steel Bars Usage and Demand Fulfillment:\n")

total_cost = 0
for stock_type, stock_details in stocks.items():
    stock_length = stock_details["length"]
    stock_cost = stock_details["cost"]
    stock_total_cost = 0

    print(f"Stock {stock_type} (Length: {stock_length}):")

    # Filter patterns for this stock type
    stock_patterns = [p for p in patterns if p["stock_type"] == stock_type]

    for i, pattern in enumerate(stock_patterns):
        pattern_cost = stock_cost
        stock_total_cost += pattern_cost

        # Format cuts into a list for easier printing
        cuts_list = [pattern["cuts"][item] for item in order]

        print(f"  Pattern {i+1}: {cuts_list} x1 (Cost: ${pattern_cost} each)")

    total_cost += stock_total_cost
    print(f"  Total Cost for {stock_type}: ${stock_total_cost}\n")

# Calculate demand fulfillment
demand_fulfillment = {
    item: sum(p["cuts"][item] for p in patterns) for item in order
}

print("Demand Fulfillment:")
for item, fulfilled in demand_fulfillment.items():
    print(f"  {item}: {fulfilled}/{order[item]['demand']} pieces cut")
print("\n")

print("Total Cost by Stock Type:")
for stock_type, stock_details in stocks.items():
    stock_cost = stock_details["cost"]
    # Count how many times this stock type is used in patterns
    stock_count = len([p for p in patterns if p["stock_type"] == stock_type])
    stock_total_cost = stock_cost * stock_count
    print(f"  {stock_type}: ${stock_total_cost}")

print(f"\nTotal Cost: ${total_cost}")
print(f"Execution Time: {execution_time:.4f} seconds")
