def policy_sailing_ln(state, boats, people):
    """
    state: object containing maps for 'x', 'y', 'v' of boats, 'd' of people, and 'saved' status
    boats: list of available boats [b0, b1]
    people: list of people to rescue [p0, p1]
    """
    
    # Phase 1: Rescue Check & Speed Boundary Enforcement
    # Iterate through all unsaved people to check if a boat is inside their rescue diamond
    for p in people:
        if not state.saved[p]:
            for b in boats:
                x_b, y_b, v_b = state.x[b], state.y[b], state.v[b]
                d_p = state.d[p]
                
                # Check the 4 standard linear geometric constraints for the diamond zone
                in_zone = (x_b + y_b >= d_p) and (y_b - x_b >= d_p) and \
                          (x_b + y_b <= d_p + 25) and (y_b - x_b <= d_p + 25)
                
                if in_zone:
                    # Crucial PDDL Precondition: Velocity must be <= 1 to perform a rescue
                    if v_b <= 1:
                        return f"save_person({b}, {p})"
                    else:
                        # If inside the zone but moving too fast, execute a braking action
                        return f"decelerate({b})"
                        
    # Phase 2: Cruise Navigation & Speed Management
    unsaved_people = [p for p in people if not state.saved[p]]
    if not unsaved_people:
        return "no_action (all people saved)"
        
    for b in boats:
        x_b, y_b, v_b = state.x[b], state.y[b], state.v[b]
        
        # Target the closest unsaved person based on latitude (y-axis)
        target_person = min(unsaved_people, key=lambda p: abs(y_b - (state.d[p] + 12.5)))
        d_p = state.d[target_person]
        target_y_center = d_p + 12.5
        
        # Cruise Control: If far away from the target y-center, maximize speed (up to v=3)
        if abs(y_b - target_y_center) > 20 and v_b < 3:
            return f"accelerate({b})"
            
        # Case A: Boat is North of the rescue zone (needs to go South)
        if y_b > d_p + 25:
            if x_b > 2:
                return f"go_south_east({b})" # Decreases both X and Y to realign to centerline
            elif x_b < -2:
                return f"go_south_west({b})" # Increases X, decreases Y to realign to centerline
            else:
                return f"go_south({b})"      # Direct descent along the X=0 centerline
                
        # Case B: Boat is South of the rescue zone (needs to go North)
        elif y_b < d_p:
            if x_b > 2:
                return f"go_north_west({b})" # Decreases X, increases Y
            elif x_b < -2:
                return f"go_north_east({b})" # Increases X, increases Y
            else:
                # No direct 'go_north' exists; alternate (zig-zag) to maintain alignment
                return f"go_north_west({b})" if x_b >= 0 else f"go_north_east({b})"
                
        # Case C: Correct latitude range, but outside X-axis boundaries of the diamond
        else:
            if x_b > 0:
                return f"go_west({b})" # High-yield horizontal shift (3 * v)
            elif x_b < 0:
                return f"go_est({b})"  # High-yield horizontal shift (3 * v)
                
    return "no_action (all boats stationary or waiting)"