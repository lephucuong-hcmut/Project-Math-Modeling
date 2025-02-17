from itertools import product
import time
# Define stock information with their lengths and costs
stocks = {
    "Type 1": {"length": 80, "cost": 90},
    "Type 2": {"length": 100, "cost": 110},
    "Type 3": {"length": 120, "cost": 130},
}

# Define order requirements with their lengths and demands
order = {
    "S": {"length": 15, "demand": 20},
    "M": {"length": 30, "demand": 10},
    "L": {"length": 34, "demand": 15},
    "XL": {"length": 47, "demand": 5},
}

def is_valid_pattern(pattern, order, stock_length):
    """Check if the pattern is valid based on the stock length and order constraints."""
    total_length = sum(order[f]["length"] * count for f, count in pattern.items())
    remaining_length = stock_length - total_length
    
    if remaining_length > 0 and remaining_length >= min(order[f]["length"] for f in order):
        return False

    return total_length <= stock_length

def generate_patterns(stock_length, order):
    """Generate all feasible patterns for a given stock length."""
    max_cuts = [stock_length // order[f]["length"] for f in order]
    feasible_patterns = []
    
    for pattern in product(*(range(m + 1) for m in max_cuts)):
        pattern_dict = dict(zip(order.keys(), pattern))
        if is_valid_pattern(pattern_dict, order, stock_length):
            feasible_patterns.append(pattern_dict)
    
    return feasible_patterns

def greedy_cutting(order, stocks):
    """Perform the greedy cutting based on cost minimization and print the summary."""
    sorted_stocks = sorted(stocks.items(), key=lambda x: x[1]['cost'] / x[1]['length'])
    
    remaining_demand = {k: v['demand'] for k, v in order.items()}
    stock_usage = {stock_id: {} for stock_id in stocks}
    cut_counts = {demand: 0 for demand in order}  # Track cut counts for each demand
    total_cost = 0

    while any(remaining_demand[f] > 0 for f in remaining_demand):
        for stock_id, stock_info in sorted_stocks:
            stock_length = stock_info["length"]
            cost = stock_info["cost"]
            patterns = generate_patterns(stock_length, order)
            
            patterns = sorted(patterns, key=lambda p: sum(p.values()), reverse=True)
            
            best_pattern = None
            best_pattern_cost = float('inf')
            
            for pattern in patterns:
                if all(remaining_demand[f] >= pattern[f] for f in pattern):
                    if cost < best_pattern_cost:
                        best_pattern = pattern
                        best_pattern_cost = cost
            
            if not best_pattern:
                continue
            
            pattern_tuple = tuple(sorted(best_pattern.items()))
            if pattern_tuple in stock_usage[stock_id]:
                stock_usage[stock_id][pattern_tuple] += 1
            else:
                stock_usage[stock_id][pattern_tuple] = 1

            for item in best_pattern:
                cut_counts[item] += best_pattern[item]  # Update cut counts
                remaining_demand[item] -= best_pattern[item]
            total_cost += best_pattern_cost

            if all(remaining_demand[f] <= 0 for f in remaining_demand):
                break
    
    return stock_usage, total_cost, cut_counts

# Perform greedy cutting
# Start timing
start_time = time.time()
stock_usage, total_cost, cut_counts = greedy_cutting(order, stocks)
# End timing
end_time = time.time()
# Calculate execution time
execution_time = end_time - start_time
# Print the summary with patterns as vectors and costs
print("Summary of Steel Bars Usage and Demand Fulfillment:\n")

total_cost_by_stock = {stock_id: 0 for stock_id in stocks}  # Initialize costs for each stock type

for stock_id, patterns in stock_usage.items():
    print(f"Stock {stock_id} (Length: {stocks[stock_id]['length']}):")
    pattern_index = 1
    for pattern_tuple, count in patterns.items():
        pattern_dict = dict(pattern_tuple)
        vector = [pattern_dict.get(demand, 0) for demand in order.keys()]
        pattern_cost = stocks[stock_id]['cost']
        total_cost_by_stock[stock_id] += pattern_cost * count  # Accumulate cost for the current pattern
        print(f"  Pattern {pattern_index}: {vector} x{count} (Cost: ${pattern_cost} each)")
        pattern_index += 1
print("\nDemand Fulfillment:")
for demand in order:
    print(f"  {demand}: {cut_counts[demand]}/{order[demand]['demand']} pieces cut")

print("\nTotal Cost by Stock Type:")
for stock_id, cost in total_cost_by_stock.items():
    print(f"  {stock_id}: ${cost}")

print(f"\nTotal Cost: ${total_cost}\n")
print(f"Execution Time: {execution_time:.4f} seconds")