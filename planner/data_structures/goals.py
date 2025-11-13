from data_structures.atom import extractGoalAtom
import re
class Goal:
    def __init__(self, goal_expr,atoms,bool_goal):
        self.goal_expr = goal_expr
        self.atoms = atoms
        self.bool_goal = bool_goal
        
    def checkGoal(self,state):
        if self.bool_goal:
            return  state.values[self.goal_expr]
        else:
            actual_goal = self.goal_expr
            for atom in self.atoms:
                pattern = rf'(?<!_)({re.escape(atom.name)})'
                actual_goal = re.sub(pattern, str(state[atom.name]), actual_goal)
            return eval(actual_goal)
        
def checkIfGoal(state,goals):
    for goal in goals:
        
        if goal.bool_goal:
            if not state.values[goal.goal_expr]:
                return False
        else:
            actual_goal = goal.goal_expr
            for atom in goal.atoms:
                pattern = rf'(?<!_)({re.escape(atom.name)})'
                actual_goal = re.sub(pattern, str(state.values[atom.name]), actual_goal)
                
            if (not eval(actual_goal)):
                return False
    return True

def goalDist(state,goal):
    tmp = 0
    actual_goal = goal.goal_expr
        
    for fluent in goal.fluents:
        fluent_value = state.values.get(fluent)
        actual_goal = actual_goal.replace(str(fluent),str(fluent_value))
            
    if not eval(actual_goal):
        actual_goal = actual_goal[1:-1]
        if 'or' in actual_goal:
            or_conditions = actual_goal.split('or')
            for i in or_conditions:
                val = 0
                if "==" in i:
                    if 'not' in i:
                        val = 1
                    else:
                        left_side, right_side = i.split("==")
                        val = abs(int(left_side) - int(right_side))
                if val > tmp:
                    tmp = val
                        
        elif 'and' in actual_goal:
            and_conditions = actual_goal.split('and')
            for i in and_conditions:
                val = 0
                if "==" in i:
                    if 'not' in i:
                        val = 1
                    else:
                        left_side, right_side = i.split("==")
                        val = abs(int(left_side) - int(right_side))
                tmp += val
                    
        else:
            condition = actual_goal
            if "==" in condition:
                if 'not' in condition:
                    tmp = 1
                else:
                    left_side, right_side = condition.replace(" ","").split("==")
                    tmp = abs(int(left_side) - int(right_side)) 
    return tmp

def hadd(state,goals):
    dist = 0
    for goal in goals:
        tmp = goalDist(state,goal)          
        dist += tmp
    return dist

def hmax(state,goals):
    dist = 0
    for goal in goals:
        tmp = goalDist(state,goal)
        if tmp > dist:
            dist = tmp          
    return dist

def standardizeGoals(goals):
    outputs = list() 
    for goal in goals:
        toOutput = standardizeGoal(goal)
        outputs.append(toOutput)
        
    return outputs
        
        
def standardizeGoal(goal):
    if booleanGoal(goal):
        #return Goal(str(goal),[getBooleanPredicate(goal,initial_state)],True)
        return Goal(str(goal),extractGoalAtom(goal),True)
    atoms = list()
    standardizeGoalRecursive(goal.args[0],atoms)
    standardizeGoalRecursive(goal.args[1],atoms)
    #TODO: modify with numeric goals
    return Goal(str(goal),atoms,False)
    
def standardizeGoalRecursive(condition,atoms):
    if len(condition.args) > 1:
        standardizeGoalRecursive(condition.args[0],atoms)
        standardizeGoalRecursive(condition.args[1],atoms)
    elif len(condition.args) == 1:
        standardizeGoalRecursive(condition.args[0],atoms)
    if condition.node_type.value == 8:
        if str(condition) not in atoms:
            atoms.append(extractGoalAtom(condition))

def booleanGoal(goal):
    return all(c not in str(goal) for c in "=><+")
    
    
def getBooleanPredicate(goal,initial_state):
    for i in initial_state:
        if str(i) == str(goal):
            return i
    return None
    


def extractOperatorKind(type):
    
    if type.value == 2:
        return "or"
    elif type.value == 16:
        return "+"
    elif type.value == 17:
        return "-"
    elif type.value == 20:
        return "<="
    elif type.value == 22:
        return "=="
    elif type.value == 8:
        return 'fluent'

    else:
        ValueError("Operator not supported")