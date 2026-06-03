def policy_farmland(state, graph, weights, target_benefit):
    """
    state: map associating each farm with its current worker count 'x'
    graph: adjacency list representing the 'adj' predicates
    weights: map of the benefit coefficients for each farm (from the goal)
    target_benefit: the float value to reach (e.g., 560.0)
    """
    
    # Helper function to calculate the current total benefit
    current_benefit = sum(state[f] * weights[f] for f in state)
    
    # Phase 1: Satisfy the hard constraint (x >= 1 for all farms)
    # Identify farms that currently have 0 workers
    starving_farms = [f for f in state if state[f] < 1]
    if starving_farms:
        target_starving = starving_farms[0]
        
        # Find a farm with surplus workers (x > 1) to supply the starving ones
        for source in state:
            if state[source] > 1:
                # Calculate the shortest path in the graph from source to the starving farm
                path = find_shortest_path(graph, source, target_starving)
                if path:
                    next_hop = path[1] # The immediate next node in the path
                    return f"move-slow({source}, {next_hop})"
                    
    # Phase 2: Maximize benefit if the target is not yet reached
    if current_benefit < target_benefit:
        # Identify the farm with the highest global weight to act as a "sink"
        best_farm = max(weights, key=weights.get)
        
        # Move surplus workers towards the best_farm to maximize the linear combination
        for f in state:
            # We only move workers if they are not already at the best farm,
            # and if removing 1 worker doesn't violate the x >= 1 constraint.
            if f != best_farm and state[f] > 1:
                
                # Route the worker step-by-step towards the best_farm
                path = find_shortest_path(graph, f, best_farm)
                if path:
                    next_hop = path[1]
                    return f"move-slow({f}, {next_hop})"
                    
    # Phase 3: No violations and target reached
    return "no_action (goal reached)"

def find_shortest_path(graph, start, end):
    """
    Standard Breadth-First Search (BFS) to find the shortest path 
    between two nodes in an unweighted graph. Returns a list of nodes.
    """
    # Implementation omitted for brevity (standard BFS queue logic)
    pass