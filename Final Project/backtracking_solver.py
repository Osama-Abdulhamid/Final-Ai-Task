import time

def solve_backtracking(items, bin_capacity):
    # ترتيب تنازلي عشان الـ Pruning يشتغل بأعلى كفاءة
    sorted_items = sorted(items, reverse=True)
    
    best_num_bins = float('inf')
    best_solution = []

    def backtrack(item_index, current_bins, bin_assignments):
        nonlocal best_num_bins, best_solution
        
        # 1. Pruning
        if len(current_bins) >= best_num_bins:
            return
        
        # 2. Base Case
        if item_index == len(sorted_items):
            best_num_bins = len(current_bins)
            best_solution = [list(b) for b in bin_assignments]
            return
        
        current_item = sorted_items[item_index]
        
        # 3. محاولة الوضع في الصناديق المفتوحة
        for i in range(len(current_bins)):
            if current_bins[i] >= current_item:
                current_bins[i] -= current_item
                bin_assignments[i].append(current_item)
                
                backtrack(item_index + 1, current_bins, bin_assignments)
                
                # Backtrack
                current_bins[i] += current_item
                bin_assignments[i].pop()
                
        # 4. فتح صندوق جديد
        if len(current_bins) + 1 < best_num_bins:
            current_bins.append(bin_capacity - current_item)
            bin_assignments.append([current_item])
            
            backtrack(item_index + 1, current_bins, bin_assignments)
            
            # Backtrack
            current_bins.pop()
            bin_assignments.pop()

    start_time = time.time()
    backtrack(0, [], [])
    end_time = time.time()
    
    return best_solution, (end_time - start_time)