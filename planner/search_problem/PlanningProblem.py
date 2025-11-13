from search_problem.SearchProblem import SearchProblem

class PlanningProblem(SearchProblem):
    
    def __init__(self, init, goal, actions):
        super().__init__(init, goal, actions)
        
    def getSuccessors(self, state) -> set:
        
        return state.__neighbors__(self.actions)
    
    def isGoal(self,state) -> bool:
        return state.__is_goal__(self.goal)