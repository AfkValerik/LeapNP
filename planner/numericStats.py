import argparse 
import contextlib
from fractions import Fraction
import io
import glob
from data_structures import get_problem, get_grounded_problem,standardizeGoals, standardizeActions, extractInitValues, extractAtom
import os
import sys
import tempfile
import re

class C_StdoutRedirector:
    def __init__(self):
        # Crea un file temporaneo in lettura/scrittura testuale
        self.temp_file = tempfile.TemporaryFile(mode='w+t')
        self.original_stdout_fd = sys.stdout.fileno()
        # Salva il vero standard output
        self.saved_stdout_fd = os.dup(self.original_stdout_fd)
        self.output = ""

    def __enter__(self):
        # Dirotta l'output di sistema (fd 1) verso il file temporaneo
        os.dup2(self.temp_file.fileno(), self.original_stdout_fd)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Ripristina l'output originale di sistema
        os.dup2(self.saved_stdout_fd, self.original_stdout_fd)
        os.close(self.saved_stdout_fd)
        # Legge cosa è stato catturato nel file temporaneo
        self.temp_file.seek(0)
        self.output = self.temp_file.read()
        self.temp_file.close()

def _parse_arguments():
    parser = argparse.ArgumentParser()
    default_grounder = "enhsp"
    
    
    parser.add_argument('--o', required=True, type=str, help='path to domain file')
    parser.add_argument('--p', required=True, type=str, help='path directory containing problem files')
    parser.add_argument('--grounder',default = default_grounder, type = str, help = f'grounder to use (default={default_grounder})')
    
    args = parser.parse_args()
    return args
    
    
    
    
def _main(args):
    analyze_problems(args.o,args.p,args.grounder)
    
    
    
def analyze_problems(domain,path,grounder):
    fluents_ratios = list()
    conditions_ratios = list()
    actual_fluents_ratios = list()
    search_pattern = os.path.join(path, "*.pddl")
    

    for instance_path in glob.glob(search_pattern):

        filename = os.path.basename(instance_path)
        
        if os.path.isfile(instance_path) and filename != "domain.pddl":
            print(f"Analyzing problem: {filename}")
            fluents_ratio,conditions_ratio,actual_fluents_ratio = analyze_problem(domain, instance_path, grounder)
            fluents_ratios.append(fluents_ratio)
            conditions_ratios.append(conditions_ratio)
            actual_fluents_ratios.append(actual_fluents_ratio)
    
    avg_fluents = sum(fluents_ratios) / len(fluents_ratios) if fluents_ratios else 0
    avg_conditions = sum(conditions_ratios) / len(conditions_ratios) if conditions_ratios else 0
    avg_actual_fluents = sum(actual_fluents_ratios) / len(actual_fluents_ratios) if actual_fluents_ratios else 0
    print(f"Ratio of all numeric fluents: {avg_fluents:.2f}")
    print(f"Ratio of numeric conditions: {avg_conditions:.2f}")
    print(f"Ratio of numeric fluents: {avg_actual_fluents:.2f}")
    
    
            

                    
            
def analyze_problem(domain, instance,grounder):
    problem = get_problem(domain, instance)
    
    redirector = C_StdoutRedirector()
    
    with redirector:
        groundedProblem = get_grounded_problem(problem, grounder)
        
    # L'output ora è salvato qui dentro!
    output_str = redirector.output
    
    # Debug: decommenta questa riga per vedere se sta catturando davvero
    # print(f"DEBUG OUTPUT CATTURATO:\n{output_str}")
    
    # Estrazione con espressioni regolari
    f_match = re.search(r"\|F\|:\s*(\d+)", output_str)
    x_match = re.search(r"\|X\|:\s*(\d+)", output_str)
    
    f_val = int(f_match.group(1)) if f_match else 0
    x_val = int(x_match.group(1)) if x_match else 0
    
    
    initial_state = problem.initial_values
    goals = problem.goals
    #actions = problem.actions
    groundedActions = groundedProblem.problem.actions
    if 'and' in str(problem.goals[0]):
        goals = problem.goals[0].args
    else:
        goals = [problem.goals[0]]
        
    check_goals = standardizeGoals(goals)
    groundedActions = standardizeActions(groundedActions)
    original_initial_state = get_initial_state(initial_state)
    initial_state = extractInitValues(original_initial_state)
    
    
    num_fluents = 0
    bool_fluents = 0
    num_conditions = 0
    bool_conditions = 0
    for key, value in initial_state.items():
        if isinstance(value, bool):
            bool_fluents += 1
        else:
            num_fluents += 1
            
    for goal in check_goals:
        if goal.bool_goal:
            bool_conditions += 1
        else:
            num_conditions += 1
            
    for action in groundedActions:
        for pre in action.preconditions:
            if pre.is_bool:
                bool_conditions += 1
            else:
                num_conditions += 1
    
    total_fluents = num_fluents + bool_fluents
    total_conditions = num_conditions + bool_conditions
    fluents_ratio = num_fluents / total_fluents if total_fluents > 0 else 0
    conditions_ratio = num_conditions / total_conditions if total_conditions > 0 else 0
    actual_fluents_ratio = x_val / (f_val + x_val) if (f_val + x_val) > 0 else 0
    return fluents_ratio, conditions_ratio, actual_fluents_ratio
    
def get_initial_state(input):
    initial_state = dict()
    tmp_vals = [str_to_bool(v) if v.node_type.name == "BOOL_CONSTANT" else float(Fraction(str(v))) for v in input.values()]
    
    for key,value in zip(input,tmp_vals):

        initial_state.update({str(key): extractAtom(key,value)})

    return initial_state

def str_to_bool(s):
    return str(s).lower() == 'true'


if __name__ == "__main__":
    args = _parse_arguments()
    _main(args)
    
