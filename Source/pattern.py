from itertools import product
import matplotlib.pyplot as plt
import numpy as np
import random

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

# Display patterns
for stock_id, patterns in all_patterns.items():
    print(f"\nPatterns for stock {stock_id} (length {stocks[stock_id]['length']}):")
    for i, pattern in enumerate(patterns):
        total_length = sum(order[f]["length"] * count for f, count in pattern.items())
        remaining_length = stocks[stock_id]['length'] - total_length
        print(f"Pattern {i+1}: {pattern}, Total length: {total_length}, Remaining length: {remaining_length}")

# Optionally, save patterns to a JSON file
import json
with open('patterns.json', 'w') as f:
    json.dump(all_patterns, f)
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def plot_pattern(stock_length, pattern, order, ax, stock_label):
    """
    Plot the cutting pattern on a chart.
    """
    x_offset = 0
    colors = {'S': 'red', 'M': 'blue', 'L': 'green', 'XL': 'orange'}
    
    # Add cutting pieces to the chart
    for size, count in pattern.items():
        piece_length = order[size]['length']
        for _ in range(count):
            # Create a rectangle for each piece and add it to the plot
            rect = patches.Rectangle((x_offset, 0), piece_length, 1, linewidth=1, edgecolor='black', facecolor=colors[size])
            ax.add_patch(rect)
            x_offset += piece_length
    
    # Draw the remaining part of the stock bar if there is any leftover
    if x_offset < stock_length:
        remaining_length = stock_length - x_offset
        # Create a rectangle for the remaining part with a dashed line style
        rect = patches.Rectangle((x_offset, 0), remaining_length, 1, linewidth=1, edgecolor='black', facecolor='gray', linestyle='--')
        ax.add_patch(rect)
    
    # Set the x-axis limits and ticks
    ax.set_xlim(0, stock_length)
    ax.set_ylim(0, 1.5)
    ax.set_yticks([])
    ax.set_xticks([x for x in range(0, stock_length + 1, 10)])
    ax.set_xticklabels([str(x) for x in range(0, stock_length + 1, 10)])
    ax.set_title(stock_label)
    
    # Add a legend to the chart
    patches_list = [patches.Patch(color=color, label=label) for label, color in colors.items()]
    ax.legend(handles=patches_list, loc='upper left')

# Create subplots for each stock type
fig, axs = plt.subplots(len(stocks), figsize=(12, 3 * len(stocks)))
for ax, (stock_id, stock_info) in zip(axs, stocks.items()):
    stock_length = stock_info['length']
    patterns = all_patterns[stock_id]
    for i, pattern in enumerate(patterns[:3]):  # Only plot the first 3 patterns for each stock type
        plot_pattern(stock_length, pattern, order, ax, f"{stock_id} - Pattern {i+1}")

plt.tight_layout()
plt.show()