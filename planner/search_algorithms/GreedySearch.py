from search_algorithms.SearchAlgorithm import SearchAlgorithm
from data_structures import State, checkActionPreconditions, applyActionEffects

class GSState(State):
    def __init__(self, values, g = 0, h = 0, parent = None, action = None) -> None:
        super().__init__(values, g, h, parent, action)
        
    def _cmp_key(self):
        return (self.h,self.g)  
    
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
                neighbors.append(GSState(new_values,self.g + 1, 0, self.id, action))
        return neighbors
    

    
class GS(SearchAlgorithm):
    """Best First Search

    Args:
        Solver (_type_): This is an implementation for the Solver class
    """
    def __init__(self, heuristic = lambda x,y : 0, w = 1) -> None:
        self.heuristic = heuristic
        self.w = w
        
    def extract_solution(self, current_state, closed_list) -> str:
        path = ""
        goal = current_state.values
        path = str(closed_list)    
        return path,goal
    
    
    def solve(self, problem) -> list:
        actions = list()
        running = True
        n = GSState(problem.init)
        self.reset_expanded()
        while (running):

            self.update_expanded()
            if (problem.isGoal(n)):
                return self.extract_solution(n,actions)
            
            toEvaluate = problem.getSuccessors(n)
            
            if len(toEvaluate) > 0:
                n = self.heuristic.__generalPolicy__(toEvaluate,n)
                n.__updatef__()
                actions.append(n.action.action_expr.name)
            else:
                running = False
                
        return None