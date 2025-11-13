
import torch
from typing import Dict, List, Tuple, Any
import unicodedata
from torch.functional import Tensor
from heuristic.NNheuristic import NNHeuristic


from data_structures import encode_state,encode_goal_state, extract_goal_condition_object_pairs, extract_num_values, extract_condition_object_pairs, get_encoded_states_with_values
from architecture import g_model_classes

def normalize(s: str,
              remove_all_spaces: bool = False,
              collapse_spaces: bool = True,
              ignore_case: bool = False,
              unicode_norm: str = "NFC") -> str:
    """
    Normalizza la stringa:
      - unicode normalization (NFC by default)
      - opzionalmente rimuove tutti gli spazi o collassa gli spazi multipli
      - opzionalmente ignora il case
    """
    if not isinstance(s, str):
        s = str(s)
    s = unicodedata.normalize(unicode_norm, s)
    if remove_all_spaces:
        s = s.replace(" ", "")
    elif collapse_spaces:
        # collassa ogni sequenza di whitespace in un singolo spazio e strip esterno
        s = " ".join(s.split())
    else:
        s = s.strip()
    if ignore_case:
        s = s.lower()
    return s

def map_keys_using_dict1(dict1: Dict[str, Any],
                        dict2: Dict[str, Any],
                        remove_all_spaces: bool = False,
                        collapse_spaces: bool = True,
                        ignore_case: bool = False,
                        unicode_norm: str = "NFC",
                        keep_unmatched: bool = True) -> Dict[str, Any]:
    """
    Restituisce una nuova versione di dict2 dove, se possibile, ogni chiave di dict2
    viene sostituita con la chiave corrispondente presente in dict1 (trovata usando
    la normalizzazione). Se non trova corrispondenza, mantiene la chiave originale
    (se keep_unmatched=True) oppure salta quella coppia (se False).
    """
    # costruisco mappa normalizzata -> chiave originale di dict1 (in caso di clash,
    # mantiene la prima comparsa; si può modificare se si preferisce comportamento diverso)
    norm_to_key1 = {}
    for k1 in dict1.keys():
        nk = normalize(k1, remove_all_spaces, collapse_spaces, ignore_case, unicode_norm)
        if nk not in norm_to_key1:
            norm_to_key1[nk] = k1

    new_dict2 = {}
    for k2, v2 in dict2.items():
        nk2 = normalize(k2, remove_all_spaces, collapse_spaces, ignore_case, unicode_norm)
        if nk2 in norm_to_key1:
            matched_key = norm_to_key1[nk2]
            new_dict2[matched_key] = v2
        else:
            if keep_unmatched:
                new_dict2[k2] = v2
            # altrimenti skip
    return new_dict2
class GnnVal(NNHeuristic):
    def __init__(self, model, predicates, goal_predicates, objects, obj_encoding, num_conditions, goal_num_conditions,num_conditions_in_goal,encoding,goals,goal_encoding,constants):
        self.model = model
        self.predicates = predicates
        self.goal_predicates = goal_predicates
        self.objects = objects
        self.obj_encoding = obj_encoding
        self.num_conditions = num_conditions = map_keys_using_dict1(encoding, num_conditions)
        self.goal_num_conditions = map_keys_using_dict1(encoding, goal_num_conditions)
        self.num_conditions_in_goal = map_keys_using_dict1(encoding, num_conditions_in_goal)
        self.goals = goals
        self.goal_encoding = goal_encoding
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
        
        input = collate(encoded_tensors,self.model.device)
        with torch.no_grad():
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
        with torch.no_grad():
            input = collate(encoded_tensors,self.model.device)
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
        
        #encoded_state = encoded_state|condition_state
        return encoded_state,bool_encoded_state

        

def gnnHeuristic(path,predicates,goal_predicates,objects,obj_encoding,num_conditions,goal_num_conditions,num_conditions_in_goal,goals,aggregation,readout,gpus,state,constants):
    Model = __load_model__(aggregation, readout)
    if gpus > 0 and torch.cuda.is_available():
        device = torch.device('cuda')
        print("running with GPU")
    else: 
        device = torch.device('cpu')
        print("running with CPU")
    model = Model.load_from_checkpoint(checkpoint_path=str(path), strict=False).to(device)
    goal_encoding = encode_goal_state(goal_predicates)
    
        
    return GnnVal(model, predicates, goal_predicates, objects, obj_encoding, num_conditions, goal_num_conditions,num_conditions_in_goal,model.encoding,goals,goal_encoding,constants)


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


    