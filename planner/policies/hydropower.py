def policy_hydropower(state, timeline, target_funds):
    """
    state: object containing current funds, stored_units, stored_capacity, and timenow
    timeline: helper object that parses static 'before', 'demand', and 'value' predicates
    target_funds: the goal value for funds (e.g., 1080)
    """
    # Check if the goal is already satisfied
    if state.funds >= target_funds:
        return "no_action (goal reached)"

    current_time = state.timenow
    current_demand_node = timeline.get_demand_node(current_time) # e.g., "n7"
    current_price = timeline.get_value(current_demand_node)      # e.g., 7
    
    # Analyze future market trends based on static initial state knowledge
    max_future_price = timeline.get_max_future_price(current_time)
    is_local_minimum = timeline.is_trough(current_time) # True if price starts rising next step
    is_local_maximum = timeline.is_peak(current_time)   # True if price starts dropping next step

    # Option 1: GENERATE (Sell High)
    # We can generate multiple times in the same time step as long as we have water.
    # We sell if we are at a market peak, at the absolute maximum price, 
    # or if selling right now allows us to immediately reach the target funds.
    if state.stored_units >= 1:
        if is_local_maximum or current_price == max_future_price or (state.funds + current_price >= target_funds):
            return f"generate({current_time}, {current_demand_node})"

    # Option 2: PUMP WATER UP (Buy Low)
    # We can pump multiple times as long as we have empty capacity and enough funds.
    cost_to_pump = 1.05 * current_price
    if state.stored_capacity >= 1 and state.funds >= cost_to_pump:
        # We buy ONLY if we are at a local minimum and the future peak price 
        # is high enough to guarantee a profit over the 1.05 multiplier.
        if is_local_minimum and cost_to_pump < max_future_price:
            return f"pump_water_up({current_time}, {current_demand_node})"

    # Option 3: ADVANCE TIME
    # If no profitable trades can be made (or if capacity/units are exhausted for this time step),
    # move to the next chronological time step.
    next_time = timeline.get_next_time(current_time)
    if next_time is not None:
        return f"advance_time({current_time}, {next_time})"
        
    # Fallback if timeline ends before reaching the goal
    return "no_action (dead end)"