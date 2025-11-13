

from logicStructures.dataFormatter import  parse_domain

#function to get the number of lifted actions in the domain, to determine the output dimension of the readout function for actions readout
#TODO: check if it works correctly
def get_num_actions(data):
    data = data['domain']
    actions = data['actions_encoding']
    return len(actions)


def get_fluents_num_relations(data):
    relations = list()
    data = data['domain']
    predicates = data['predicates'].copy()
    predicates.update(data['goal_predicates'])
    functions = data['num_functions'].copy()
    functions.update(data['goal_num_functions'])
    conditions = data['goal_num_conditions'].copy()
    conditions.update(data['num_conditions'])
    conditions.update(data['num_conditions_in_goal'])
    
    for key,value in predicates.items():
        val1 = value.pop()
        val2 = value.pop()
        relations.append((key,val2,val1))
        
    for key,value in functions.items():
        val1 = value.pop()
        val2 = value.pop()
        relations.append((key,val2,val1))
        
    for key,value in conditions.items():
        val1 = value.pop()
        val2 = value.pop()
        relations.append((key,val2,val1))
        
    return relations
    
#new architecture with numeric fluents instead of numeric conditions
def get_fluents_relations(data):
    relations = list()
    data = data['domain']
    predicates = data['predicates'].copy()
    predicates.update(data['goal_predicates'])
    functions = data['num_functions'].copy()
    functions.update(data['goal_num_functions'])
    for key,value in predicates.items():
        val1 = value.pop()
        val2 = value.pop()
        relations.append((key,val2,val1))
        
    for key,value in functions.items():
        val1 = value.pop()
        val2 = value.pop()
        relations.append((key,val2,val1))
        
    return relations
    
#function for the numeric values version of the GNN
def get_num_relations(data):
    relations = list()
    data = data['domain']
    predicates = data['predicates'].copy()
    predicates.update(data['goal_predicates'])
    conditions = data['goal_num_conditions'].copy()
    conditions.update(data['num_conditions'])
    conditions.update(data['num_conditions_in_goal'])
    
    for key,value in predicates.items():
        val1 = value.pop()
        val2 = value.pop()
        relations.append((key,val2,val1))
 
        
    for key,value in conditions.items():
        val1 = value.pop()
        val2 = value.pop()
        relations.append((key,val2,val1))


    # Return the relations
    return relations

#functions for the version that evaluates numeric condition as boolean values
def get_condition_relations(data):
    """
    Extracts the relations from the dataset.
    """
    relations = list()
    cond_list = set()
    data = data['domain']
    
    predicates = data['predicates'].copy()
    predicates.update(data['goal_predicates'])
    conditions = data['goal_num_conditions'].copy()
    conditions.update(data['num_conditions'])
    conditions.update(data['num_conditions_in_goal'])
    
    for key,value in predicates.items():
        
        relations.append((key,value[0]))
        
    for key,value in conditions.items():
        if "false" not in key:
            relations.append((key,value[0]))
            cond_list.add(key)
    
    return relations,cond_list
 
 #boolean version
def get_relations(data):
    """
    Extracts the relations from the dataset.
    """
    relations = list()
    data = data['domain']
    
    predicates = data['predicates'].copy()
    predicates.update(data['goal_predicates'])
    #conditions = data['num_conditions']
    #conditions.update(data['goal_num_conditions'])
    #conditions.update(data['actions_encoding'])
   
    for key,value in predicates.items():
        
        relations.append((key,value[0]))
 
        
    #for key,value in conditions.items():
        
    #    relations.append((key,value))


    # Return the relations
    return relations

#old
def get_domain(data):
    """
    Extracts the domain from the dataset.
    """
    data = data['domain']
    
    # Parse the domain
    
    domain = parse_domain(data['domain_name'], data['actions'], data['object_types'],data['predicates'],data['goal_predicates'],data['num_predicates'])
    # Return the domain
    return domain

#old
def get_dictionaries(data):
    """
    Extracts the dictionaries from the dataset.
    """
    data = data['domain']
    
    predicates = data['predicates']
    predicates.update(data['goal_predicates'])
    num_predicates = data['num_predicates']

    # Return the dictionaries
    return predicates,num_predicates



