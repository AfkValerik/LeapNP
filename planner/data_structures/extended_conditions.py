import sympy as sp
from .conditions import checkIfNumeric, getTypeName, extractOperatorKind
import re
from data_structures.actions import getActionFromMap
from data_structures.goals import standardizeGoal
class Param:
    def __init__(self, name, type):
        self.name = name
        self.type = type
def getPredicatesAndNumericGoalsGNNExtended(problem, norm_conditions = 'left', constants = False):
    
    predicates = dict([(predicate.name,predicate.arity) for predicate in problem.fluents if str(predicate.type) == 'bool'])
    goal_predicates = dict([("goal_" + predicate.name, predicate.arity) for predicate in problem.fluents if str(predicate.type) == 'bool'])
    num_functions = dict([(predicate.name,predicate.arity) for predicate in problem.fluents if str(predicate.type) == 'real'])
    num_conditions = dict()
    goal_num_conditions = dict()
    num_conditions_in_goal = dict()
    #actual_num_conditions = dict()
 
    #add numeric conditions from the goal of the problem
    if 'and' in str(problem.goals[0]):
        goals = problem.goals[0].args
    else:
        goals = [problem.goals[0]]
    for i in goals:
        if checkIfNumeric(i):
            conditions,arities,fluents = extractNumericPrecondition(i,problem.all_objects,norm_conditions,constants)
            for condition,arity,fluent in zip(conditions,arities,fluents): 
                num_conditions_in_goal.update({condition : [arity,fluent]})
                goal_num_conditions.update({"goal_" + condition : [arity,fluent]})
    #add numeric conditions from the actions preconditions of the problem
    for i in problem.actions:
        if len(i.preconditions) > 0:
            params = i.parameters
            if ' and' in str(i.preconditions[0]):
                for j in i.preconditions[0].args:
                    if len(j.args) > 0:
                        if str(j.type) != 'bool' or str(j.args[0].type) == 'real'  or len(j.args) > 1 and str(j.args[1].type) == 'real':
                            conditions,arities,fluents = extractNumericPrecondition(j,params,norm_conditions,constants)
                            for condition,arity,fluent in zip(conditions,arities,fluents): 
                                num_conditions.update({condition : [arity,fluent]})
                                #actual_num_conditions.update({condition : [arity,fluent]})
                                #actual_num_conditions.update({"false_" + condition : [arity,fluent]})
                    elif str(j.type) != 'bool':
                        conditions,arities,fluents = extractNumericPrecondition(j,params,norm_conditions,constants)
                        for condition,arity,fluent in zip(conditions,arities,fluents): 
                            num_conditions.update({condition : [arity,fluent]})
                            #actual_num_conditions.update({condition : [arity,fluent]})
                            #actual_num_conditions.update({"false_" + condition : [arity,fluent]})
            else:
                if str(i.preconditions[0].type) != 'bool' or str(i.preconditions[0].args[0].type) == 'real' or (len(i.preconditions[0].args) > 1 and str(i.preconditions[0].args[1].type) == 'real'):
                    conditions,arities,fluents = extractNumericPrecondition(i.preconditions[0],params,norm_conditions,constants)
                    for condition,arity,fluent in zip(conditions,arities,fluents): 
                        num_conditions.update({condition : [arity,fluent]})
                        #actual_num_conditions.update({condition : [arity,fluent]})
                        #actual_num_conditions.update({"false_" + condition : [arity,fluent]})
                
    return predicates,goal_predicates,num_conditions,goal_num_conditions,num_functions,num_conditions_in_goal

def getGoalsMap(goals,objects,obj_encoding,norm_conditions = "left", constants = False):
    num_conditions_map = dict()
    goal_num_conditions_map = dict()
    
    for goal in goals:
        if checkIfNumeric(goal):
            conditions = extractNormalization(goal,objects,norm_conditions,constants)
            newGoal = standardizeGoal(goal)
            for atom in newGoal.atoms:
                atom.addObjectEncoding(obj_encoding)
            num_conditions_map.setdefault(conditions[0],[]).append(newGoal)
            goal_num_conditions_map.setdefault("goal_" + conditions[0],[]).append(newGoal)
            
    return num_conditions_map,goal_num_conditions_map

def getPredicatesMap(state,goals,obj_encoding):
    predicates = dict()
    goal_predicates = dict()
    for key,value in state.items():
        if type(value.value) is bool:
            tmp = value.convertToGoalAtom()
            tmp.addObjectEncoding(obj_encoding)
            
            predicates.setdefault(tmp.fluent,[]).append(tmp)            
            for goal in goals:
                if goal.goal_expr == tmp.name:
                    goal_predicates.setdefault("goal_" + tmp.fluent,[]).append(tmp)
    
    return predicates,goal_predicates

