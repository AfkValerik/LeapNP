#from unified_planning.model.fnode import Fnode
from fractions import Fraction
from data_structures.goals import checkIfGoal, hmax, hadd


class State:
    def __init__(self, values, g, h, parent = None, action = None):
        self.id = values.values()
        self.values = values
        self.g = g
        self.h = h
        self.f = g + h
        self.parent = parent
        self.action = action
        
    def __updatef__(self):
        self.f = self.g + self.h
        
    def _cmp_key(self):
        return (self.f,self.g)  
    
    def __eq__(self, other):
        return self._cmp_key() == other._cmp_key()
    
    def __lt__(self,other):
        return self._cmp_key() < other._cmp_key() 
    
    def __tostring__(self):
        return str(self.values) + " f = " + str(self.f) + "g =  " + str(self.g) + " h = " + str(self.h) 
    
    def __neighbors__ (self, actions):
        neighbors = list()
        for action in actions:
            if action.checkPreconditions(self):
                new_values = self.values.copy()
                action.applyEffects(new_values)
                neighbors.append(State(new_values,self.g + 1, 0, self.id, action))
        return neighbors
    
    def __is_goal__(self,goals):
        return checkIfGoal(self,goals)
    
    def __hadd__(self,goals):
        return hadd(self,goals)
    
    def __hmax__(self,goals):
        return hmax(self,goals)

def extractInitValues(state):
    new_state = dict()
    for key,value in state.items():
        new_state.update({key:value.value})
    return new_state

#TODO: those two methods should be put in the actions class, they are here due to some error while trying to import them, fix later 
def checkActionPreconditions(state,action):
    if "and" in str(action.action_expr.preconditions):
        toLoop = action.action_expr.preconditions[0].args
    else:
        toLoop = action.action_expr.preconditions
    for precondition in toLoop:
        if booleanCondition(precondition):
            if not state.values.get(precondition):
                return False
        else:
            actual_precondition = str(precondition)
            if "available" in actual_precondition:
                banana = True
            for fluent in action.precondition_fluents:
                fluent_value = state.values.get(fluent)
                #actual_precondition = actual_precondition.replace(str(fluent),str(fluent_value))
                # Suddividi il testo in parole
                actual_precondition = actual_precondition.replace(', ', ',')
                words = actual_precondition.split()
                
                for i, word in enumerate(words):
                    word = word.replace(',', ', ')
                    # Controlla se la parola è esattamente uguale al fluent
                    # e non è preceduta da un underscore
                    if str(fluent) in word:
                        if not ('_' in word and '_' not in str(fluent)):
                            words[i] = word.replace(str(fluent), str(fluent_value))
                actual_precondition = ' '.join(words)
            if (not eval(actual_precondition)):
                return False
    return True

def booleanCondition(condition):
    return all(c not in str(condition) for c in "=><+")

def applyActionEffects(state,action):
    for effect in action.action_expr.effects:
        state.update({effect.fluent: applyEffect(state.get(effect.fluent),effect,state)})


def applyEffect(value,effect,state):
    
    if effect.kind.value == 1:
        new_val = True if str(effect.value) == "true" else False
        
    elif effect.kind.value == 2:
        try:
            toadd = int(str(effect.value))
        except ValueError:
            toadd = state.get(effect.value)
            if toadd == None:
                if len(effect.value.args) > 1:
                    tmp1 = state.get(effect.value.args[0])
                    tmp2 = effect.value.args[1]
                    toadd = eval(str(apply(effect.value.node_type, tmp1, tmp2)))
                else:
                    toadd = getFloatValue(effect.value)
        new_val = value + toadd

    elif effect.kind.value == 3:
        try:
            toadd = int(str(effect.value))
        except ValueError:
            toadd = state.get(effect.value)
            if toadd == None:
                if len(effect.value.args) > 1:
                    tmp1 = state.get(effect.value.args[0])
                    tmp2 = effect.value.args[1]
                    toadd = eval(str(apply(effect.value.node_type, tmp1, tmp2)))
                else:
                    toadd = getFloatValue(effect.value)
        new_val = value - toadd
    else:
        return ArithmeticError("Effect not recognized")
    
    return new_val

def apply(operator, left, right):
    if operator.value == 18:
        return left * right
    else:
        return ArithmeticError("Math operator not recognized")
    
def getFloatValue(value):
    return float(Fraction(str(value)))
        
        
