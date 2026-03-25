from data_structures.extended_conditions import  checkIfNumeric, standardizeGoal, extractPreconditionRecursive, normalize_conditions
from data_structures.goals import Goal
import re
from fractions import Fraction

class AugmentedGoal(Goal):
    def __init__(self, goal_expr,atoms,bool_goal, segments):
        super().__init__(goal_expr,atoms,bool_goal)
        self.segments = segments

class Segments:
    def __init__(self, atoms,alpha,k_expr):
        self.k_expr = k_expr
        self.alpha = alpha
        self.atoms = atoms

def getAugmentedGoalsMap(goals,objects,obj_encoding,norm_conditions = "left", constants = False):
    num_conditions_map = dict()
    goal_num_conditions_map = dict()
    augmented_goals_map = dict()
    for goal in goals:
        if checkIfNumeric(goal):
            conditions,special = extractNormalization(goal,objects,norm_conditions,constants)

            newGoal = standardizeGoal(goal)

            for atom in newGoal.atoms:
                atom.addObjectEncoding(obj_encoding)
            if special:
                segments = list()
                for i in conditions[1]:
                    atoms = list()
                    for j in newGoal.atoms:
                        if j.name in i["formula"]:
                            atoms.append(j)
                    segments.append(Segments(atoms,i["alpha"],i["k"]))
                specialGoal = AugmentedGoal(newGoal.goal_expr,newGoal.atoms,newGoal.bool_goal,segments)
                augmented_goals_map.setdefault(conditions[0],[]).append(specialGoal)
            else:
                num_conditions_map.setdefault(conditions[0],[]).append(newGoal)
                goal_num_conditions_map.setdefault("goal_" + conditions[0],[]).append(newGoal)
            
    return num_conditions_map,goal_num_conditions_map, augmented_goals_map



def extractNormalization(condition,parameters,norm_conditions,constants):
    out = ""
    param_list = list()
    cond_list = list()
    arities = list()
    fluents = list()
    const = False
    if constants != False and  (not set(constants) <= set(parameters)):
            const = True
    out = extractPreconditionRecursive(condition,out,parameters,param_list,cond_list,arities,const,constants)
    if len(param_list) > 1:
            special_goals = [out,extractSpecialGoals(str(condition))]
            return special_goals, True
    cond_list.append(out)
    arities.append(len(param_list))

    cond_list = normalize_conditions(cond_list,norm_conditions)
    
    return cond_list, False

def extractSpecialGoals(condition):
    # Estrai la soglia numerica a sinistra del <=
    threshold_match = re.search(r"\(?\s*(\d+)\s*<=", condition)
    threshold = int(threshold_match.group(1)) if threshold_match else None

    # Estrai tutti i termini tipo coeff * x(farmN)
    pattern = r'([0-9/\.]+)\s*\*\s*x\(farm(\d+)\)'
    matches = re.findall(pattern, condition)
    terms = [(float(Fraction(c)), f"x(farm{v})") for c, v in matches]

    # Rimuovi i termini dei fluenti dalla stringa
    cleaned_expr = re.sub(pattern, '', condition)

    # Trova i simboli extra con i loro segni
    symbol_exprs = re.findall(r'([\+\-]?)\s*([a-zA-Z_][a-zA-Z0-9_]*)', cleaned_expr)

    extras = []
    k_term_names = []
    for sign, name in symbol_exprs:
        if name.startswith("x") or name.startswith("farm") or name == "x":
            continue
        sign = sign.strip()
        inverted_sign = '-' if sign == '+' else '+' if sign == '-' else '+'
        term = f"{inverted_sign} {name}".strip()
        extras.append(term)
        k_term_names.append(name)

    # Costruzione dell’espressione simbolica k
    if extras:
        extra_expr = ' '.join(extras).replace('+ -', '-').replace('- -', '+')
        k_expr = f"{threshold} {extra_expr}"
    else:
        k_expr = str(threshold)
        k_term_names = []

    # Costruisci la lista delle relazioni binarie
    binary_relations = []
    for i in range(len(terms) - 1):
        (c1, v1), (c2, v2) = terms[i], terms[i+1]
        formula = f"{v1} + {v2} >= {k_expr}"
        binary_relations.append({
            "formula": formula,
            "alpha": [c1, c2],
            "k": [k_expr,k_term_names]
        })

    return binary_relations

def extract_augmented_goals_pairs(state,key,values,encoded_state):
    encoded_state.setdefault("augmented_condition",[[],[]])
    encoded_state.setdefault("goal_augmented_condition",[[],[]])
    for value in values:
        obj_list = list()
        if value.checkGoal(state):
                for segment in value.segments:
                    obj_list = list()
                    for atom in segment.atoms:
                        if len(atom.objects) > 0:
                            encoded_state["augmented_condition"][1].append(state[atom.name])
                            encoded_state["goal_augmented_condition"][1].append(state[atom.name])
                        for obj in atom.objects:
                            if obj.encoding_id not in obj_list:
                                obj_list.append(obj.encoding_id)
                                encoded_state["augmented_condition"][0].append(obj.encoding_id)
                                encoded_state["goal_augmented_condition"][0].append(obj.encoding_id)
                    for a in segment.alpha:
                        encoded_state["augmented_condition"][1].append(a)
                        encoded_state["goal_augmented_condition"][1].append(a)
                    k = segment.k_expr[0]
                    for i in segment.k_expr[1]:
                        k = k.replace(i, str(state[i]))
                    k = eval(k)
                    encoded_state["augmented_condition"][1].append(k)
                    encoded_state["goal_augmented_condition"][1].append(k)
        else:
            for segment in value.segments:    
                obj_list = list()
                for atom in segment.atoms:
                    if len(atom.objects) > 0:
                        encoded_state["goal_augmented_condition"][1].append(state[atom.name])
                    for obj in atom.objects:
                        if obj.encoding_id not in obj_list:
                            obj_list.append(obj.encoding_id)
                            encoded_state["goal_augmented_condition"][0].append(obj.encoding_id)
                            
                for a in segment.alpha:
                    encoded_state["goal_augmented_condition"][1].append(a)
                    
                k = segment.k_expr[0]
                for i in segment.k_expr[1]:
                    k = k.replace(i, str(state[i]))
                k = eval(k)
                encoded_state["goal_augmented_condition"][1].append(k)

            
    return encoded_state


def extract_augmented_goals_objects(state,key,values,encoded_state):
    encoded_state.setdefault("augmented_condition",[])
    encoded_state.setdefault("goal_augmented_condition",[])
    for value in values:
        obj_list = list()
        if value.checkGoal(state):
                for segment in value.segments:
                    obj_list = list()
                    for atom in segment.atoms:

                        for obj in atom.objects:
                            if obj.encoding_id not in obj_list:
                                obj_list.append(obj.encoding_id)
                                encoded_state["augmented_condition"].append(obj.encoding_id)
                                encoded_state["goal_augmented_condition"].append(obj.encoding_id)
        else:
            for segment in value.segments:    
                obj_list = list()
                for atom in segment.atoms:
                    for obj in atom.objects:
                        if obj.encoding_id not in obj_list:
                            obj_list.append(obj.encoding_id)
                            encoded_state["goal_augmented_condition"].append(obj.encoding_id)
    return encoded_state