def policy_farmland_ln(state, graph, weights, target_benefit):
    """
    state: object exposing 'x' (map of workers per farm), 'num_of_cars', and 'cost'
    graph: adjacency list representing the 'adj' topology
    weights: map of the benefit coefficients (e.g., farm1: 1.7)
    target_benefit: the float value to reach (e.g., 420.0)
    """
    # Calculate current score: linear combination minus the accumulated cost
    current_score = sum(state.x[f] * weights[f] for f in state.x) - state.cost
    
    # Phase 1: Satisfy the hard constraint (x >= 1 for all farms)
    starving_farms = [f for f in state.x if state.x[f] < 1]
    if starving_farms:
        target_starving = starving_farms[0]
        
        # Route a single worker from the nearest surplus farm using free slow moves
        for source in state.x:
            if state.x[source] > 1:
                path = find_shortest_path(graph, source, target_starving)
                if path:
                    next_hop = path[1]
                    # We use move-slow to avoid paying cost penalties during constraint satisfaction
                    return f"move-slow({source}, {next_hop})"
                    
    # Phase 2: Maximize benefit metric
    if current_score < target_benefit:
        best_farm = max(weights, key=weights.get)
        cars = state.num_of_cars
        
        for f in state.x:
            if f != best_farm and state.x[f] > 1:
                surplus = state.x[f] - 1
                
                # Action Selection Logic:
                # 1. Evaluate if we need to scale up our transport capacity.
                # We hire a car if the surplus is large enough to utilize an additional car,
                # capping the max cars (e.g., at 10) to prevent infinite hiring loops.
                if surplus >= 4 * (cars + 1) and cars < 10:
                    return "hire-car()"
                
                # 2. Route the surplus towards the maximum yield node
                path = find_shortest_path(graph, f, best_farm)
                if path:
                    next_hop = path[1]
                    
                    # 3. Use bulk transport if we have enough units to fill the fleet
                    if surplus >= 4 * cars and cars > 0:
                        return f"move-by-car({f}, {next_hop})"
                    else:
                        # Fallback for remainders that don't fill the car capacity
                        return f"move-slow({f}, {next_hop})"
                        
    # Phase 3: Goal conditions met
    return "no_action (goal reached)"

def find_shortest_path(graph, start, end):
    """
    Standard BFS to find the shortest unweighted path.
    Returns a list of nodes, e.g., [farm0, farm1]
    """
    # Implementation omitted
    pass