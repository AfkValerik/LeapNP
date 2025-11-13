from fractions import Fraction

def encode_objects(objects):
    obj_encoding = dict()
    i = 0
    for object in objects:
        obj_encoding.update({object.name : i})
        i = i+1
    return obj_encoding


def encode_goals(state, goal_predicates, goal_num_conditions,objects,obj_encoding,num_functions,goals,constants):
    encoded_state = encode_goal_state(state,goal_predicates,obj_encoding,goals)
    for key,value in goal_num_conditions.items():
        encoded_state = extract_goal_condition_object_pairs(state,key,objects,obj_encoding,num_functions,encoded_state,value,goals,constants)
    
    return encoded_state

def extract_goal_condition_object_pairs(state,condition,objects,obj_encoding,num_functions,encoded_state,arity,goals,constants = False):
    tmp,objlist = reconstruct_condition(state,condition,objects,num_functions,arity,constants, goal = True)
    obj1 = objlist[0]
    if len (objlist) > 1:
        obj2 = objlist[1]
    else:
        obj2 = list()
    object_list = list()
    if len(obj2) > 0:
        for i in obj1:
            for j in obj2:
                if object_in_goal_condition(str(i),tmp,goals,str(j)):
                    object_list.append([i.args[0],j.args[0]])
    elif len(obj1) > 0:
        for i in obj1:
            if object_in_goal_condition(str(i),tmp,goals):
                object_list.append(i.args[0])
        
    encoded_state.update({condition : get_object_ids(object_list,obj_encoding)})
        
    return encoded_state 

#encode the state in a dictionary of predicate-object pairs
def encode_goal_state(goal_predicates):
    encoded_state = dict()
    for key,value in goal_predicates.items():
        encoded_state.update({key: extract_predicate_object_pair(value)})        
    return encoded_state

def extract_numeric_goals(key,values,encoded_state):
    encoded_state.setdefault("goal_" + key,[])
    for value in values:
        obj_list = list()
   
        for atom in value.atoms:
            for obj in atom.objects:
                if obj.encoding_id not in obj_list:
                    obj_list.append(obj.encoding_id)
                    encoded_state["goal_" + key].append(obj.encoding_id)
    return encoded_state

def extract_numeric_goals_in_state(state,key,values,encoded_state):
    encoded_state.setdefault(key,[])
    for value in values:
        obj_list = list()
        if value.checkGoal(state):
                for atom in value.atoms:
                    for obj in atom.objects:
                        if obj.encoding_id not in obj_list:
                            obj_list.append(obj.encoding_id)
                            encoded_state[key].append(obj.encoding_id)
     
    return encoded_state

def extract_conditions(state,key,values,encoded_state):
    encoded_state.setdefault(key,[])
    for value in values:
        obj_list = list()
        if value.checkPrecondition(state):
                for atom in value.atoms:
                    for obj in atom.objects:
                        if obj.encoding_id not in obj_list:
                            obj_list.append(obj.encoding_id)
                            encoded_state[key].append(obj.encoding_id)
    return encoded_state
    
#encode a state in a dictionary of predicate-object and numeric_condition-object pairs
def encode_gnn_state(state, predicates,objects, obj_encoding,num_conditions,num_functions,num_conditions_in_goal,constants):
    encoded_state = dict()
    encoded_state = encode_state(state,predicates,obj_encoding,encoded_state)
    for key,value in num_conditions.items():
        encoded_state = extract_condition_object_pairs(state,key,objects,obj_encoding,num_functions,encoded_state,value,constants)
    for key,value in num_conditions_in_goal.items():
        encoded_state = extract_condition_object_pairs(state,key,objects,obj_encoding,num_functions,encoded_state,value,constants)
    
    return encoded_state

    #extract the value of the action taken to reach the state, probably unused in the new code
def encode_action(action,obj_encoding,encoded_state,actions):
    objs = list()
    if action is not None:
        for i in actions:
            if i.name  in action.action_expr.name and ((len(i.name.split("_")) + len(i.parameters)) == len(action.action_expr.name.split("_"))) :
                if len(i.parameters) > 0:
                    tmp = action.action_expr.name.rsplit("_")
                    for j in range(0,len(i.parameters)):
                        objs.insert(0,tmp.pop())
                    objs = get_object_ids(objs,obj_encoding)
                    if len(objs) > 1:
                        encoded_state.update({i.name: [objs]})
                    else:
                        encoded_state.update({i.name: objs})
                else:
                    encoded_state.update({i.name: []})
            else:
                encoded_state.update({i.name: []})
    else:
        for i in actions:
            encoded_state.update({i.name: []}) 

    return encoded_state



