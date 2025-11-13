from search_algorithms.SearchAlgorithm import SearchAlgorithm
from queue import PriorityQueue
from data_structures import State, checkActionPreconditions, applyActionEffects, CostState

class WAstarState(State):
    def __init__(self, values, g = 0, h = 0, parent = None, action = None) -> None:
        super().__init__(values, g, h, parent, action)
    
    def __updatef__(self, w = 1):
        self.f = self.g + w* self.h
        
    def _cmp_key(self):
        return (self.f,self.g)  
    
    def __eq__(self, other):
        return self._cmp_key() == other._cmp_key()
    
    def __lt__(self,other):
        return self._cmp_key() < other._cmp_key() 

    def __neighbors__ (self, actions):
        neighbors = list()
        for action in actions:
            if checkActionPreconditions(self,action):
                new_values = self.values.copy()
                applyActionEffects(new_values,action)
                neighbors.append(WAstarState(new_values,self.g + 1, 0, self.id, action))
        return neighbors
    
class WAstar(SearchAlgorithm):
    """AStar First Search

    Args:
        Solver (_type_): This is an implementation for the Solver class
    """
    def __init__(self, heuristic = lambda x,y : 0, w = 1) -> None:
        self.heuristic = heuristic
        self.w = w
        

    def solve(self, problem) -> list:
        cost = dict()
        frontier = PriorityQueue()
        n = WAstarState(problem.init)
        frontier.put(n)
        #TODO: change values inside state to a list in order to use the cost dict correctly
        cost[n.id] = CostState(n.g)
        #cost[problem.init] = 0
        self.reset_expanded()
        while (not frontier.empty()):
                n = frontier.get()
            #TODO: understand why this is here
            #if cost[n.state] == n.g:
                self.update_expanded()
                if (problem.isGoal(n)):
                    return self.extract_solution(n,cost)
                for s in problem.getSuccessors(n):
                    if s.id not in cost or n.g < cost[s.id].g:
                        self.heuristic.__valuateState__(s)
                        s.__updatef__(self.w)
                        cost[s.id] = CostState(s.g,s.parent,s.action.action_expr.name)
                        frontier.put(s)
        return None
    
    
class MEWAstar(SearchAlgorithm):
    """AStar First Search

    Args:
        Solver (_type_): This is an implementation for the Solver class
    """
    def __init__(self, heuristic = lambda x,y : 0, w = 1) -> None:
        self.heuristic = heuristic
        self.w = w
        

    def solve(self, problem) -> list:
        cost = dict()
        frontier = PriorityQueue()
        n = WAstarState(problem.init)
        frontier.put(n)
        #TODO: change values inside state to a list in order to use the cost dict correctly
        cost[n.id] = CostState(n.g)
        #cost[problem.init] = 0
        self.reset_expanded()
        while (not frontier.empty()):
                n = frontier.get()
            #TODO: understand why this is here
            #if cost[n.state] == n.g:
                self.update_expanded()
                if (problem.isGoal(n)):
                    return self.extract_solution(n,cost)
                toEvaluate = list()
                for s in problem.getSuccessors(n):
                    if s.id not in cost or n.g < cost[s.id].g:
                        toEvaluate.append(s)
                if len(toEvaluate) > 0:
                    self.heuristic.__valuateStates__(toEvaluate)
                    for t in toEvaluate:
                        t.__updatef__(self.w)
                        cost[t.id] = CostState(t.g,t.parent,t.action.action_expr.name)
                        frontier.put(t)
        return None