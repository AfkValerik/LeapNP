from data_structures.atom import extractPreconditionAtom, extractEffectAtom, extractPreconditionGnnAtom
import re
from scipy.optimize import linear_sum_assignment
from Levenshtein import ratio
import numpy as np
from sympy import expand

class Precondition:
    def __init__(self, name, atoms, is_bool):
        self.name = name
        self.atoms = atoms
        self.is_bool = is_bool
        #if precondition_map != None:
        #    self.normalized = precondition_map[name][0]
        #else:
        #    self.normalized = None
        
    def __eq__(self, value):
        return self.name == value.name
    
    def __hash__(self):
        return hash(self.name)
    
    def __lt__(self,value):
        return len(self.atoms) < len(value.atoms)
    
    def getObjects(self):
        objects = set()
        for atom in self.atoms:
            for obj in atom.objects:
                objects.add(obj)
        return list(objects)
    
    def checkPrecondition(self,state):
        if self.is_bool:
            if "not" in self.name:
                return not state[self.atoms[0].name]
            return state[self.atoms[0].name]

        else:
            newVal = self.name
            for atom in self.atoms:
                pattern = rf'(?<!_)({re.escape(atom.name)})'
                newVal = re.sub(pattern, str(state[atom.name]), newVal)
                #newVal = newVal.replace(atom.name,str(state[atom.name]))
            return eval(newVal)
        
    def orderAtoms(self,condition):
        if len(self.atoms) > 1:
            newAtoms = list()
            pattern = r'(^|(?<=\s))([^\s(]*\s*\([^)]*\))'
            liftedAtoms = re.findall(pattern, condition)
            liftedAtoms = [i[1] for i in liftedAtoms]
            for i in liftedAtoms:
                for atom in self.atoms:
                    if i.split("(")[0] == atom.fluent:
                        newAtoms.append(atom)
                        break
            self.atoms = newAtoms
        
class Effect:
    def __init__(self, name, atoms,lhs, rhs, is_effect_bool,operator):
        self.name = name
        self.atoms = atoms
        self.is_bool = is_effect_bool
        self.lhs = lhs
        self.rhs = rhs
        self.operator = operator
        
    def applyEffect(self,state):
        if self.is_bool:
            state[self.lhs] = self.rhs
        else:
            newVal = self.lhs + " " + self.operator +" "+  self.rhs
            for atom in self.atoms:
                pattern = rf'(?<!_)({re.escape(atom.name)})'
                newVal = re.sub(pattern, str(state[atom.name]), newVal)
                #newVal = newVal.replace(atom.name,str(state[atom.name]))
            state[self.lhs] = eval(newVal)
        
class Action:
    def __init__(self, name, preconditions, effects):
        self.name = name
        self.preconditions = preconditions
        self.effects = effects
    
    def __eq__(self, value):
        return self.name == value.name
    
    def checkPreconditions(self,state):
        for precondition in self.preconditions:
            if not precondition.checkPrecondition(state):
                return False
        return True
    
    def applyEffects(self,state):
        for effect in self.effects:
            effect.applyEffect(state)
    
    def hasBoolEffects(self):
        for effect in self.effects:
            if effect.is_bool:
                return True
        return False
        

class GNNAction:
    def __init__(self, name, preconditions):
        self.name = name
        self.preconditions = preconditions
    
    def __eq__(self, value):
        return self.name == value.name
    
    def checkPreconditions(self,state):
        for precondition in self.preconditions:
            if not precondition.checkPrecondition(state):
                return False
        return True
    
def standardizeActions(actions):
    outputs = list() 
    for action in actions:
        toOutput = standardizeaction(action)
        outputs.append(toOutput)
        
    return outputs
        
        
def standardizeaction(action):
    preconditions = list()
    effects = list()
    if "and" in str(action.preconditions):
        toLoop = action.preconditions[0].args
    else:
        toLoop = action.preconditions
    for precondition in toLoop:
        precondition_fluents = list()
        is_bool_wrapper = [True]
        standardizePreconditionRecursive(precondition,precondition_fluents,is_bool_wrapper)
        preconditions.append(Precondition(str(precondition),precondition_fluents,is_bool_wrapper[0]))
    for effect in action.effects:
        effect_fluents = list()
        is_effect_bool = True
        if not str(effect.fluent.type) == "bool":
            is_effect_bool = False
        effect_fluents.append(extractEffectAtom(effect.fluent))
        lhs = str(effect.fluent) 
        if is_effect_bool:
            if str(effect.value) == "true":
                rhs = True
            else:
                rhs = False
        else:
            rhs = str(effect.value)
            standardizeEffectRecursive(effect.value,effect_fluents)
        effects.append(Effect(str(effect),effect_fluents,lhs,rhs,is_effect_bool,getEffect(effect)))
    return Action(action.name,preconditions, effects)
    

    
    
