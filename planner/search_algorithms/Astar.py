from search_algorithms.SearchAlgorithm import SearchAlgorithm
from queue import PriorityQueue
from data_structures import State, checkActionPreconditions, applyActionEffects, CostState

class AstarState(State):
    def __init__(self, values, g = 0, h = 0, parent = None, action = None) -> None:
        super().__init__(values, g, h, parent, action)
    
    def _cmp_key(self):
        return (self.f,self.g)  
    
    def __eq__(self, other):
        return self._cmp_key() == other._cmp_key()
    
    def __lt__(self,other):
        return self._cmp_key() < other._cmp_key() 

    def __neighbors__ (self, actions):
        neighbors = list()
        for action in actions:
            if action.checkPreconditions(self.values):
                new_values = self.values.copy()
                action.applyEffects(new_values)
                neighbors.append(AstarState(new_values,self.g + 1, 0, self.id, action))
        return neighbors
    
class Astar(SearchAlgorithm):
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
        n = AstarState(problem.init)
        frontier.put(n)
        #TODO: change values inside state to a list in order to use the cost dict correctly
        cost[str(n.id)] = CostState(n.g)
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
                    if str(s.id) not in cost or n.g < cost[str(s.id)].g:
                        self.heuristic.__valuateState__(s)
                        s.__updatef__()
                        self.update_states_evaluated()
                        cost[str(s.id)] = CostState(s.g,s.parent,s.action.name)
                        if (problem.isGoal(s)):
                            return self.extract_solution(s,cost)
                        frontier.put(s)
        return None
    
    
class MEAstar(SearchAlgorithm):
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
        n = AstarState(problem.init)
        frontier.put(n)
        #TODO: change values inside state to a list in order to use the cost dict correctly
        cost[str(n.id)] = CostState(n.g)
        #cost[problem.init] = 0
        self.reset_expanded()
        self.reset_states_evaluated()
        while (not frontier.empty()):
                n = frontier.get()
            #TODO: understand why this is here
            #if cost[n.state] == n.g:
                self.update_expanded()
                if (problem.isGoal(n)):
                    return self.extract_solution(n,cost)
                toEvaluate = list()
                for s in problem.getSuccessors(n):
                    if str(s.id) not in cost or s.g < cost[str(s.id)].g:
                        toEvaluate.append(s)
                if len(toEvaluate) > 0:
                    self.heuristic.__valuateStates__(toEvaluate)
                    for t in toEvaluate:
                        t.__updatef__()
                        cost[str(t.id)] = CostState(t.g,t.parent,t.action.name)
                        self.update_states_evaluated()
                        #TODO: check if it is corrrect to put the goal here
                        if (problem.isGoal(t)):
                            return self.extract_solution(t,cost)
                        frontier.put(t)
        return None