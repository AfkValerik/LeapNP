from search_algorithms.SearchAlgorithm import SearchAlgorithm
from queue import PriorityQueue
from data_structures import State, CostState

class KBFSState(State):
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
                neighbors.append(KBFSState(new_values,self.g + 1, 0, self.id, action))
        return neighbors
    
    
class KBFS(SearchAlgorithm):
    """Best First Search

    Args:
        heuristic, weight, the weight is not used for BFS, use  WAStar for that
        
        version with deferred evaluation to speed up GNN-based heuristics, slower for classical heuristics, might lead to memory issues with large problems
    """
    def __init__(self, heuristic = lambda x,y : 0, w = 1) -> None:
        super().__init__()
        self.heuristic = heuristic
        self.w = w
        

    def solve(self, problem, k = 100) -> list:
        cost = dict()
        frontier = PriorityQueue()
        n = KBFSState(problem.init)
        
        frontier.put(n)

        cost[str(n.id)] = CostState(n.g)

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
        
        self.heuristic.__valuateStates__(toEvaluate)

        for t in toEvaluate:
            t.__updatef__()
            self.update_states_evaluated()

            if (problem.isGoal(t)):
                return self.extract_solution(t,cost)
            frontier.put(t)
            
        #main loop

        while (not frontier.empty()):
                n = frontier.get()
            
                self.update_expanded()
                toEvaluate = list()
                successors = problem.getSuccessors(n)
                
                for i in range(k - 1):
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
  

                if len(toEvaluate) > 0:
                    self.heuristic.__valuateStates__(toEvaluate)
                    for t in toEvaluate:
                        t.__updatef__()
                        self.update_states_evaluated()
                        frontier.put(t)
        return None


    
