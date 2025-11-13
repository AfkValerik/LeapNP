import torch


#function for the version that evaluates numeric condition as boolean values old dataset version
def get_condition_encoded_states_old(instance,predicates,max_samples_per_file = None):
    encoded_states = list(list())
    states = instance['instance']['states']
    
    for state in states:

        state_value = torch.tensor([state['state_value']])
        encoded_state = dict()
        for key,value in state['bool_encoded_state'].items():
            encoded_state.update({key: torch.tensor(flatten_list(value))})
            
        for key,values in state['encoded_state'].items():
            if key in predicates:
                if len(values) > 0:
                    objs = list()
                    for value in values:
                        objs.append(value[0])
                    encoded_state.update({key: objs})
                    encoded_state.update({key: torch.tensor(flatten_list(encoded_state[key]))})
                else:
                    encoded_state.update({key: torch.tensor([])})


        for key,values in state['encoded_preconditions'].items():
            if key in predicates:
                if ("goal_" + key) in encoded_state:
                    if len(values) > 0:
                        objs = list()
                        nums = list()
                        for value in values:
                            objs.append(value[0])


                        encoded_state.update({key: objs})
                        encoded_state.update({key: torch.tensor(flatten_list(encoded_state[key]))})

                    else:
                        encoded_state.update({key: torch.tensor([])})
                else:
                    if len(values) > 1:
                        encoded_state.update({key: values[0]})
                        encoded_state.update({key: torch.tensor(flatten_list(encoded_state[key]))})
                    elif len(values) > 0:
                        encoded_state.update({key: values[0][0]})
                        encoded_state.update({key: torch.tensor(flatten_list(encoded_state[key]))})
                    else:
                        encoded_state.update({key: torch.tensor([])})
        
        new_tuple = tuple((state_value,encoded_state))
        if max_samples_per_file is None or len(encoded_states) < max_samples_per_file:
            encoded_states.append(new_tuple)
        else:
            break
        
    return encoded_states

#function for the version that evaluates numeric condition as boolean values 
def get_condition_encoded_states(instance,predicates,max_samples_per_file = None, actions_readout = False):
    encoded_states = list(list())
    states = instance['instance']['states']

    for neighbours in states:
        for _,boilerplate in neighbours.items():
            for state in boilerplate:
                if actions_readout:
                    state_value = torch.tensor(flatten_list(list(state['encoded_actions'].values())))
                else:
                    state_value = torch.tensor([state['state_value']])
                encoded_state = dict()
                for key,value in state['bool_encoded_state'].items():
                    encoded_state.update({key: torch.tensor(flatten_list(value))})
                    
                for key,values in state['encoded_state'].items():
                    if key in predicates:
                        if len(values) > 1:
                            encoded_state.update({key: values[0]})
                            encoded_state.update({key: torch.tensor(flatten_list(encoded_state[key]))})
                        elif len(values) > 0:
                            encoded_state.update({key: values[0][0]})
                            encoded_state.update({key: torch.tensor(flatten_list(encoded_state[key]))})
                        else:
                            encoded_state.update({key: torch.tensor([])})
                            
                for key,values in state['encoded_preconditions'].items():
                    if key in predicates:
                        if len(values) > 1:
                            encoded_state.update({key: values[0]})
                            encoded_state.update({key: torch.tensor(flatten_list(encoded_state[key]))})
                        elif len(values) > 0:
                            encoded_state.update({key: values[0][0]})
                            encoded_state.update({key: torch.tensor(flatten_list(encoded_state[key]))})
                        else:
                            encoded_state.update({key: torch.tensor([])})
                
                new_tuple = tuple((state_value,encoded_state))
                if max_samples_per_file is None or len(encoded_states) < max_samples_per_file:
                    encoded_states.append(new_tuple)
                else:
                    break
        
    return encoded_states


