import time
from itertools import product
import time
# Dữ liệu của bạn
stocks = {
    "Type 1": {"length": 80, "cost": 90},
    "Type 2": {"length": 100, "cost": 110},
    "Type 3": {"length": 120, "cost": 130},
}

order = {
    "S": {"length": 15, "demand": 20},
    "M": {"length": 30, "demand": 10},
    "L": {"length": 34, "demand": 15},
    "XL": {"length": 47, "demand": 5},
}

def is_valid_pattern(pattern, order, stock_length):
    """Kiểm tra xem một mẫu cắt có hợp lệ không dựa trên chiều dài thanh thép và các ràng buộc đơn hàng."""
    total_length = sum(order[f]["length"] * count for f, count in pattern.items())
    return total_length <= stock_length

def generate_patterns(stock_length, order):
    """Sinh tất cả các mẫu cắt hợp lệ cho một chiều dài thanh thép."""
    max_cuts = [stock_length // order[f]["length"] for f in order]
    feasible_patterns = []
    
    for pattern in product(*(range(m + 1) for m in max_cuts)):
        pattern_dict = dict(zip(order.keys(), pattern))
        if is_valid_pattern(pattern_dict, order, stock_length):
            feasible_patterns.append(pattern_dict)
    
    return feasible_patterns

def modified_greedy_cutting(order, stocks):
    """Thực hiện thuật toán Greedy với điều chỉnh để tối thiểu hóa chi phí."""
    sorted_stocks = sorted(stocks.items(), key=lambda x: x[1]['cost'] / x[1]['length'])
    
    remaining_demand = {k: v['demand'] for k, v in order.items()}
    stock_usage = {stock_id: {} for stock_id in stocks}
    cut_counts = {demand: 0 for demand in order}
    total_cost = 0

    while any(remaining_demand[f] > 0 for f in remaining_demand):
        for stock_id, stock_info in sorted_stocks:
            stock_length = stock_info["length"]
            cost = stock_info["cost"]
            patterns = generate_patterns(stock_length, order)
            
            # Sắp xếp các mẫu theo tỷ lệ giữa tổng số lượng cắt được và tổng chiều dài đã cắt, bỏ qua mẫu cắt có tổng chiều dài = 0
            patterns = sorted(patterns, key=lambda p: sum(p.values()) / sum(order[f]["length"] * p[f] for f in p) if sum(order[f]["length"] * p[f] for f in p) > 0 else float('inf'), reverse=True)
            
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
                cut_counts[item] += best_pattern[item]
                remaining_demand[item] -= best_pattern[item]
            total_cost += best_pattern_cost

            if all(remaining_demand[f] <= 0 for f in remaining_demand):
                break
    
    return stock_usage, total_cost, cut_counts

# Thực hiện thuật toán Modified Greedy
# Bắt đầu đo thời gian
start_time = time.time()
stock_usage, total_cost, cut_counts = modified_greedy_cutting(order, stocks)
# Kết thúc đo thời gian
end_time = time.time()
# Tính toán thời gian thực thi
execution_time = end_time - start_time

# In kết quả
print("Summary of Steel Bars Usage and Demand Fulfillment:\n")

total_cost_by_stock = {stock_id: 0 for stock_id in stocks}

for stock_id, patterns in stock_usage.items():
    print(f"Stock {stock_id} (Length: {stocks[stock_id]['length']}):")
    pattern_index = 1
    for pattern_tuple, count in patterns.items():
        pattern_dict = dict(pattern_tuple)
        vector = [pattern_dict.get(demand, 0) for demand in order.keys()]
        pattern_cost = stocks[stock_id]['cost']
        total_cost_by_stock[stock_id] += pattern_cost * count
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