def standardizePreconditionRecursive(condition,fluents,is_bool_wrapper):
    if len(condition.args) > 1:
        standardizePreconditionRecursive(condition.args[0],fluents,is_bool_wrapper)
        standardizePreconditionRecursive(condition.args[1],fluents,is_bool_wrapper)
    elif len(condition.args) == 1:
        standardizePreconditionRecursive(condition.args[0],fluents,is_bool_wrapper)
    if condition.node_type.value == 8:
        if str(condition) not in fluents:
            fluents.append(extractPreconditionAtom(condition))
        if not str(condition.type) == "bool":
            is_bool_wrapper[0] = False
            
            
def standardizeEffectRecursive(condition,fluents):
    if len(condition.args) > 1:
        standardizeEffectRecursive(condition.args[0],fluents)
        standardizeEffectRecursive(condition.args[1],fluents)
    elif len(condition.args) == 1:
        standardizeEffectRecursive(condition.args[0],fluents)
    if condition.node_type.value == 8:
        if str(condition) not in fluents:
            fluents.append(extractEffectAtom(condition))

class LiftedPrecondition:
    def __init__(self,name,args,node_id,type,node_type,ids = 0, checkLifted = False):
        self.name = name
        self.args = args
        self.node_id = node_id
        self.type = type
        self.node_type = node_type
        #TODO: change to intercept all the fluents using the objects in the tracebackmap
        if ids == 0:
            self.id = ids
        elif checkLifted:
            for name,id in ids:
                if (name.split("(")[0] + "(") in self.name:
                    self.id = id
                    break
        else:
            for name,id in ids:
                if name in self.name:
                    self.id = id
                    break

            
    def __eq__(self, value):
        return (self.id,self.node_id) == (value.id,value.node_id)
    
    def __lt__(self,value):
        return (self.id,self.node_id) < (value.id,value.node_id)
    
    def checkPrecondition(self,state):
        if self.is_bool:
            if self.atoms[0].name in state.values:
                return state.values[self.atoms[0].name]
            else:
                return False
        else:
            newVal = self.name
            for atom in self.atoms:
                newVal = newVal.replace(atom.name,str(state[atom.name].value))
            return eval(newVal)
        
 
#def removeGroundedConditions(grounded,lifted):

# Step 1: Build the similarity matrix

def build_similarity_matrix(lifted, grounded):
    matrix = np.zeros((len(lifted), len(grounded)))
    new_lifted = list()
    new_grounded = list()
    for i,j in zip(lifted,grounded):
        #new_lifted.append(str(simplify(i.name, rational = False)))
        #new_grounded.append(str(simplify(j.name, rational = False)))
        if i.node_type.value == 22:
            new_lifted.append(i.name)
        else:
            new_lifted.append(reorder(str(expand(i.name))))
        if j.node_type.value == 22:
            new_grounded.append(j.name)
        else:
            new_grounded.append(reorder_ground(str(expand(j.name))))
    for i, l in enumerate(new_lifted):
        for j, g in enumerate(new_grounded):
            matrix[i, j] = ratio(l, g)  # normalized Levenshtein similarity

    cost_matrix = -matrix  # since the assignment function minimizes cost
    # Step 3: Solve assignment problem
    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    # Step 4: Reorder grounded preconditions based on mapping
    ordered_grounded = [grounded[j] for j in col_ind]
    
    return ordered_grounded


def reorder_ground(ground):
    if "<=" in ground:
        left,right = ground.split("<=")
        if ground.count("-") > ground.count("+"):
            tmp = right + " " + left
            tmp = tmp.replace("- ","-").replace("+ ","+")
            tmp = tmp.split(" ")
            new_string = ""
            for i in tmp:
                if "(" in i:
                    if "-" in i:
                        i = i.replace("-","+ ")
                    elif "+" in i:
                        i = i.replace("+","- ")
                    new_string += i + " "
                elif i == "0":
                    new_string += " <= " + i
                else:
                    new_string += i + " "
            return new_string
                    
        else:
            return right + " >= " + left
    return ground
def reorder(lift):
    if "<=" in lift:
        left,right = lift.split("<=")
        if left.count("(") > 1:
            return right + " >= " + left
    return lift
        