def get_encoded_states_with_values_old(instance,predicates,max_samples_per_file = None):
    encoded_states = list(list())
    states = instance['instance']['states']
    encoding = dict([(predicate, index) for index, (predicate, _,_) in enumerate(predicates)])
    for state in states:

        state_value = torch.tensor([state['state_value']])
        encoded_state = dict()
        num_values = dict()
        for key,values in state['encoded_state'].items():
            if len(values) > 0:
                objs = list()
                nums = list()
                for value in values:
                    objs.append(value[0])
                    nums.append(value[1])

                encoded_state.update({key: objs})
                encoded_state.update({key: torch.tensor(flatten_list(encoded_state[key]))})
                num_values.update({encoding[key]: nums})
                num_values.update({encoding[key]: torch.tensor(flatten_list(num_values[encoding[key]]))})
            else:
                encoded_state.update({key: torch.tensor([])})
                num_values.update({encoding[key]: torch.tensor([])})
        for key,values in state['encoded_preconditions'].items():
          if ("goal_" + key) in encoded_state:
                if len(values) > 0:
                    objs = list()
                    nums = list()
                    for value in values:
                        objs.append(value[0])
                        nums.append(value[1])

                    encoded_state.update({key: objs})
                    encoded_state.update({key: torch.tensor(flatten_list(encoded_state[key]))})
                    num_values.update({encoding[key]: nums})
                    num_values.update({encoding[key]: torch.tensor(flatten_list(num_values[encoding[key]]))})
                else:
                    encoded_state.update({key: torch.tensor([])})
                    num_values.update({encoding[key]: torch.tensor([])})
          else:
            if len(values) > 1:
                encoded_state.update({key: values[0]})
                encoded_state.update({key: torch.tensor(flatten_list(encoded_state[key]))})
                num_values.update({encoding[key]: values[1]})
                num_values.update({encoding[key]: torch.tensor(flatten_list(num_values[encoding[key]]))})
            elif len(values) > 0:
                encoded_state.update({key: values[0][0]})
                encoded_state.update({key: torch.tensor(flatten_list(encoded_state[key]))})
                num_values.update({encoding[key]: values[0][1]})
                num_values.update({encoding[key]: torch.tensor(flatten_list(num_values[encoding[key]]))})
            else:
                encoded_state.update({key: torch.tensor([])})
                num_values.update({encoding[key]: torch.tensor([])})
        for key,values in state['bool_encoded_state'].items():
            encoded_state.update({key: values})
            encoded_state.update({key: torch.tensor(flatten_list(encoded_state[key]))})
            num_values.update({encoding[key]: torch.tensor([])})
            
        new_tuple = tuple((state_value,encoded_state,num_values))
        if max_samples_per_file is None or len(encoded_states) < max_samples_per_file:
            encoded_states.append(new_tuple)
        else:
            break
        
    return encoded_states




#function for the numeric values version of the GNN
def get_encoded_states_with_values(instance,predicates,max_samples_per_file = None, actions_readout = False):
    encoded_states = list(list())
    states = instance['instance']['states']
    encoding = dict([(predicate, index) for index, (predicate, _,_) in enumerate(predicates)])
    for neighbours in states:
        for _,boilerplate in neighbours.items():
            for state in boilerplate:
                if actions_readout:
                    state_value = torch.tensor(flatten_list(list(state['encoded_actions'].values())))
                else:
                    state_value = torch.tensor([state['state_value']])
                encoded_state = dict()
                num_values = dict()
                for key,values in state['encoded_state'].items():
                    if len(values) > 1:
                        encoded_state.update({key: values[0]})
                        encoded_state.update({key: torch.tensor(flatten_list(encoded_state[key]))})
                        num_values.update({encoding[key]: values[1]})
                        num_values.update({encoding[key]: torch.tensor(flatten_list(num_values[encoding[key]]))})
                    elif len(values) > 0:
                        encoded_state.update({key: values[0][0]})
                        encoded_state.update({key: torch.tensor(flatten_list(encoded_state[key]))})
                        num_values.update({encoding[key]: values[0][1]})
                        num_values.update({encoding[key]: torch.tensor(flatten_list(num_values[encoding[key]]))})
                    else:
                        encoded_state.update({key: torch.tensor([])})
                        num_values.update({encoding[key]: torch.tensor([])})
                for key,values in state['encoded_preconditions'].items():
                    if len(values) > 1:
                        encoded_state.update({key: values[0]})
                        encoded_state.update({key: torch.tensor(flatten_list(encoded_state[key]))})
                        num_values.update({encoding[key]: values[1]})
                        num_values.update({encoding[key]: torch.tensor(flatten_list(num_values[encoding[key]]))})
                    elif len(values) > 0:
                        encoded_state.update({key: values[0][0]})
                        encoded_state.update({key: torch.tensor(flatten_list(encoded_state[key]))})
                        num_values.update({encoding[key]: values[0][1]})
                        num_values.update({encoding[key]: torch.tensor(flatten_list(num_values[encoding[key]]))})
                    else:
                        encoded_state.update({key: torch.tensor([])})
                        num_values.update({encoding[key]: torch.tensor([])})
                for key,values in state['bool_encoded_state'].items():
                    encoded_state.update({key: values})
                    encoded_state.update({key: torch.tensor(flatten_list(encoded_state[key]))})
                    num_values.update({encoding[key]: torch.tensor([])})
                    
                new_tuple = tuple((state_value,encoded_state,num_values))
                if max_samples_per_file is None or len(encoded_states) < max_samples_per_file:
                    encoded_states.append(new_tuple)
                else:
                    break
        
    return encoded_states

#boolean version
def get_encoded_states(instance,max_samples_per_file = None, actions_readout = False):
    encoded_states = list(list())
    states = instance['instance']['states']
    for neighbours in states:
        for _,boilerplate in neighbours.items():
            for state in boilerplate:
                if actions_readout:
                    state_value = torch.tensor(flatten_list(list(state['encoded_actions'].values())))
                else:
                    state_value = torch.tensor([state['state_value']])
                encoded_state = dict()
                for key,values in state['bool_encoded_state'].items():
                    encoded_state.update({key: values})
                    encoded_state.update({key: torch.tensor(flatten_list(encoded_state[key]))})
                    
                new_tuple = tuple((state_value,encoded_state))
                if max_samples_per_file is None or len(encoded_states) < max_samples_per_file:
                    encoded_states.append(new_tuple)
                else:
                    break
        
    return encoded_states

   
#if the input is a matrix of dimensions [X,Y] , it flattens it returning a list of dimension [X*Y]
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




    