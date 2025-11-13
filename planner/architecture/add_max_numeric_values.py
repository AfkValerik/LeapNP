import numpy as np
import torch
import torch.nn as nn
import pytorch_lightning as pl


# Imports related to type annotations
from typing import List, Dict, Tuple
from torch.nn.functional import Tensor

#from datasets.extract_relations import get_relations

class RelationMessagePassing(nn.Module):
    def __init__(self, relations: List[Tuple[int, int]], hidden_size: int):
        super().__init__()
        self.hidden_size = hidden_size
        self.relation_modules = nn.ModuleList()
        self.num_relation_modules = nn.ModuleList()
        self.num_inputs = 2
        #for relation, arity,num_inputs in relations:
        for relation, arity in relations:
            assert relation == len(self.relation_modules)
            input_size = arity * hidden_size
            output_size = arity * hidden_size
            #num_inputs_size = num_inputs * arity
            #TODO: remove the placeholder and pass the value as an input
            num_inputs_size = self.num_inputs * arity
            if (input_size > 0) and (output_size > 0):
                mlp = nn.Sequential(nn.Linear(input_size, input_size, True), nn.ReLU(), nn.Linear(input_size, output_size, True))
                if num_inputs_size > 0:
                    mlpnum = nn.Sequential(nn.Linear(num_inputs_size, num_inputs_size, True), nn.ReLU(), nn.Linear(num_inputs_size, num_inputs_size, True))
                   
                else:
                    mlpnum = None
            else:
                mlp = None
                mlpnum = None
            self.relation_modules.append(mlp)
            self.num_relation_modules.append(mlpnum)
        self.update = nn.Sequential(nn.Linear(2 * (hidden_size + self.num_inputs), 2 * (hidden_size + self.num_inputs), True), nn.ReLU(), nn.Linear(2 * (hidden_size + self.num_inputs), (hidden_size + self.num_inputs), True))
        self.dummy = nn.Parameter(torch.empty(0))

    def get_device(self):
        return self.dummy.device

    def forward(self, node_states: Tuple[Tensor,Tensor], relations: Dict[int, Tensor]) -> Tuple[Tensor, Tensor]:
        # Compute an aggregated message for each recipient
        max_outputs = []
        outputs = []
        sum_msg = torch.zeros_like(node_states[1], dtype=torch.float, device=self.get_device())
        for relation, (module, num_module) in enumerate(zip(self.relation_modules, self.num_relation_modules)):
            if (module is not None) and (relation in relations):
                values = relations[relation]
                if values.dtype != torch.int64:
                    values = values.to(torch.int64)
                
                input = torch.index_select(node_states[0], 0, values).view(-1, module[0].in_features)
                output = module(input).view(-1, self.hidden_size)
                max_outputs.append(torch.max(output))
                node_indices = values.view(-1, 1).expand(-1, self.hidden_size)
                outputs.append((output, node_indices))
                
                #numeric values
                num_input = torch.index_select(node_states[1], 0, values).view(-1, num_module[0].in_features)
                #TODO: change to support different sizes
                num_output = num_module(num_input).view(-1, self.num_inputs)
                num_node_indices = values.view(-1, 1).expand(-1, self.num_inputs)
                sum_msg = torch.scatter_add(sum_msg, 0, num_node_indices, num_output)
                
        max_offset = torch.max(torch.stack(max_outputs))
        exps_sum = torch.full_like(node_states[0], 1E-16, device=self.get_device())
        for output, node_indices in outputs:
            exps = torch.exp(8.0 * (output - max_offset))
            exps_sum = torch.scatter_add(exps_sum, 0, node_indices, exps)

        # Update states with aggregated messages
        max_msg = ((1.0 / 8.0) * torch.log(exps_sum)) + max_offset
                
        # Update states with aggregated messages
        next_node_states = torch.split(self.update(torch.cat([max_msg, sum_msg,node_states[0],node_states[1]], dim=1)),[self.hidden_size,self.num_inputs],dim=1)
        
        return next_node_states


