import time
import matplotlib.pyplot as plt
from itertools import product
import numpy as np
import random
import time
import tracemalloc

stocks = {
    "Type 1": {"length": 80, "cost": 90},
    "Type 2": {"length": 100, "cost": 110},
}

# Define the order requirements with their lengths and demands
order = {
    "A": {"length": 20, "demand": 5},
    "B": {"length": 30, "demand": 3},
}

# # Steel stock data with more types
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

#  # Define stock information with their lengths and costs
# stocks = {
#     "Type 1": {"length": 80, "cost": 100},
#     "Type 2": {"length": 100, "cost": 150},
#     "Type 3": {"length": 120, "cost": 200},
# }
# # Define steel stock data with various types
# order = {
#     "S": {"length": 10, "demand": 50},
#     "M": {"length": 20, "demand": 30},
#     "L": {"length": 30, "demand": 20},
#     "XL": {"length": 40, "demand": 10},
# }
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

# ======================================================
def ffd_heuristic(stocks, order):
    """
    Applies the First-Fit Decreasing heuristic to the cutting stock problem.

    Args:
        stocks: A dictionary containing stock types, their lengths, and costs.
        order: A dictionary containing order types, their lengths, and demands.

    Returns:
        A dictionary representing the solution, where keys are stock types and
        values are dictionaries of cutting patterns and their counts.
    """

    # Sort order items by decreasing length
    order_items = sorted(order.items(), key=lambda x: x[1]["length"], reverse=True)

    # Initialize residual demands
    residual_demands = {item: details["demand"] for item, details in order.items()}

    # Initialize solution dictionary
    solution = {stock_id: {} for stock_id in stocks}

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
                pattern_tuple = tuple(sorted(pattern.items()))
                if pattern_tuple not in solution[stock_type]:
                    solution[stock_type][pattern_tuple] = 0
                solution[stock_type][pattern_tuple] += 1

    return solution

# ======================================================

# Hàm để đo thời gian thực hiện của Greedy và SA
optimal_value = 220  # Giá trị tối ưu (nếu biết)

# Modified measure_performance function to include FFD
def measure_performance(order, stocks, optimal_value=None, iterations=10):
    greedy_times = []
    greedy_results = []
    greedy_deviations = []
    sa_times = []
    sa_results = []
    sa_deviations = []
    ffd_times = []
    ffd_results = []
    ffd_deviations = []

    for _ in range(iterations):
        # Measure Greedy
        start_time = time.time()
        _, greedy_cost, _ = greedy_cutting(order, stocks)
        greedy_times.append(time.time() - start_time)
        greedy_results.append(greedy_cost)

        # Measure Simulated Annealing
        start_time = time.time()
        _, sa_cost, _ = simulated_annealing(order, stocks)
        sa_times.append(time.time() - start_time)
        sa_results.append(sa_cost)

        # Measure FFD
        start_time = time.time()
        ffd_solution = ffd_heuristic(stocks, order)
        ffd_cost, _ = evaluate_solution(ffd_solution, stocks, order)
        ffd_times.append(time.time() - start_time)
        ffd_results.append(ffd_cost)

    # Calculate deviations if optimal_value is provided
    if optimal_value is not None:
        greedy_deviations = [abs(cost - optimal_value) / optimal_value * 100 for cost in greedy_results]
        sa_deviations = [abs(cost - optimal_value) / optimal_value * 100 for cost in sa_results]
        ffd_deviations = [abs(cost - optimal_value) / optimal_value * 100 for cost in ffd_results]

    return (greedy_times, greedy_results, greedy_deviations,
            sa_times, sa_results, sa_deviations,
            ffd_times, ffd_results, ffd_deviations)

# Measure performance including FFD
greedy_times, greedy_results, greedy_deviations, sa_times, sa_results, sa_deviations, ffd_times, ffd_results, ffd_deviations = measure_performance(order, stocks, optimal_value)

# Compare average times
average_greedy_time = sum(greedy_times) / len(greedy_times)
average_sa_time = sum(sa_times) / len(sa_times)
average_ffd_time = sum(ffd_times) / len(ffd_times)

print(f"Average Greedy Time: {average_greedy_time:.6f} seconds")
print(f"Average Simulated Annealing Time: {average_sa_time:.6f} seconds")
print(f"Average FFD Time: {average_ffd_time:.6f} seconds")

# Plotting - Modify to include FFD
plt.figure(figsize=(12, 6))

# Subplot 1: Execution Time
plt.subplot(1, 2, 1)
plt.plot(greedy_times, label='Greedy', marker='o')
plt.plot(sa_times, label='Simulated Annealing (SA)', marker='x')
plt.plot(ffd_times, label='First-Fit Decreasing (FFD)', marker='s')  # Add FFD plot
plt.xlabel('Iteration')
plt.ylabel('Time (seconds)')
plt.title('Comparison of Execution Time')
plt.legend()
plt.grid(True)

# Subplot 2: Solution Cost
plt.subplot(1, 2, 2)
plt.plot(greedy_results, label='Greedy', marker='o')
plt.plot(sa_results, label='Simulated Annealing (SA)', marker='x')
plt.plot(ffd_results, label='First-Fit Decreasing (FFD)', marker='s')  # Add FFD plot
if optimal_value is not None:
    plt.axhline(y=optimal_value, color='r', linestyle='--', label='Optimal Solution')
plt.xlabel('Iteration')
plt.ylabel('Solution Cost')
plt.title('Comparison of Solutions with Optimal Value')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
