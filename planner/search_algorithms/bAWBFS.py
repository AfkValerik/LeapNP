from search_algorithms.SearchAlgorithm import SearchAlgorithm
from queue import PriorityQueue
from data_structures import State, CostState

class AWBFSState(State):
    def __init__(self, values, g = 0, h = 0, parent = None, action = None) -> None:
        super().__init__(values, g, h, parent, action)
    
    def _cmp_key(self):
        return (self.h,self.g)  
    
    def __eq__(self, other):
        return self._cmp_key() == other._cmp_key()
    
    def __lt__(self,other):
        return self._cmp_key() < other._cmp_key()
    
    def __hash__(self):
        return hash(self.id)
    
    def __neighbors__ (self, actions):
        neighbors = list()
        for action in actions:
            if action.checkPreconditions(self.values):
                new_values = self.values.copy()
                action.applyEffects(new_values)
                neighbors.append(AWBFSState(new_values,self.g + 1, 0, self.id, action))
        return neighbors
    
    
class bAWBFS(SearchAlgorithm):
    """Best First Search

    Args:
        heuristic, weight, the weight is not used for BFS, use  WAStar for that
        
        version with deferred evaluation to speed up GNN-based heuristics, slower for classical heuristics, might lead to memory issues with large problems
        version with the possibility to go up and down with the width
    """
    def __init__(self, heuristic = lambda x,y : 0, w = 1) -> None:
        super().__init__()
        self.heuristic = heuristic
        self.w = w
        
#TODO: instead of using separate values to track the expanded and evaluated state to calculate the branching factor, directly use the existing variables from the search algorithm class
    def solve(self, problem, memory_limit = 8000) -> list:
        cost = dict()
        frontier = PriorityQueue()
        n = AWBFSState(problem.init)
        mem1, basemem = self.heuristic.__calculate_state_memory_usage__(n)
        width = 1
        
        frontier.put(n)
        #TODO: change values inside state to a list in order to use the cost dict correctly
        cost[str(n.id)] = CostState(n.g)
        #cost[problem.init] = 0
        self.reset_expanded()
        self.reset_states_evaluated()
        n = frontier.get()
        self.update_expanded()
        self.update_states_evaluated()
        if (problem.isGoal(n)):
            return self.extract_solution(n,cost)
        toEvaluate = list()
        for s in problem.getSuccessors(n):
            if str(s.id) not in cost or s.g < cost[str(s.id)].g:
                toEvaluate.append(s)
                cost[str(s.id)] = CostState(s.g,s.parent,s.action.name)
        
        mem2, numstates = self.heuristic.__calculate_states_memory_usage__(toEvaluate)
        mem2 = mem2 - basemem
        mem = (mem2 - mem1)/(numstates - 1)
        bf = len(problem.actions)
        print("currently expanding: ", width, " state at a time")
        print(f"Estimated memory usage for inference operations: {mem*bf:.2f} MB") 
        expanded_count_d1 = 0
        actual_successors = 0
        for t in toEvaluate:
            t.__updatef__()
            self.update_states_evaluated()

            if (problem.isGoal(t)):
                return self.extract_solution(t,cost)
            frontier.put(t)
            
        besth = 1000000
        #main loop

        while (not frontier.empty()):
                n = frontier.get()
                if n.h < besth:
                    if width > 1 and n.h + 0.5 < besth:
                        width -= 1
                        print("decreasing parallel expansions to: ", width)
                    besth = n.h
                else:
                        if width == 1:
                            bf = actual_successors / expanded_count_d1
                            print("average branching factor calculated: ", bf)
                        if mem * (bf*(width + 1)) < memory_limit:
                            width += 1
                            print("increasing parallel expansions to: ", width)
                            print(f"Estimated memory usage for inference operations: {mem*(bf*width):.2f} MB") 
            
                self.update_expanded()
                toEvaluate = list()
                successors = problem.getSuccessors(n)
                if width > 1:
                    for i in range(width - 1):
                        if not frontier.empty():
                            new = frontier.get()
                            successors.extend(problem.getSuccessors(new))
                            self.update_expanded()
                for s in successors:
                    if str(s.id) not in cost or s.g < cost[str(s.id)].g:
                        toEvaluate.append(s)
                        cost[str(s.id)] = CostState(s.g,s.parent,s.action.name)
                        if (problem.isGoal(s)):
                            return self.extract_solution(s,cost)
                if width == 1:
                    expanded_count_d1 += 1
                    actual_successors += len(successors)

                if len(toEvaluate) > 0:
                    self.heuristic.__valuateStates__(toEvaluate)
                    for t in toEvaluate:
                        t.__updatef__()
                        self.update_states_evaluated()
                        frontier.put(t)
        return None


    
