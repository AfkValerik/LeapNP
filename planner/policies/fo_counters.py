def policy_fn_counters(state, counters, max_int):
    """
    state: object containing maps for 'value' and 'rate_value' of each counter
    counters: ordered list of counters [c0, c1, ..., cn]
    max_int: maximum allowed value defined by the domain
    """
    n = len(counters)
    
    # Scan adjacent pairs to find the first goal violation
    for i in range(n - 1):
        c_curr = counters[i]
        c_next = counters[i + 1]
        
        val_curr = state.value[c_curr]
        val_next = state.value[c_next]
        
        # Check if the goal constraint v(c_i) + 1 <= v(c_{i+1}) is violated
        if val_curr + 1 > val_next:
            
            rate_curr = state.rate_value[c_curr]
            rate_next = state.rate_value[c_next]
            
            # To maintain fine control and prevent overshooting, we simulate the standard
            # counter domain by ensuring the rate_value is exactly 1 before modifying values.
            expected_rate_curr = max(1, rate_curr)
            expected_rate_next = max(1, rate_next)
            
            # Option 1: Try to decrement the current counter (c_curr)
            # Check if decrementing by expected rate keeps value >= 0 and doesn't break the left constraint
            if val_curr - expected_rate_curr >= 0:
                left_safe = (i == 0) or (state.value[counters[i - 1]] + 1 <= val_curr - expected_rate_curr)
                if left_safe:
                    if rate_curr == 0:
                        return f"increase_rate({c_curr})"
                    elif rate_curr > 1:
                        return f"decrement_rate({c_curr})"
                    else:
                        return f"decrement({c_curr})"
            
            # Option 2: Increment the next counter (c_next)
            # If decrementing left is not safe, try to raise the right side
            if val_next + expected_rate_next <= max_int:
                if rate_next == 0:
                    return f"increase_rate({c_next})"
                elif rate_next > 1:
                    return f"decrement_rate({c_next})"
                else:
                    return f"increment({c_next})"
                    
            # Option 3: Fallback (c_next is stuck at max_int)
            # Force decrement left, fixing cascade errors in future cycles
            if val_curr - expected_rate_curr >= 0:
                if rate_curr == 0:
                    return f"increase_rate({c_curr})"
                elif rate_curr > 1:
                    return f"decrement_rate({c_curr})"
                else:
                    return f"decrement({c_curr})"
                    
    # No violations found, all constraints are satisfied
    return "no_action (goal reached)"