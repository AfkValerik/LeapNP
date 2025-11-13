import sympy as sp


def getPredicatesAndNumericGoalsGNN(problem, norm_conditions = 'left'):
    
    predicates = dict([(predicate.name,predicate.arity) for predicate in problem.fluents if str(predicate.type) == 'bool'])
    goal_predicates = dict([("goal_" + predicate.name, predicate.arity) for predicate in problem.fluents if str(predicate.type) == 'bool'])
    num_functions = dict([(predicate.name,predicate.arity) for predicate in problem.fluents if str(predicate.type) == 'real'])
    num_conditions = dict()
    goal_num_conditions = dict()
 
    #add numeric conditions from the goal of the problem
    if 'and' in str(problem.goals[0]):
        goals = problem.goals[0].args
    else:
        goals = [problem.goals[0]]
    for i in goals:
        if checkIfNumeric(i):
            conditions,arities = extractNumericPrecondition(i,problem.all_objects,norm_conditions)
            for condition,arity in zip(conditions,arities): 
                num_conditions.update({condition : arity})
                goal_num_conditions.update({"goal_" + condition : arity})
    #add numeric conditions from the actions preconditions of the problem
    for i in problem.actions:
        if len(i.preconditions) > 0:
            params = i.parameters
            if 'and' in str(i.preconditions[0]):
                for j in i.preconditions[0].args:
                    if len(j.args) > 0:
                        if str(j.type) != 'bool' or str(j.args[0].type) == 'real':
                            conditions,arities = extractNumericPrecondition(j,params,norm_conditions)
                            for condition,arity in zip(conditions,arities): 
                                num_conditions.update({condition : arity})
                    elif str(i.type) != 'bool':
                        conditions,arities = extractNumericPrecondition(j,params,norm_conditions)
                        for condition,arity in zip(conditions,arities): 
                            num_conditions.update({condition : arity})
            else:
                if str(i.preconditions[0].type) != 'bool' or str(i.preconditions[0].args[0].type) == 'real' or str(i.preconditions[0].args[1].type) == 'real':
                    conditions,arities = extractNumericPrecondition(i.preconditions[0],params,norm_conditions)
                    for condition,arity in zip(conditions,arities): 
                        num_conditions.update({condition : arity})
                
    return predicates,goal_predicates,num_conditions,goal_num_conditions,num_functions

def getPredicatesGNN(problem):
    predicates = dict([(predicate.name,predicate.arity) for predicate in problem.fluents if str(predicate.type) == 'bool'])
    goal_predicates = dict([("goal_" + predicate.name, predicate.arity) for predicate in problem.fluents if str(predicate.type) == 'bool'])
    return predicates,goal_predicates


def checkIfNumeric(condition):
    if str(condition.type) == "real":
        return True
    elif len(condition.args) > 0:
        for i in condition.args:
            if checkIfNumeric(i):
                return True 
    return False


def extractPreconditionRecursive(condition,out,parameters,param_list,cond_list,arities):

    if len(condition.args) > 1:
        out = extractPreconditionRecursive(condition.args[0],out,parameters,param_list,cond_list,arities)
        oper = extractOperatorKind(condition.node_type)
        if oper == "or":
            cond_list.append(out)
            arities.append(len(param_list))
            out = ""
            param_list = list()
        else:
            out = out + " " + oper + " "
        out = extractPreconditionRecursive(condition.args[1],out,parameters,param_list,cond_list,arities)
    else:
        if "(" in str(condition) and not ("not" in str(condition)):
           condition = getTypeName(str(condition),parameters,param_list)
        elif "not" in str(condition):
            out = out + "not "
            out = extractPreconditionRecursive(condition.args[0],out,parameters,param_list,cond_list,arities)
            return out
        out = out + str(condition)
        
    return out
          
def extractNumericPrecondition(condition,parameters,norm_conditions):
    out = ""
    param_list = list()
    cond_list = list()
    arities = list()
    out = extractPreconditionRecursive(condition,out,parameters,param_list,cond_list,arities)
    cond_list.append(out)
    arities.append(len(param_list))
    cond_list = normalize_conditions(cond_list,norm_conditions)
    return cond_list,arities

#take a list of conditions as input and normalize them
def normalize_conditions(cond_list,norm_conditions):
        if norm_conditions == 'left':
            new_list = list()
            for i in cond_list:
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
                    if " " in str(rhs):
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

                new_list.append(str(new_equation).replace("-","- "))
            return new_list
        return cond_list



def getTypeName(condition,parameters,param_list):
    for i in parameters:
        if str(i.name) == condition.split("(")[1].split(")")[0]:
            if not str(i.name) in param_list:
                param_list.append(str(i.name)) 
            return condition.split("(")[0] + "(" + i.type.name + ")"
    return condition


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
    elif type.value == 21:
        return "<"
    elif type.value == 15:
        return "real"
    elif type.value == 8:
        return "fluent_exp"
    elif type.value == 18:
        return "*"
    else:
        ValueError("Operator not supported")
        