def getFluentsMap(state,obj_encoding):
    fluents = dict()
    for key,value in state.items():
        if type(value.value) is not bool:
            tmp = value.convertToGoalAtom()
            tmp.addObjectEncoding(obj_encoding)
            fluents.setdefault(tmp.fluent,[]).append(tmp)
    return fluents

class GoalFluent:
    def __init__(self, name, fluent, objects, goal_exprs):
        self.name = name
        self.fluent = fluent
        self.objects = objects
        self.goal_exprs = goal_exprs
        self.goal_inclusions = 1

    def addGoalInclusion(self,goal_expr):
        if goal_expr not in self.goal_exprs:
            self.goal_exprs.append(goal_expr)
            self.goal_inclusions += 1
            

def getGoalFluentsMap(fluents,goals):
    goal_fluents = dict()
    tmp_fluents = dict()
    for key,value in fluents.items():
        goal_fluents.setdefault("goal_" + key,[])
    
    for key,value in goals.items():
        for goal in value:
            for i in goal.atoms:
                    if i.name not in tmp_fluents.keys():
                        tmp_fluents[i.name] = GoalFluent(i.name,i.fluent,i.objects,[goal])
                    else:
                        tmp_fluents[i.name].addGoalInclusion(goal)
    for key,value in tmp_fluents.items():
        goal_fluents["goal_" + value.fluent].append(value)
    return goal_fluents

def getPreconditionsMap(mbai,obj_encoding,initial_state, norm_conditions = 'left', constants = False):
    ids = [(k, i) for i, (k, v) in enumerate(initial_state.items()) if not isinstance(v, bool)]
    preconditions_map = dict()
    for key,i in mbai.items():
        if len(i[0].preconditions) > 0:
            params = i[0].parameters
            #actual_action = getGroundedAction(groundedActions,key)
            actual_action,toLoopLifted = getActionFromMap(key,i, obj_encoding,ids)
            if ' and' in str(i[0].preconditions[0]):  
                #for j,k in zip(i[0].preconditions[0].args,actual_action.preconditions):
                for j,k in zip(toLoopLifted,actual_action.preconditions):
                    if len(j.args) > 0:
                        #if str(j.type) != 'bool' or str(j.args[0].type) == 'real'  or len(j.args) > 1 and str(j.args[1].type) == 'real':
                            conditions = extractNormalization(j,params,norm_conditions,constants)
                            k.orderAtoms(conditions[0])
                            preconditions_map.setdefault(conditions[0],[]).append(k)
                    #elif str(j.type) != 'bool':
                    else:
                        conditions = extractNormalization(j,params,norm_conditions,constants)
                        k.orderAtoms(conditions[0])
                        preconditions_map.setdefault(conditions[0],[]).append(k)
            
            else:
                if str(i[0].preconditions[0].type) != 'bool' or str(i[0].preconditions[0].args[0].type) == 'real' or (len(i[0].preconditions[0].args) > 1 and str(i[0].preconditions[0].args[1].type) == 'real'):
                    conditions = extractNormalization(i[0].preconditions[0],params,norm_conditions,constants)
                    actual_action.preconditions[0].orderAtoms(conditions[0])
                    preconditions_map.setdefault(conditions[0],[]).append(actual_action.preconditions[0])

    for key,value in preconditions_map.items():
        preconditions_map[key] = list(set(value))
    return preconditions_map



def extractNormalization(condition,parameters,norm_conditions,constants):
    out = ""
    param_list = list()
    cond_list = list()
    arities = list()
    fluents = list()
    const = False
    if constants != False and  (not set(constants) <= set(parameters)):
            const = True
    out = extractPreconditionRecursive(condition,out,parameters,param_list,cond_list,arities,const,constants)
    cond_list.append(out)
    arities.append(len(param_list))
    cond_list = normalize_conditions(cond_list,norm_conditions)
    
    return cond_list

def extractNumericPrecondition(condition,parameters,norm_conditions,constants):
    out = ""
    param_list = list()
    cond_list = list()
    arities = list()
    fluents = list()
    const = False
    if constants != False and  (not set(constants) <= set(parameters)):
            const = True
    out = extractPreconditionRecursive(condition,out,parameters,param_list,cond_list,arities,const,constants)
    cond_list.append(out)
    arities.append(len(param_list))
    cond_list = normalize_conditions(cond_list,norm_conditions)
    for i in cond_list:
        fluent = multiple_functions(i,parameters,param_list)
        fluents.append(fluent)
    return cond_list,arities,fluents