def goals_contains_atom(atom,predicate,goals):
        for goal in goals:
            if predicate.replace("goal_", "") in goal and str(atom) in goal: 
                return True
        return False      

            #extract the number assign to the object, given the name of the object
def get_object_encoding_from_name(object,obj_encoding,value = 1):
        object = str(object).split("(")[1].replace(")","")
        if value == 1:
            out = obj_encoding.get(object)
        elif value == 2:
            objects = object.replace(" ","").split(",")
            out = list()
            out.append(obj_encoding.get(objects[0]))
            out.append(obj_encoding.get(objects[1]))
        return out
    
def object_in_goal_condition(obj1,condition,goals,obj2 = False):
    phrase = " ".join(condition)
    tmp = phrase.replace("obj1",str(obj1))
    
    if obj2 != False:
        tmp = tmp.replace("obj2",str(obj2))
    
    tmp = "".join(char for char in tmp if char not in "()")
    for i in range(len(goals)):
        check = "".join(char for char in str(goals[i]) if char not in "()")
        if tmp in check:
            if "not" not in check:
                return True
            elif "not" in tmp:
                return True
        
    return False
        

def extract_condition_object_pairs(state,condition,objects,obj_encoding,num_functions,encoded_state, arity, constants = False):
        tmp,objout = reconstruct_condition(state,condition,objects,num_functions,arity,constants)
        object_list = list()
        if len(objout) == 2:
            for i in objout[0]:
                for j in objout[1]:
                    if arity[0] == 2 and str(i) != str(j):   
                        if valuate_condition(objout[0].get(i),tmp,objout[1].get(j)):
                            object_list.append([i.args[0],j.args[0]])
                    elif arity[0] == 1 and arity[1] == 2 and str(i.args[0]) == str(j.args[0]):
                        if valuate_condition(objout[0].get(i),tmp,objout[1].get(j)):
                            object_list.append([i.args[0]])                          
        elif len(objout) > 0:
            for i in objout[0]:
                if valuate_condition(objout[0].get(i),tmp):
                    if arity[0] == 2 and arity[1] == 1:
                        object_list.append([i.args[0],i.args[1]])
                    else:
                        object_list.append(i.args[0])
                    
        encoded_state.update({condition : get_object_ids(object_list,obj_encoding)})
        return encoded_state

def get_object_ids(object_list,obj_encoding):
    if object_list:
        if isinstance(object_list[0],list):
            for indexi,itemi in enumerate(object_list):
                for indexj,itemj in enumerate(itemi):
                    object_list[indexi][indexj] = obj_encoding.get(str(itemj))
        else:
            for index,item in enumerate(object_list):
                object_list[index] = obj_encoding.get(str(item))
            
    return object_list

#valuate numeric conditions
def valuate_condition(obj1,condition, obj2 = False):

    phrase = " ".join(condition)
    tmp = phrase.replace("obj1",str(obj1))
    
    if obj2 != False:
        #if str(obj1) == str(obj2):
        #    return False
        tmp = tmp.replace("obj2",str(obj2))
        
    if eval(tmp):
        return True
    else:
        return False

def extract_object_pairs(state,condition,objects,constants):
        object_dict = dict()

        const = ""
        for i in constants:
            if i.name in condition.split("(")[1]:
                const = i.name
                break
        condition = condition.replace(",",", ")
        for atom_key, atom_value in state.items():
            if str(atom_key).split("(")[0] == condition.split("(")[0]:
                if "(" in str(atom_key) and const in str(atom_key):
                    check1,check2 = checkPairObjectType(str(atom_key),objects,const)
                    if check1 in condition and check2 in condition:
                        object_dict.update({atom_key : atom_value})
        return object_dict 

def checkPairObjectType(state_item,objects,const):
        tmp1 = ""
        tmp2 = ""
        for i in objects:
            if tmp1 != "" and tmp2 != "":
                if const != "":
                    tmp1 = const
                return tmp1,tmp2
            else:
                if str(i.name) == state_item.split("(")[1].split(",")[0].split(")")[0]:
                    tmp1 = i.type.name
                if str(i.name) == state_item.split(",")[1].split(")")[0].replace(" ",""):
                    tmp2 = i.type.name
        if const != "":
            tmp1 = const
        return tmp1,tmp2
    
