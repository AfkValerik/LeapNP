from fractions import Fraction
from .encoded_state import object_in_goal_condition, checkObjectType
import torch
#def encode_goals(state,objects,obj_encoding,goals,goal_num_conditions):
#    encoded_state = encode_goal_state(state,objects,obj_encoding,goals)
#    for key,value in goal_num_conditions.items():
#        encoded_state,condition_state = extract_goal_condition_object_pairs(state,key,objects,obj_encoding,encoded_state,condition_state,goals, arity = value)
#            
#    return encoded_state,condition_state


    
def extract_num_values(state,condition,obj_encoding,encoded_state,arity):
        object_list = list()
        state_values = list()
        values = list()
        if arity == 0:
            return encoded_state
        elif arity == 1:
            for i in state:
                tmp1 = len(str(i).split(("_")))
                tmp2 = len(condition.split(("_")))
                if tmp1 == tmp2 and condition in str(i) and  "(" in str(i):
                    object_list.append([str(i).split("(")[1].split(")")[0]])
                    state_values.append(state.get(i))
            
            obj_to_encode = get_object_ids(object_list,obj_encoding)
            
            for i,j in zip(state_values,obj_to_encode):
                values.append([j,int(str(i))])
                
        encoded_state.update({condition : values})
        return encoded_state

def extract_condition_object_pairs(state,key,values,encoded_state):
    encoded_state.setdefault(key,[[],[]])
    encoded_state.setdefault("false_" + key,[[],[]])
    for value in values:
        obj_list = list()
        if value.checkPrecondition(state):
                for atom in value.atoms:
                    encoded_state[key][1].append(state[atom.name])
                    for obj in atom.objects:
                        if obj.encoding_id not in obj_list:
                            obj_list.append(obj.encoding_id)
                            encoded_state[key][0].append(obj.encoding_id)
        else:
            for atom in value.atoms:
                encoded_state["false_" + key][1].append(state[atom.name])
                for obj in atom.objects:
                    if obj.encoding_id not in obj_list:
                        obj_list.append(obj.encoding_id)
                        encoded_state["false_" + key][0].append(obj.encoding_id)

            
    return encoded_state

def extract_goal_condition_object_pairs(state,key,values,encoded_state):
    encoded_state.setdefault(key,[[],[]])
    encoded_state.setdefault("goal_" + key,[[],[]])
    for value in values:
        obj_list = list()
        if value.checkGoal(state):
                for atom in value.atoms:
                    encoded_state[key][1].append(state[atom.name])
                    encoded_state["goal_" + key][1].append(state[atom.name])
                    for obj in atom.objects:
                        if obj.encoding_id not in obj_list:
                            obj_list.append(obj.encoding_id)
                            encoded_state[key][0].append(obj.encoding_id)
                            encoded_state["goal_" + key][0].append(obj.encoding_id)
        else:
            for atom in value.atoms:
                encoded_state["goal_" + key][1].append(state[atom.name])
                for obj in atom.objects:
                    if obj.encoding_id not in obj_list:
                        obj_list.append(obj.encoding_id)
                        encoded_state["goal_" + key][0].append(obj.encoding_id)

            
    return encoded_state

def extract_numeric_fluents(state,key,values,encoded_state):
    encoded_state.setdefault(key,[[],[]])
    for value in values:
        obj_list = list()
        encoded_state[key][1].append(state[value.name])
        for obj in value.objects:
            if obj.encoding_id not in obj_list:
                obj_list.append(obj.encoding_id)
                encoded_state[key][0].append(obj.encoding_id)
        
    return encoded_state

def extract_numeric_goals_fluents(state,key,values,encoded_state):
    encoded_state.setdefault(key,[[],[]])
    for value in values:
        obj_list = list()
        encoded_state[key][1].append(value.goal_inclusions)
        for obj in value.objects:
            if obj.encoding_id not in obj_list:
                obj_list.append(obj.encoding_id)
                encoded_state[key][0].append(obj.encoding_id)
        solved = 0
        for goal in value.goal_exprs:
            if goal.checkGoal(state):
                solved += 1
        encoded_state[key][1].append(solved)
    return encoded_state
def valuate_condition_bool(obj1,condition, obj2 = False, obj3 = False):

        phrase = " ".join(condition)
        tmp = phrase.replace("obj1",str(obj1))
        
        if obj2 != False:
            #if str(obj1) == str(obj2):
            #    return False
            tmp = tmp.replace("obj2",str(obj2))
            
        if obj3 != False:
            #if str(obj1) == str(obj2):
            #    return False
            tmp = tmp.replace("obj3",str(obj3))
            
        if eval(tmp):
            return True
        else:
            return False
        
        
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
    
#extract value of functions without objects
def extract_function(state,condition):
        for atom_key, atom_value in state.items():
            if condition in str(atom_key):
                return atom_value
        return False
    
    
    
def get_encoded_states_with_values(state,encoding):

        encoded_state = dict()
        num_values = dict()
        for key,values in state.items():
           
                encoded_state.update({key: values[0]})
                encoded_state.update({key: torch.tensor(flatten_list(values[0]))})
                num_values.update({encoding[key]: values[1]})
                num_values.update({encoding[key]: torch.tensor(flatten_list(values[1]))})


        new_tuple = tuple((encoded_state,num_values))
    
        
        return new_tuple


def flatten_list(nested_list):
    flattened_list = []
    if not isinstance(nested_list, list):
        nested_list = [nested_list]
    for element in nested_list:
        if isinstance(element, list):
            flattened_list.extend(flatten_list(element))
        else:
            flattened_list.append(element)
    return flattened_list


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