def extractPreconditionRecursive(condition,out,parameters,param_list,cond_list,arities,const,constants):
    if len(condition.args) > 1:
            oper = extractOperatorKind(condition.node_type)
            if oper != "fluent_exp":
                out = extractPreconditionRecursive(condition.args[0],out,parameters,param_list,cond_list,arities,const,constants)
            if oper == "or":
                cond_list.append(out)
                arities.append(len(param_list))
                out = ""
                param_list = list()
            elif oper == "fluent_exp":
                if const:
                    const_list = constants
                else:
                    const_list = const
                condition = getTypeNames(str(condition),parameters,param_list,const_list)
                out = out + str(condition)
                return out
            else:
               out = out + " " + oper + " "
            out = extractPreconditionRecursive(condition.args[1],out,parameters,param_list,cond_list,arities,const,constants)
    else:
            if "(" in str(condition) and not ("not" in str(condition)):
                condition = getTypeName(str(condition),parameters,param_list)
            elif "not" in str(condition):
                out = out + "not "
                out = extractPreconditionRecursive(condition.args[0],out,parameters,param_list,cond_list,arities,const,constants)
                return out
            out = out + str(condition)
            
    return out
    
def multiple_functions(condition,parameters,param_list):
        fluents = 0
        for i in parameters:
            if i.name in param_list:
                if " -" in str(i.type):
                    word = str(i.type).split(" -")[0]
                else:
                    word = str(i.type)
                fluents = fluents + condition.count(word) - condition.count(word + "_")
        if fluents > condition.count("("):
            fluents = condition.count("(")
        return fluents
    
    
 #take a list of conditions as input and normalize them
def normalize_conditions(cond_list,norm_conditions):
        if norm_conditions == 'left':
            new_list = list()
            tmp_replace = False
            for i in cond_list: 
                i = str(i)
                #TODO: this may create error when having conditions with both - as minus and in variable names
                if "- " not in i and " -" not in i and "-" in i:
                    i = i.replace("-","_")
                    tmp_replace = True
                equation = sp.sympify(i)
                if isinstance(equation,bool) or not hasattr(equation, 'rhs'):
                    new_equation = i
                else:
                    rhs = equation.rhs
                    lhs = equation.lhs
                    op = equation.rel_op
                
                    if op == ">":
                        lhs = - lhs
                        rhs = - rhs
                        op = "<"
                    elif op == ">=":
                        lhs = - lhs
                        rhs = - rhs
                        op = "<="
                
                    rhs = -rhs
                    rhsstring = ""
                    operators = ["+","-","*","/"]
                    tmp = ["< ","> ","<= ",">= ","== "]
                    opjoin =  '|'.join(map(re.escape, tmp))
                    
                    if " " in str(rhs) and " " in re.split(f"({opjoin})", i)[2].strip():
                        operators = ["+","-","*","/"]
                        for i in rhs.args:
                            tocheck = str(i).lstrip()
                            if tocheck[0] not in operators:
                                rhsstring = " + " + str(i) + rhsstring
                            else:
                                
                                rhsstring = " " + str(i)[0] + " " + str(i)[1:] + " " + rhsstring
                    else:
                        rhsstring = str(rhs)
                
                    new_equation = str(lhs) + " " + rhsstring + " " +  str(op) + " 0"
                    #TODO: normalizzare perchè i vecchi dataset non hanno gli spazi doppi, quelli nuovi in alcuni casi si
                    # Aggiunge spazi attorno a / solo se non ci sono già
                    if "/" in new_equation:
                        new_equation = re.sub(r'(?<!\s)([*/])(?!\s)', r' \1 ', new_equation)
                    new_equation = re.sub(r'\s{2,}', ' ', new_equation)  # Rimuove spazi doppi
                if tmp_replace:
                    new_list.append(str(new_equation).replace("-","- ").replace("_","-"))
                else:
                    new_list.append(str(new_equation).replace("-","- "))
                                        
            return new_list
        return cond_list
    
def getTypeNames(condition, parameters, param_list,const):
    tmp1 = ""
    tmp2 = ""
    for i in parameters:
        if tmp1 and tmp2:
            return condition.split("(")[0] + "(" + tmp1 + "," + tmp2 + ")"
        else: 
            if str(i.name) == condition.split("(")[1].split(",")[0].replace(" ",""):
                if not str(i.name) in param_list:
                    param_list.append(str(i.name))
                    tmp1 = i.type.name
            if str(i.name) == condition.split(",")[1].split(")")[0].replace(" ",""):
                if not str(i.name) in param_list:
                    param_list.append(str(i.name))
                    tmp2 = i.type.name
    if const != False:
        for i in const:
            if tmp1 and tmp2:
                return condition.split("(")[0] + "(" + tmp1 + "," + tmp2 + ")"
            else:
                if str(i.name) == condition.split("(")[1].split(",")[0].replace(" ",""):
                    if not str(i.name) in param_list:
                        param_list.append(str(i.name))
                        tmp1 = i.name
                if str(i.name) == condition.split(",")[1].split(")")[0].replace(" ",""):
                    if not str(i.name) in param_list:
                        param_list.append(str(i.name))
                        tmp2 = i.name
    return condition.split("(")[0] + "(" + tmp1 + "," + tmp2 + ")"