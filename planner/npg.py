from fractions import Fraction
from heuristic import gnnCondHeuristic, gnnValHeuristic, gnnBaseHeuristic, gnnAugmentedHeuristic, gnnCondAugmentedHeuristic
from search_algorithms import BFS, MEBFS, Astar, MEAstar, WAstar, MEWAstar, GS, DBFS
from data_structures import  encode_objects,standardizeGoals, standardizeActions,extractAtom, getPreconditionsMap, getPredicatesMap, getGoalsMap, extractInitValues, getAugmentedGoalsMap
from search_problem import PlanningProblem
import time
import os
import random
import numpy as np
import torch

"""
def set_global_seed(seed: int):
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    try:
        torch.use_deterministic_algorithms(True,warn_only=True)
        os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":4096:8"
    except Exception:
        pass
"""
def set_global_seed(seed: int, strict: bool = False):
    """
    set global seeds to ensure reproducibility.
    
    Args:
        seed (int): the seed value to set
        strict (bool): if true enforce absolute determinism (a lot slower, do not use)
    """
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

    if strict:
        # Modalità deterministica totale (rallenta parecchio)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
        try:
            torch.use_deterministic_algorithms(True, warn_only=True)
            os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":4096:8"
        except Exception:
            pass
    else:
        # Modalità "bilanciata": riproducibile ma veloce
        torch.backends.cudnn.deterministic = False
        torch.backends.cudnn.benchmark = True

def setup_problem(dom,problem,groundedProblem,search_algorithm,heuristicName,network,gpus,aggregation,readout,multiple_eval,w = 1,seed=None, norm_conditions = "left"):
    if seed is not None and seed >= 0:
        set_global_seed(seed)
    start = time.time()
    initial_state = problem.initial_values
    goals = problem.goals
    #actions = problem.actions
    objects = problem.all_objects
    groundedActions = groundedProblem.problem.actions
    if 'and' in str(problem.goals[0]):
        goals = problem.goals[0].args
    else:
        goals = [problem.goals[0]]
        
    
    check_goals = standardizeGoals(goals)
    groundedActions = standardizeActions(groundedActions)
    #TODO: constants not used right now, check if needed and decide what to do with them accordingly
    #constants = get_constants(dom,objects)
    constants = []
    original_initial_state = get_initial_state(initial_state)
    obj_encoding = encode_objects(objects)
    predicates_map, goal_predicates_map = getPredicatesMap(original_initial_state,check_goals,obj_encoding)
    initial_state = extractInitValues(original_initial_state)
    if  network is not None:
        if heuristicName == "gnnval" or heuristicName == "gnncond":
            num_conditions_map, goal_num_conditions_map = getGoalsMap(goals,problem.all_objects,obj_encoding, norm_conditions = "left")
            preconditions_map = getPreconditionsMap(groundedProblem.map_back_action_instance.keywords["map"],obj_encoding,initial_state, norm_conditions = "left")
            #preconditions_map = prova(preconditions_map)
        elif heuristicName == "gnnaugmented" or heuristicName == "gnncondaugmented":
            num_conditions_map, goal_num_conditions_map, augmented_goals_map = getAugmentedGoalsMap(goals,problem.all_objects,obj_encoding, norm_conditions = "left")
            preconditions_map = getPreconditionsMap(groundedProblem.map_back_action_instance.keywords["map"],obj_encoding,initial_state, norm_conditions = "left")
        #starting version that does not handle numeric features
        elif heuristicName == "gnnbase":
            pass

        if heuristicName == "gnncond":
            heuristic = gnnCondHeuristic(network,predicates_map,goal_predicates_map,objects,obj_encoding,preconditions_map,num_conditions_map,goal_num_conditions_map,check_goals,aggregation,readout,gpus,initial_state,constants)
        elif heuristicName == "gnnaugmented":
             heuristic = gnnAugmentedHeuristic(network,predicates_map,goal_predicates_map,objects,obj_encoding,preconditions_map,num_conditions_map,goal_num_conditions_map,augmented_goals_map,check_goals,aggregation,readout,gpus,initial_state,constants)
        elif heuristicName == "gnnval":
            heuristic = gnnValHeuristic(network,predicates_map,goal_predicates_map,objects,obj_encoding,preconditions_map,num_conditions_map,goal_num_conditions_map,check_goals,aggregation,readout,gpus,initial_state,constants)
        elif heuristicName == "gnncondaugmented":
            heuristic = gnnCondAugmentedHeuristic(network,predicates_map,goal_predicates_map,objects,obj_encoding,preconditions_map,num_conditions_map,goal_num_conditions_map,augmented_goals_map,check_goals,aggregation,readout,gpus,initial_state,constants)
        elif heuristicName == "gnnbase":
            heuristic = gnnBaseHeuristic(network,predicates_map,goal_predicates_map,objects,encode_objects(objects),goals,aggregation,readout,gpus,initial_state,constants)

    end = time.time()
    print("initial setup done, time: ", (end - start))
    
    problem = PlanningProblem(initial_state,check_goals,groundedActions)
    
    if search_algorithm == "bfs":
            if multiple_eval:
                search = MEBFS(heuristic)
            else:
                search = BFS(heuristic)
    elif search_algorithm == "dbfs":
        search = DBFS(heuristic)
    #TODO: ensure that other search algorithms are updated according with the new data structures (probably not)
    elif search_algorithm == 'astar':
        if multiple_eval:
            search = MEAstar(heuristic)
        else:
            search = Astar(heuristic)
    elif search_algorithm == 'wastar':
        if multiple_eval:
            search = MEWAstar(heuristic,w)
        else: 
            search = WAstar(heuristic, w)
    elif search_algorithm == 'greedy':
        search = GS(heuristic)
                
    start = time.time()
    path,goal = search.solve(problem)
    end = time.time()
    print("solution found, time: ", (end - start))
    return path,goal,search.expanded,search.evaluated,path.count("\n")
        

def get_initial_state(input):
    initial_state = dict()
    tmp_vals = [str_to_bool(v) if v.node_type.name == "BOOL_CONSTANT" else float(Fraction(str(v))) for v in input.values()]
    
    for key,value in zip(input,tmp_vals):

        initial_state.update({str(key): extractAtom(key,value)})

    return initial_state

    
def str_to_bool(s):
    return str(s).lower() == 'true'

#TODO: figure out what to do with constants
def get_constants(domain,objects):
    with open(domain,"r") as f:
            filedom = f.read()
    f.close()
    if "(:constants" in filedom:
        constdom = filedom.split("(:constants")[1].split("-")[0]
        constdom = constdom.split(" ")[1:-1]
        constants = list()
        for i in constdom:
            for j in objects:
                if i == j.name:
                    constants.append(j)
                    break
        return constants
    else:
        return False
    
