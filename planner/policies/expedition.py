def policy_expedition(state, sleds, waypoints, goal):
    """
    state: object mapping sleds and waypoints to their current supplies
    sleds: list of sleds [s0, s1, ...]
    waypoints: ordered list of waypoints [wa0, wa1, ..., wa8]
    goal: target waypoint (wa8)
    """
    goal_idx = waypoints.index(goal)
    
    for sled in sleds:
        loc = state.at[sled]
        idx = waypoints.index(loc)
        
        if loc == goal:
            continue # Sled has reached the destination
            
        sup = state.sled_supplies[sled]
        cap = state.sled_capacity[sled]
        wp_sup = state.waypoint_supplies[loc]
        
        dist_to_goal = goal_idx - idx
        
        # Rule 1: Direct Finish
        # If the sled has enough supplies to walk directly to the goal, do it.
        if sup >= dist_to_goal:
            next_wp = waypoints[idx + 1]
            return f"move_forwards({sled}, {loc}, {next_wp})"
            
        # Rule 2: Load Supplies (The "Breadcrumb" Logic)
        # We pick up supplies if we have space. 
        # CRITICAL: We only fully load at a forward base if doing so leaves at least 
        # 1 supply behind (wp_sup + sup > cap). This guarantees the return path is not destroyed.
        # We also load unconditionally if we are at the main base (idx == 0) or completely empty.
        if wp_sup > 0 and sup < cap:
            if idx == 0 or (wp_sup + sup > cap) or sup == 0:
                return f"retrieve_supplies({sled}, {loc})"
                
        # Rule 3: Advance
        # If the sled is fully loaded, it pushes the supply frontier forward.
        if sup == cap:
            next_wp = waypoints[idx + 1]
            return f"move_forwards({sled}, {loc}, {next_wp})"
            
        # Rule 4: Cache (Drop Supplies)
        # If we moved forward (not full, but > 1 supply), drop supplies to build a cache.
        # We keep exactly 1 supply as a return ticket.
        if 1 < sup < cap:
            return f"store_supplies({sled}, {loc})"
            
        # Rule 5: Return
        # If we have exactly 1 supply and are not at the main base, return to get more.
        if sup == 1 and idx > 0:
            prev_wp = waypoints[idx - 1]
            return f"move_backwards({sled}, {loc}, {prev_wp})"
            
    return "no_action (all sleds at goal or waiting)"