class Readout(nn.Module):
    def __init__(self, input_size: int, output_size: int, bias: bool = True):
        super().__init__()
        self.pre = nn.Sequential(nn.Linear(input_size, input_size, bias), nn.ReLU(), nn.Linear(input_size, input_size, bias))
        self.post = nn.Sequential(nn.Linear(input_size, input_size, bias), nn.ReLU(), nn.Linear(input_size, output_size, bias))
        self.dummy = nn.Parameter(torch.empty(0))

    def get_device(self):
        return self.dummy.device

    def forward(self, batch_num_objects: List[int], node_states: Tensor) -> Tensor:
        # Loopless implementation, faster than the reference implementation.
        cumsum_indices = torch.tensor(batch_num_objects, device=self.get_device()).cumsum(0) - 1  # TODO: This can be computed once.
        cumsum_states = self.pre(node_states).cumsum(0).index_select(0, cumsum_indices)
        aggregated_states = torch.cat((cumsum_states[0].view(1, -1), cumsum_states[1:] - cumsum_states[0:-1]))
        return self.post(aggregated_states)
        # Reference implementation.
        # return self.post(torch.stack([torch.sum(nodes, dim=0) for nodes in self.pre(node_states).split(batch_num_objects)]))

    def feature_vectors(self, batch_num_objects: List[int], node_states: Tensor) -> Tensor:
        results: List[Tensor] = []
        offset: int = 0
        nodes: Tensor = self.pre(node_states)
        for num_objects in batch_num_objects:
            intermediate = []
            intermediate.append(torch.sum(nodes[offset:(offset + num_objects)], dim=0))
            for layer in self.post:
                intermediate.append(layer(intermediate[-1]))
            results.append(torch.cat(intermediate))
            offset += num_objects
        return torch.stack(results)


class RelationMessagePassingModel(nn.Module):
    def __init__(self, relations: list, hidden_size: int, iterations: int):
        super().__init__()
        self.hidden_size = hidden_size
        self.iterations = iterations
        self.relation_network = RelationMessagePassing(relations, hidden_size)
        self.dummy = nn.Parameter(torch.empty(0))

    def get_device(self):
        return self.dummy.device

    def forward(self, states: Tuple[Dict[int, Tensor], List[int]]) -> Tensor:
        node_states = self._initialize_nodes(sum(states[1]),inits=states[2])
        node_states = self._pass_messages(node_states, states[0], states[1])
        return node_states

    def _pass_messages(self, node_states: Tensor, relations: Dict[int, Tensor], batch_num_objects: List[int]) -> Tensor:
        for _ in range(self.iterations):
            node_states = self.relation_network(node_states, relations)
        return node_states

    #put numeric values inside init_nodes
    def _initialize_nodes(self, num_objects: int, inits: Dict[int,List[int]]) -> Tensor:
        max_length = max(len(value) for value in inits.values())
        padded_lists = [[0] * (max_length - len(value)) + value for value in inits.values()]
        init_values = torch.tensor(padded_lists, dtype=torch.float, device=self.get_device())
        init_zeroes = torch.zeros((num_objects, (self.hidden_size // 2) + (self.hidden_size % 2)), dtype=torch.float, device=self.get_device())
        init_random = torch.randn((num_objects, self.hidden_size // 2), device=self.get_device())
        init_nodes = [torch.cat([init_zeroes, init_random], dim=1), init_values]
        return init_nodes


class AddMaxNumericModelValues(pl.LightningModule):
    def __init__(self, predicates: List[Tuple[str, int]], hidden_size: int, iterations: int):
        super().__init__()
        self.save_hyperparameters()
        #changed code to extract everything from the json file
        encoding = dict([(predicate, index) for index, (predicate, _) in enumerate(predicates)])
        arities = [(encoding[predicate], arity) for predicate, arity in predicates]
        #encoding,arities = get_relations(predicates)
        self.encoding = encoding
        self.model = RelationMessagePassingModel(arities, hidden_size, iterations)
        self.readout = Readout((hidden_size + self.model.relation_network.num_inputs), 1)


    def forward(self, states: Tuple[Dict[str, Tensor], List[int]]) -> Tensor:
        encoded_states = (dict([(self.encoding[name], values) for name, values in states[0].items()]), states[1],states[2])
        node_states = self.model(encoded_states)
        value = torch.abs(self.readout(encoded_states[1], torch.cat([node_states[0],node_states[1]],dim=1)))
        return value
    
    def feature_vectors(self, states: Tuple[Dict[int, Tensor], List[int]]) -> Tensor:
        encoded_states = (dict([(self.encoding[name], values) for name, values in states[0].items()]), states[1])
        node_states = self.model(encoded_states)
        value = self.readout.feature_vectors(encoded_states[1], node_states)
        return value

    def freeze_relation_model(self):
        """Freeze the relation message passing model."""
        for param in self.model.parameters():
            param.requires_grad = False

    def unfreeze_relation_model(self):
        """Unfreeze the relation message passing model."""
        for param in self.model.parameters():
            param.requires_grad = True