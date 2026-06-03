def policy_counters(state, counters, max_int):
    """
    state: map associating each counter with its current value
    counters: ordered list of counters [c0, c1, ..., cn]
    max_int: maximum allowed value defined by the domain
    """
    n = len(counters)
    
    # Scan adjacent pairs to find the first goal violation
    for i in range(n - 1):
        c_curr = counters[i]
        c_next = counters[i + 1]
        
        val_curr = state[c_curr]
        val_next = state[c_next]
        
        # Check if the goal constraint v(c_i) + 1 <= v(c_{i+1}) is violated
        if val_curr + 1 > val_next:
            
            # Option 1: Try to decrement the current counter (c_curr)
            # It must respect the precondition (>= 1) and not break the constraint 
            # previously satisfied with the left counter (if i > 0)
            if val_curr >= 1:
                if i == 0 or state[counters[i - 1]] + 1 <= val_curr - 1:
                    return f"decrement({c_curr})"
            
            # Option 2: Increment the next counter (c_next)
            # If decrementing is not safe or possible, raise the value on the right
            if val_next < max_int:
                return f"increment({c_next})"
                
            # Option 3: Fallback (c_next is stuck at max_int)
            # Force the decrement on the left, even if it temporarily breaks the previous
            # ordering. Subsequent cycles will fix the cascading error.
            if val_curr >= 1:
                return f"decrement({c_curr})"
                
    # No violations found, all constraints are satisfied
    return "no_action (goal reached)"