def policy_sailing(state, boats, people):
    """
    state: object containing maps for 'x' and 'y' of boats, 'd' of people, and 'saved' status
    boats: list of available boats [b0, b1, b2, b3]
    people: list of people to rescue [p0, p1]
    """
    
    # Phase 1: Immediate Gratification (Rescue if inside the diamond zone)
    # Check if any boat is currently positioned to execute a save operation
    for p in people:
        if not state.saved[p]:
            for b in boats:
                x_b, y_b = state.x[b], state.y[b]
                d_p = state.d[p]
                
                # Verify the 4 linear PDDL constraints for save_person
                cond1 = (x_b + y_b) >= d_p
                cond2 = (y_b - x_b) >= d_p
                cond3 = (x_b + y_b) <= (d_p + 25)
                cond4 = (y_b - x_b) <= (d_p + 25)
                
                if cond1 and cond2 and cond3 and cond4:
                    return f"save_person({b}, {p})"
                    
    # Phase 2: Navigation (Steer boats toward the rescue zones)
    # If no immediate save is possible, navigate active boats toward unsaved targets
    unsaved_people = [p for p in people if not state.saved[p]]
    if not unsaved_people:
        return "no_action (all people saved)"
        
    for b in boats:
        x_b, y_b = state.x[b], state.y[b]
        
        # Greedily target the closest unsaved person based on latitude (y-axis)
        target_person = min(unsaved_people, key=lambda p: abs(y_b - (state.d[p] + 12.5)))
        d_p = state.d[target_person]
        
        # Case A: Boat is too far North (Needs to sail South)
        # The target zone spans from y = d_p to y = d_p + 25
        if y_b > d_p + 25:
            # Adjust longitude (x) on the way down to hit the x = 0 centerline
            if x_b > 2:
                return f"go_south_east({b})"
            elif x_b < -2:
                return f"go_south_west({b})"
            else:
                return f"go_south({b})"
                
        # Case B: Boat is too far South (Needs to sail North)
        elif y_b < d_p:
            # Tacking upwind toward the x = 0 centerline
            if x_b > 0:
                return f"go_north_west({b})"
            else:
                return f"go_north_east({b})"
                
        # Case C: Boat is at the correct latitude, but outside the X boundaries of the diamond
        else:
            if x_b > 0:
                return f"go_west({b})"
            elif x_b < 0:
                return f"go_est({b})"
                
    return "no_action (all boats stationary or waiting)"