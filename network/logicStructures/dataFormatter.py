class Domain:
    def __init__(self, domain_name, actions, object_types, predicates, goal_predicates, num_predicates):
        self.name = domain_name
        self.actions = actions
        self.types = object_types
        self.predicates = predicates
        self.goal_predicates = goal_predicates
        self.num_predicates = num_predicates
        
        
class Instance:
    def __init__(self, instance_name, grounded_actions, objects,goals, possible_states,values):
        self.name = instance_name
        self.grounded_actions = grounded_actions
        self.objects = objects
        self.goals = goals
        self.states = possible_states
        self.values = values
       
class Action:
    def __init__(self, name, parameters, preconditions, effects):
        self.name = name
        self.parameters = parameters
        self.preconditions = preconditions
        self.effects = effects 
        
class State:
    def __init__(self, fluents, value):
        self.fluents = fluents
        self.value = value
       
class EncodedStates:
    def __init__(self, states, predicates,num_predicates,goal_predicates, obj_encoding):
        self.states = states
        self.encoded_states = encode_states(states,predicates,num_predicates,goal_predicates,obj_encoding)


#create an encoding for the objects in the instance
def encode_objects(objects):
    obj_encoding = dict()
    i = 0
    for object in objects:
        obj_encoding.update({object['object'] : i})
        i = i+1
    return obj_encoding

def encode_states(states, predicates,num_predicates,goal_predicates, obj_encoding):
    encoded_states = list()
    for state in states:
        encoded_states.append(encode_state(state,predicates,num_predicates,goal_predicates,obj_encoding))
        
    return encoded_states

#encode the state in a dictionary of predicate-object pairs
def encode_state(state,predicates,num_predicates,goal_predicates,obj_encoding):
    encoded_state = dict()
    #TODO: try with a domain that has a boolean predicate with two objects
    for key,value in predicates.items():
        if value == 2:
            encoded_state.update({key: extract_predicate_object_pair(state,key,obj_encoding)})
    #TODO: try with a domain that has a boolean predicate with two objects
    for key,value in goal_predicates.items():
        if value == 1:
            encoded_state.update({key: extract_predicate_object_pair(state,key,obj_encoding)})
        elif value == 2:
            encoded_state.update({key: extract_predicate_object_pair(state,key,obj_encoding)})
    for key,value in num_predicates.items():
        if value == 2:
            encoded_state.update({key: extract_predicate_object_pair_numeric(state,key,obj_encoding)})
    
    return encoded_state

#extract the objects in the state that are related to the predicate
def extract_predicate_object_pair(state,predicate,obj_encoding):
    
    state, state_value = state.items()
    predicate_list = list()
    for atom in state[1]:
        for atom_key, atom_value in atom.items():
            if atom_contains_predicate(atom_key,predicate):
                predicate_list.append(get_object_encoding_from_name(atom_key,obj_encoding))
    return predicate_list
#extract the objects in the state that are related to the predicate, for numeric predicate
def extract_predicate_object_pair_numeric(state,predicate,obj_encoding):
    
    state, state_value = state.items()
    predicate_list = list()
    for atom in state[1]:
        for atom_key, atom_value in atom.items():
            if atom_contains_predicate(atom_key,predicate):
                predicate_list.append(get_object_encoding_from_name(atom_key,obj_encoding))
                predicate_list.append(atom_value)
        
    return predicate_list

#check if the atom contains the predicate name in the string
def atom_contains_predicate(atom,predicate):
    predicate = predicate.split("_")[-1]
    if (str(predicate) + "(") in str(atom):
        return True
    else :
        return False

#extract the number assign to the object, given the name of the object
def get_object_encoding_from_name(object,obj_encoding):
    object = object.split("(")[1].replace(")","")
    out = obj_encoding.get(object)
    return out
    

def get_encoded_states(state, predicates,num_predicates,goal_predicates, obj_encoding):
    return EncodedStates(state, predicates,num_predicates,goal_predicates, obj_encoding)
        
def parse_action(action_name, parameters, preconditions, effects):
    return Action(action_name, parameters, preconditions, effects)

def parse_domain(domain_name, actions, object_types, predicates, goal_predicates,num_predicates):
    return Domain(domain_name, actions, object_types, predicates, goal_predicates,num_predicates)

def parse_instance(instance_name, grounded_actions, objects,goals, possible_states,values):
    return Instance(instance_name, grounded_actions, objects,goals, possible_states,values)
 
def parse_state(fluents, value):
    return State(fluents, value) 
