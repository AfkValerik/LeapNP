
import torch
from typing import Dict, List
from torch.functional import Tensor
from heuristic.NNheuristic import NNHeuristic


from data_structures import encode_gnn_state, encode_goal_state, extract_numeric_goals, extract_conditions, encode_state, extract_augmented_goals_objects, extract_numeric_goals_in_state
from architecture import g_model_classes

class GnnCondAugmented(NNHeuristic):
    def __init__(self, model, predicates, goal_predicates, objects, obj_encoding, num_conditions, goal_num_conditions,num_conditions_in_goal,augmented_goals,encoding,goals,goal_encoding,constants):
        self.model = model
        self.predicates = predicates
        self.goal_predicates = goal_predicates
        self.objects = objects
        self.obj_encoding = obj_encoding
        self.num_conditions = num_conditions
        self.goal_num_conditions = goal_num_conditions
        self.num_conditions_in_goal = num_conditions_in_goal
        self.augmented_goals = augmented_goals
        self.goals = goals
        self.goal_encoding = goal_encoding
        self.encoding = encoding
        self.constants = constants
    
    def __valuateState__(self,state, parent = None):

        encoded_state = encode_gnn_state(state.values,self.predicates,self.objects,self.obj_encoding,self.num_conditions,self.num_functions)
        encoded_tensor = self.goals.copy()
        for key,value in encoded_state.items():
            encoded_tensor.update({key: torch.tensor(flatten_list(value))})
        input = collate([encoded_tensor],self.model.device)

        with torch.no_grad():
            h = self.model(input)
        state.h = h.item()
        
        
    def __valuateStates__(self,states, parent = None):
        encoded_tensors =  list(dict())
        for state in states:
            encoded_state = dict()
            encoded_tensor = dict()
            bool_encoded_state = self.goal_encoding.copy()
            bool_encoded_state = encode_state(state.values,self.predicates,bool_encoded_state)
            for key,value in self.num_conditions_in_goal.items():
                encoded_tensor.update({key: torch.tensor(flatten_list(value))})
            for key,value in self.num_conditions.items():
                encoded_state = extract_conditions(state.values,key,value,encoded_state)
            for key,value in self.goal_num_conditions.items():
                encoded_state = extract_numeric_goals_in_state(state.values,key,value,encoded_state)
            for key,value in self.augmented_goals.items():
                encoded_state = extract_augmented_goals_objects(state.values,key,value,encoded_state)
            for key,value in bool_encoded_state.items():
                encoded_tensor.update({key: torch.tensor(flatten_list(value))})
            for key,value in encoded_state.items():
                encoded_tensor.update({key: torch.tensor(flatten_list(value))})
            encoded_tensors.append(encoded_tensor)
        
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
        

def gnnHeuristic(path,predicates,goal_predicates,objects,obj_encoding,num_conditions,goal_num_conditions,num_conditions_in_goal,augmented_goals,goals,aggregation,readout,gpus,state,constants):
    Model = __load_model__(aggregation, readout)
    if gpus > 0 and torch.cuda.is_available():
        device = torch.device('cuda')
        print("running with GPU")
    else: 
        device = torch.device('cpu')
        print("running with CPU")
    model = Model.load_from_checkpoint(checkpoint_path=str(path), strict=False).to(device)
    goal_encoding = encode_goal_state(goal_predicates)
    num_conditions_in_goal = dict()
    for key,value in goal_num_conditions.items():
        num_conditions_in_goal = extract_numeric_goals(key,value,num_conditions_in_goal)
        
    return GnnCondAugmented(model, predicates, goal_predicates, objects, obj_encoding, num_conditions, goal_num_conditions,num_conditions_in_goal,augmented_goals,model.encoding,goals,goal_encoding,constants)


def __load_model__(aggregation,readout):
    try:
        Model = g_model_classes[(aggregation, readout, 'supervised_optimal',True,False)]   
    except KeyError:
        raise NotImplementedError(f"No model found for {(aggregation, readout, 'supervised_optimal',True,False)} combination")
    return Model


def flatten_list(nested_list):
    flattened_list = []
    for element in nested_list:
        if isinstance(element, list):
            flattened_list.extend(flatten_list(element))
        else:
            flattened_list.append(element)
    return flattened_list

def collate(batch: List[Dict[str, Tensor]], device):
    """
    Input: [state]
    Output: (states, sizes)
    """
    input = {}
    sizes = []
    offset = 0
    for state in batch:
        max_size = 0
        for predicate, values in state.items():
            if values.nelement() > 0:
                max_size = max(max_size, int(torch.max(values)) + 1)
            if predicate not in input: input[predicate] = []
            input[predicate].append(values + offset)
        sizes.append(max_size)
        offset += max_size
    for predicate in input.keys():
        input[predicate] = torch.cat(input[predicate]).view(-1).to(device=device, non_blocking=True)
    return (input, sizes)


    