def reconstruct_binary_fluent(state,condition,objects,constants):
        objectsout = [[]]
        func = list()
        toReconstruct = condition.split(" ")
        for i in toReconstruct:
            if "(" in i:
                 objectsout[0] = extract_object_pairs(state,i,objects,constants)
                 func.append("obj1")
            else:
                func.append(i)
        return objectsout,func
    
def reconstruct_condition(state,condition,objects,num_functions,arity,constants,goal = False):
        if goal == True:
            condition = condition.replace("goal_","")
        if arity[0] == 2 and arity[1] == 1:
            condition = condition.replace(", ",",")
            objectsout,func = reconstruct_binary_fluent(state,condition,objects,constants)
            return func,objectsout
        toReconstruct = condition.split(" ")
        objectsout = [[]]
        func = list()
        for i in toReconstruct:
            if i.split("(")[0] in num_functions:
                #if it contains an object we must evaluate with all the possible object combinations
                if "(" in i:
                    if len(objectsout[0]) == 0:
                        objectsout[0] = extract_satisficing_object(state,i,objects)
                        func.append("obj1")
                    elif len(objectsout) == 1:
                        if  arity[0] > 1 or arity[1] > 1:
                            objectsout.append(extract_satisficing_object(state,i,objects))
                            func.append("obj2")
                        else:
                            func.append("obj1")
                    elif len(objectsout) == 2 and arity[1] > 2:
                        objectsout.append(extract_satisficing_object(state,i,objects))
                        func.append("obj3")
                else:
                    func.append(str(extract_function(state,i)))
            else:
                func.append(i)
        return func,objectsout


#extract value of functions without objects
def extract_function(state,condition):
    for atom_key, atom_value in state.items():
        if condition in str(atom_key):
            return atom_value
    return False
        
#extract the objects in the state that are related to the predicate
def extract_satisficing_object(state,condition,objects):
        object_dict = dict()
        for atom_key, atom_value in state.items():
            if str(atom_key).split("(")[0] == condition.split("(")[0]:
            #if removeNumbers(str(atom_key)) in condition:
                if "(" in str(atom_key):
                    if checkObjectType(str(atom_key),objects) in condition:
                        object_dict.update({atom_key : atom_value})
        return object_dict 
       
#encode the state in a dictionary of predicate-object pairs
def encode_state(state,predicates,encoded_state):
    for key,values in predicates.items():
            encoded_state.setdefault(key,[])
            for value in values:
                if state[value.name]:
                    for obj in value.objects:
                        encoded_state[key].append(obj.encoding_id)
        
    return encoded_state

def extract_condition_object_pair(state,condition,obj_encoding,encoded_state,value):
        condition_list = list()
        if value > 0:
            for atom_key, atom_value in state.items():
                if atom_contains_predicate(atom_key,condition) and atom_value:
                    condition_list.append(get_object_encoding_from_name(atom_key,obj_encoding,value))
                    
        encoded_state.update({condition : condition_list})
        return encoded_state
    
def extract_predicate_object_pair(value):
        predicate_list = list()
        for atom in value:
            for i in atom.objects:
                predicate_list.append(i.encoding_id)
        return predicate_list

#extract the objects in the state that are related to the predicate, for numeric predicate
def extract_predicate_object_pair_numeric(state,predicate,obj_encoding):
    predicate_list = list()

    for atom_key, atom_value in state.items():
            if atom_contains_predicate(atom_key,predicate):
                predicate_list.append(get_object_encoding_from_name(atom_key,obj_encoding))
                predicate_list.append(valueConverter(str(atom_value)))
        
    return predicate_list


#check if the atom contains the predicate name in the string
def atom_contains_predicate(atom,predicate):
    predicate = predicate.split("_")[-1]
    if (str(predicate) + "(") in str(atom):
        return True
    else :
        return False

#extract the number assign to the object, given the name of the object
#def get_object_encoding_from_name(object,obj_encoding):
#    object = str(object).split("(")[1].replace(")","")
#    out = obj_encoding.get(object)
#    return out


def valueConverter(i):
    if i == 'true':
            out = True
    elif i == 'false':
            out = False
    else:
        if i.isnumeric():
                if is_integer(i):
                    out = int(i)
                else:
                    out = float(i)
        else:
            out = float(Fraction(i))
            
    return out

def checkObjectType(state_item,objects):
    for i in objects:
        if str(i.name) == state_item.split("(")[1].split(")")[0]:
            return i.type.name
    return ValueError("Object not found")

def is_integer(s):
    return s.isdigit()
