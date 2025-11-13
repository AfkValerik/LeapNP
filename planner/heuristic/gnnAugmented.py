
import torch
from typing import Dict, List, Tuple
from torch.functional import Tensor
from heuristic.NNheuristic import NNHeuristic


from data_structures import encode_state,encode_goal_state, extract_goal_condition_object_pairs, extract_condition_object_pairs, get_encoded_states_with_values, extract_augmented_goals_pairs
from architecture import g_model_classes

class GnnAugmented(NNHeuristic):
    def __init__(self, model, predicates, goal_predicates, objects, obj_encoding, num_conditions, goal_num_conditions,num_conditions_in_goal,augmented_goals,encoding,goals,goal_encoding,constants):
        self.model = model
        self.predicates = predicates
        self.goal_predicates = goal_predicates
        self.objects = objects
        self.obj_encoding = obj_encoding
        self.num_conditions = num_conditions
        self.goal_num_conditions = goal_num_conditions
        self.num_conditions_in_goal = num_conditions_in_goal
        self.goals = goals
        self.goal_encoding = goal_encoding
        self.augmented_goals = augmented_goals
        #encoding = predicates|goal_predicates|goal_num_conditions|num_conditions|actual_num_conditions|num_conditions_in_goal
        #self.encoding = dict([(predicate, index) for index, predicate in enumerate(encoding.keys())])
        self.encoding = encoding
        self.constants = constants
        
    def __valuateState__(self,state, parent = None):
        encoded_tensors =  list(dict())
        encoded_state,bool_encoded_state = self.__encode_gnn_state__(state.values)
            
        encoded_state = get_encoded_states_with_values(encoded_state,self.encoding)
        for key,value in bool_encoded_state.items():
            encoded_state[0].update({key: torch.tensor(flatten_list(value))})
            encoded_state[1].update({self.encoding[key]: torch.tensor([])})
        encoded_tensors.append(encoded_state)
        with torch.no_grad():
            input = collate(encoded_tensors,self.model.device)
        h = self.model(input)
        state.h = h.item()
        
        
    def __valuateStates__(self,states, parent = None):
        encoded_tensors =  list(dict())
        
        for state in states:
            encoded_state,bool_encoded_state = self.__encode_gnn_state__(state.values)
            
            #for key,value in encoded_state.items():
            #    encoded_tensor.update({key: torch.tensor(flatten_list(value))})
            encoded_state = get_encoded_states_with_values(encoded_state,self.encoding)
            for key,value in bool_encoded_state.items():
                encoded_state[0].update({key: torch.tensor(flatten_list(value))})
                encoded_state[1].update({self.encoding[key]: torch.tensor([])})
            encoded_tensors.append(encoded_state)
        #encoded_tensors = get_encoded_states_with_values(encoded_tensors,self.encoding)

        input = collate(encoded_tensors,self.model.device)
        with torch.no_grad():
            h = self.model(input)

        
        for state,h1 in zip(states,h):
            state.h = h1.item()
            
    def __generalPolicy__(self,states, parent = None):
        self.__valuateStates__(states)
        min = states.pop(-1)
        for state in states:
            if state.h < min.h:
               min = state                    
        return min
    
    def __encode_gnn_state__(self,state):
        encoded_state = dict()
        bool_encoded_state =  self.goal_encoding.copy()
        bool_encoded_state = encode_state(state,self.predicates,bool_encoded_state)
        
        #fluents_state = dict()
        #condition_state = dict()
        
        for key,value in self.goal_num_conditions.items():
            encoded_state = extract_goal_condition_object_pairs(state,key,value,encoded_state)
        #for key,value in self.num_functions.items():
           #encoded_state = extract_num_values(state,key,self.obj_encoding,encoded_state, arity = value)
        for key,value in self.num_conditions.items():
            encoded_state = extract_condition_object_pairs(state,key,value,encoded_state)
        
        for key,value in self.augmented_goals.items():
            encoded_state = extract_augmented_goals_pairs(state,key,value,encoded_state)
        #encoded_state = encoded_state|condition_state
        return encoded_state,bool_encoded_state

        

def gnnHeuristic(path,predicates,goal_predicates,objects,obj_encoding,num_conditions,goal_num_conditions,num_conditions_in_goal,augmented_goals_map,goals,aggregation,readout,gpus,state,constants):
    Model = __load_model__(aggregation, readout)
    if gpus > 0 and torch.cuda.is_available():
        device = torch.device('cuda')
        print("running with GPU")
    else: 
        device = torch.device('cpu')
        print("running with CPU")
    model = Model.load_from_checkpoint(checkpoint_path=str(path), strict=False).to(device)
    goal_encoding = encode_goal_state(goal_predicates)
    num_conditions = {k: v for k, v in num_conditions.items() if k not in goal_num_conditions}
            
    return GnnAugmented(model, predicates, goal_predicates, objects, obj_encoding, num_conditions, goal_num_conditions,num_conditions_in_goal,augmented_goals_map,model.encoding,goals,goal_encoding,constants)


def __load_model__(aggregation,readout):
    try:
        Model = g_model_classes[(aggregation, readout, 'supervised_optimal',True,True)]
    except KeyError:
        raise NotImplementedError(f"No model found for {(aggregation, readout, 'supervised_optimal',True,True)} combination")
    return Model


def flatten_list(nested_list):
    flattened_list = []
    for element in nested_list:
        if isinstance(element, list):
            flattened_list.extend(flatten_list(element))
        else:
            flattened_list.append(element)
    return flattened_list

def collate(batch: List[Tuple[Dict[int, Tensor],Dict[int, Tensor]]], device):
    """
    Input: [state]
    Output: (states, sizes, inits)
    """
    input = {}
    sizes = []
    inits = {}
    offset = 0
    for state,init in batch:
        max_size = 0
        for predicate, values in state.items():
            if values.nelement() > 0:
                max_size = max(max_size, int(torch.max(values)) + 1)
            if predicate not in input: input[predicate] = []
            input[predicate].append(values + offset)
        for key,values in init.items():
            if key not in inits: inits[key] = []
            inits[key].append(values)
        sizes.append(max_size)
        offset += max_size
    for predicate in input.keys():
        input[predicate] = torch.cat(input[predicate]).view(-1).to(device=device, non_blocking=True)
    for key in inits.keys():
        inits[key] = torch.cat(inits[key]).view(-1).to(device=device, non_blocking=True)
    return (input, sizes,inits)


    