from itertools import product
import numpy as np
import random
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
    """
    Check if the pattern is valid, i.e., total length of the cuts does not exceed the stock length,
    and the remaining length does not exceed any of the required sizes.
    """
    total_length = sum(order[f]["length"] * count for f, count in pattern.items())
    remaining_length = stock_length - total_length
    
    # Check if remaining length is not larger than any required size
    if remaining_length > 0 and remaining_length >= min(order[f]["length"] for f in order):
        return False

    return total_length <= stock_length

def generate_patterns(stock_length, order):
    """
    Generate all feasible patterns for a given stock length.
    """
    max_cuts = [stock_length // order[f]["length"] for f in order]
    feasible_patterns = []
    
    # Generate all possible combinations of cut counts
    for pattern in product(*(range(m + 1) for m in max_cuts)):
        pattern_dict = dict(zip(order.keys(), pattern))
        if is_valid_pattern(pattern_dict, order, stock_length):
            feasible_patterns.append(pattern_dict)
    
    return feasible_patterns

# Generate patterns for each stock
all_patterns = {}
for stock_id, stock_info in stocks.items():
    stock_length = stock_info["length"]
    patterns = generate_patterns(stock_length, order)
    all_patterns[stock_id] = patterns


def cost_of_pattern(pattern, stock_cost):
    """Calculate the cost of using a specific pattern."""
    return stock_cost

def evaluate_solution(solution, stocks, order):
    """Calculate the total cost of a given solution and check if it meets the demand."""
    total_cost = 0
    total_cut = {demand: 0 for demand in order}
    
    for stock_id, patterns in solution.items():
        stock_cost = stocks[stock_id]['cost']
        total_cost += stock_cost * sum(patterns.values())
        for pattern_tuple, count in patterns.items():
            pattern_dict = dict(pattern_tuple)
            for item, qty in pattern_dict.items():
                total_cut[item] += qty * count
    
    # Check if total cuts meet or exceed the demand
    demand_met = all(total_cut[d] >= order[d]['demand'] for d in order)
    return total_cost, demand_met

def create_initial_solution(stocks, order):
    """Create an initial random solution."""
    solution = {stock_id: {} for stock_id in stocks}
    remaining_demand = {k: v['demand'] for k, v in order.items()}
    
    while any(remaining_demand[f] > 0 for f in remaining_demand):
        stock_id = random.choice(list(stocks.keys()))
        stock_length = stocks[stock_id]["length"]
        patterns = generate_patterns(stock_length, order)
        if patterns:
            pattern = random.choice(patterns)
            pattern_tuple = tuple(sorted(pattern.items()))
            if pattern_tuple not in solution[stock_id]:
                solution[stock_id][pattern_tuple] = 0
            solution[stock_id][pattern_tuple] += 1
            for item in pattern:
                remaining_demand[item] -= pattern[item]
    
    return solution

def simulated_annealing(order, stocks, initial_temperature=1000, cooling_rate=0.995, max_iterations=500):
    """Perform Simulated Annealing to find the optimal cutting solution."""
    current_solution = create_initial_solution(stocks, order)
    current_cost, current_demand_met = evaluate_solution(current_solution, stocks, order)
    
    best_solution = current_solution
    best_cost = current_cost
    best_demand_met = current_demand_met
    
    temperature = initial_temperature
    
    for iteration in range(max_iterations):
        new_solution = create_initial_solution(stocks, order)
        new_cost, new_demand_met = evaluate_solution(new_solution, stocks, order)
        
        cost_diff = new_cost - current_cost
        
        if new_demand_met and (cost_diff < 0 or random.random() < pow(2.718, -cost_diff / temperature)):
            current_solution = new_solution
            current_cost = new_cost
            current_demand_met = new_demand_met
            
            if new_demand_met and new_cost < best_cost:
                best_solution = new_solution
                best_cost = new_cost
                best_demand_met = new_demand_met
        
        temperature *= cooling_rate
    
    return best_solution, best_cost, best_demand_met

# Perform Simulated Annealing
start_time = time.time()
best_solution, best_cost, best_demand_met = simulated_annealing(order, stocks)
end_time = time.time()
execution_time = end_time - start_time

# Print the summary with patterns as vectors and costs
print("Summary of Steel Bars Usage and Demand Fulfillment:\n")

if best_demand_met:
    total_cost_by_stock = {stock_id: 0 for stock_id in stocks}

    for stock_id, patterns in best_solution.items():
        print(f"Stock {stock_id} (Length: {stocks[stock_id]['length']}):")
        pattern_index = 1
        for pattern_tuple, count in patterns.items():
            pattern_dict = dict(pattern_tuple)
            vector = [pattern_dict.get(demand, 0) for demand in order.keys()]
            pattern_cost = stocks[stock_id]['cost']
            total_cost_by_stock[stock_id] += pattern_cost * count
            print(f"  Pattern {pattern_index}: {vector} x{count} (Cost: ${pattern_cost} each)")
            pattern_index += 1

    print("\nTotal Cost by Stock Type:")
    for stock_id, cost in total_cost_by_stock.items():
        print(f"  {stock_id}: ${cost}")

    print(f"\nTotal Cost: ${best_cost}\n")
else:
    print("No feasible solution meets the demand.")

print(f"Execution Time: {execution_time:.4f} seconds")
