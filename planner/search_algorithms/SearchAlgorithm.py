class SearchAlgorithm:
    def __init__(self) -> None:
        self.expanded = 0
        self.evaluated = 0
        #self.expanded_states = set()

    def solve(self, problem) -> list:
        raise Exception("Not implemented")
    
    def update_expanded(self):
        self.expanded += 1
    def reset_expanded(self):
        self.expanded = 0
    def reset_states_evaluated(self):
        self.evaluated = 0
    def update_states_evaluated(self):
        self.evaluated += 1
   # def extract_solution(self, node) -> list:
   #     sol = list()
   #     while (node.parent is not None):
   #         sol.insert(0,node.action)
   #         node = node.parent
   #     return sol
   
    def extract_solution(self, current_state,closed_list) -> str:
        path = ""
        goal = current_state.values
        current_state = closed_list.get(str(current_state.id))
        while current_state:
                
            if current_state.parent is not None:
                path = current_state.action + "\n" + path
                current_state = closed_list.get(str(current_state.parent))
            else:
                current_state = False
                
        return path,goal