
class Heuristic:
    
    def __init__(self, model, predicates, goal_predicates, objects, obj_encoding, num_conditions, goal_num_conditions, num_functions, goals):
        self.model = model
        self.predicates = predicates
        self.goal_predicates = goal_predicates
        self.objects = objects
        self.obj_encoding = obj_encoding
        self.num_conditions = num_conditions
        self.goal_num_conditions = goal_num_conditions
        self.num_functions = num_functions
        self.goals = goals
        
        
    def __valuateState__(self,state):
        raise Exception("Not implemented")