def getActionFromMap(grounded,lifted, obj_encoding,ids):
    preconditions = list()
    lifted_objects = dict()
    toLoopLifted = list()
    toLoopGround = list()
    for old,new in zip(lifted[0].parameters,lifted[1]):
        lifted_objects[old.name] = new.name
    #if len(lifted[0].preconditions[0].args) != len(grounded
    if "and" in str(grounded.preconditions):
        #toLoopGround = grounded.preconditions[0].args
        #toLoopLifted = lifted[0].preconditions[0].args
        for ground,lift in zip(grounded.preconditions[0].args,lifted[0].preconditions[0].args):
            if len(lift.args) > 0:
                if str(lift.type) != "bool" or str(lift.args[0].type) == 'real'  or len(lift.args) > 1 and str(lift.args[1].type) == 'real':
                    toLoopLifted.append(LiftedPrecondition(str(lift),lift.args,lift.node_id,lift.type,lift.node_type,ids,True))
                elif str(lift.type) != "bool": 
                    toLoopLifted.append(LiftedPrecondition(str(lift),lift.args,lift.node_id,lift.type,lift.node_type,True))
            if len(ground.args) > 0:
                if str(ground.type) != "bool" or str(ground.args[0].type) == 'real' or len(ground.args) > 1 and str(ground.args[1].type) == 'real':
                    toLoopGround.append(LiftedPrecondition(str(ground),ground.args,ground.node_id,ground.type,ground.node_type,ids,False))
                #TODO: check if those elif were ment to be here or for the outside if
                elif str(ground.type) != "bool":
                    toLoopGround.append(LiftedPrecondition(str(ground),ground.args,ground.node_id,ground.type,lift.node_type,ids,False))
        #modificato utilizzando la matrice di similarità(sperando che almeno questa funzioni per ordinare le precondizioni)
        toLoopGround = build_similarity_matrix(toLoopLifted,toLoopGround)

    #TODO: modify later to handle all the cases in which some preconditions are deleted by the grounder
    elif " and" in str(lifted[0].preconditions[0]):
        return GNNAction(grounded.name,[]),[]
    else:
        if len(grounded.preconditions) > 0:
            toLoopGround.append(LiftedPrecondition(str(grounded.preconditions[0]),grounded.preconditions[0].args,grounded.preconditions[0].node_id,grounded.preconditions[0].type,grounded.preconditions[0].node_type))
            toLoopLifted.append(LiftedPrecondition(str(lifted[0].preconditions[0]),lifted[0].preconditions[0].args,lifted[0].preconditions[0].node_id,lifted[0].preconditions[0].type,lifted[0].preconditions[0].node_type))
    for groundedPrecondition, liftedPrecondition in zip(toLoopGround,toLoopLifted):
        precondition_fluents = list()
        is_bool_wrapper = [True]
    
        standardizeGnnPreconditionRecursive(liftedPrecondition,precondition_fluents,is_bool_wrapper)

        for l in precondition_fluents:
            l.changeObjectName(lifted_objects)
            l.addObjectEncoding(obj_encoding)
        preconditions.append(Precondition(groundedPrecondition.name,precondition_fluents,is_bool_wrapper[0]))
    #TODO: keep an aye on the sorting operation to ensure that every precondition is sorted correctly with respect to the lifted action
    #preconditions.sort(reverse = True)
    return GNNAction(grounded.name,preconditions),toLoopLifted

def standardizeGnnPreconditionRecursive(condition,fluents,is_bool_wrapper):
    if len(condition.args) > 1:
        standardizeGnnPreconditionRecursive(condition.args[0],fluents,is_bool_wrapper)
        standardizeGnnPreconditionRecursive(condition.args[1],fluents,is_bool_wrapper)
    elif len(condition.args) == 1:
        standardizeGnnPreconditionRecursive(condition.args[0],fluents,is_bool_wrapper)
    if condition.node_type.value == 8:
        if str(condition) not in fluents:
            fluents.append(extractPreconditionGnnAtom(condition))
        if not str(condition.type) == "bool":
            is_bool_wrapper[0] = False
            
def getEffect(effect):
    if effect.kind.value == 1:
        if str(effect.value) == "true":
            return True
        elif str(effect.value) == "false":
            return False
        else:
            return "=="
    elif effect.kind.value == 2:
        return "+"
    elif effect.kind.value == 3:
        return "-"
    else:
        return ArithmeticError("Math operator not recognized")