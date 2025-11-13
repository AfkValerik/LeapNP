from .dataset      import collate_no_label, load_directory, load_file, load_problem, load_file_spanner
from .extract_encoded_states import get_encoded_states, get_encoded_states_with_values, get_condition_encoded_states,get_encoded_states_with_fluents, get_encoded_states_with_values_fluents
from .extract_relations import get_relations, get_num_relations,get_condition_relations, get_fluents_relations, get_num_actions, get_fluents_num_relations

from .supervised   import load_dataset as supervised_load
from .supervised   import collate      as supervised_collate
from .numeric_supervised import load_dataset as numeric_supervised_load
from .numeric_supervised import collate      as numeric_supervised_collate
from .condition_supervised import load_dataset as condition_supervised_load
from .condition_supervised import collate      as condition_supervised_collate


g_dataset_methods = {
    ('supervised_optimal', False,False,"conditions",False):         (supervised_load, supervised_collate),
    ('supervised_optimal', True,True,"conditions",False):          (numeric_supervised_load, numeric_supervised_collate),
    ('supervised_optimal', True,False,"conditions",False):         (condition_supervised_load, condition_supervised_collate),
}

