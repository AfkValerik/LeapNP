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

def getGeneralGoalsMap(goals,objects,obj_encoding,norm_conditions = "left", constants = False):
    augmented_goals_map = dict()
    for goal in goals:
        if checkIfNumeric(goal):
            conditions = extractNormalization(goal,objects,norm_conditions,constants)

            newGoal = standardizeGoal(goal)

            for atom in newGoal.atoms:
                atom.addObjectEncoding(obj_encoding)

                segments = list()
                for i in conditions[1]:
                    atoms = list()
                    for j in newGoal.atoms:
                        if j.name in i["formula"]:
                            atoms.append(j)
                    segments.append(Segments(atoms,i["alpha"],i["k"]))
                specialGoal = AugmentedGoal(newGoal.goal_expr,newGoal.atoms,newGoal.bool_goal,segments)
                if conditions[0][0] not in augmented_goals_map:
                    augmented_goals_map.setdefault(conditions[0][0],[])
                augmented_goals_map[conditions[0][0]].append(specialGoal)

            
    return augmented_goals_map

def extractNormalization(condition,parameters, norm_conditions, constants):
        out = ""
        param_list = list()
        cond_list = list()
        arities = list()
        fluents = list()
        const = False
        if constants != False and  (not set(constants) <= set(parameters)):
            const = True
        out = extractPreconditionRecursive(condition,out,parameters,param_list,cond_list,arities,const, constants)
        match = re.match(r"(.*?)\s*(==|<=|>=|<|>|!=)\s*(\d+(\.\d+)?)", out)
    
        if match:
            lhs = match.group(1).strip() # La variabile, es: balls_num(room)
            op = match.group(2).strip()  # L'operatore, es: ==
        
            out = f"alpha * {lhs} {op} k"
        cond_list.append(out)

        goals = extractSpecialGoals(str(condition))

        cond_list = normalize_conditions(cond_list, norm_conditions)

        out_list = (cond_list,goals)
        return out_list
  
def extractSpecialGoals(condition):
        # Estrai la soglia
        #threshold_match = re.search(r"\(?\s*(\d+)\s*<=", condition)
        FLIP_OPS = {
    '<=': '>=',
    '>=': '<=',
    '<': '>',
    '>': '<',
    '==': '==',
    '!=': '!='
    }
        #threshold_match = re.search(r"(\d+)\s*(?:<=|>=|==|<|>)|(?:<=|>=|==|<|>)\s*(\d+)", condition)
        #threshold = int(threshold_match.group(1) or threshold_match.group(2)) if threshold_match else None
        thresh_pattern = r"(\d+)\s*(<=|>=|==|!=|<|>)|(<=|>=|==|!=|<|>)\s*(\d+)"
        t_match = re.search(thresh_pattern, condition)
        threshold = None
        final_operator = ">=" # Valore di default in caso di errore

        if t_match:
            if t_match.group(1): 
                # Caso: 280 <= ... (Numero a sinistra)
                threshold = int(t_match.group(1))
                raw_op = t_match.group(2)
                # Dobbiamo invertire l'operatore perché metteremo la variabile a sinistra
                final_operator = FLIP_OPS.get(raw_op, raw_op)
            else:
                # Caso: ... == 10 (Numero a destra)
                raw_op = t_match.group(3)
                threshold = int(t_match.group(4))
                # Manteniamo l'operatore così com'è
                final_operator = raw_op
                
        # Estrai tutte le coppie coefficiente * variabile
        pattern = r'(?:([-]?\d+(?:[./]\d+)?)\s*\*\s*)?(\w+)\(([^)]+)\)'

        raw_matches = re.findall(pattern, condition)

        # Costruisci lista di (coefficiente, variabile)
        #terms = [(float(Fraction(c)), f"x(farm{v})") for c, v in matches]
        terms = [
            (float(Fraction(c if c else '1')), f"{func}({arg})") 
            for c, func, arg in raw_matches
            ]
        # Costruisci la lista delle relazioni binarie
        extracted_relations = []
        if len(terms) == 1:
                c, v = terms[0]
                formula = f"{v} {final_operator} {threshold}"
                extracted_relations.append({
                    "formula": formula,
                    "alpha": [c],
                    "k": [threshold,[]]
                })
                
            # CASO BINARIO/MULTIPLO (Sliding Window)
            #TODO: in the future we will have to incorporate binary and more compatibility, and also reintroduce the possibility to have multiple values in k, as in the augmented goals version
        else:
                for i in range(len(terms) - 1):
                    (c1, v1), (c2, v2) = terms[i], terms[i+1]
                    formula = f"{v1} + {v2} {final_operator} {threshold}"
                    extracted_relations.append({
                        "formula": formula,
                        "alpha": [c1, c2],
                        "k": [threshold,[]]
                    })
        return extracted_relations

def extract_general_goals_pairs(state,key,values,encoded_state):
    encoded_state.setdefault(key,[[],[]])
    encoded_state.setdefault("goal_" + key,[[],[]])
    for value in values:
        obj_list = list()
        if value.checkGoal(state):
                for segment in value.segments:
                    obj_list = list()
                    for atom in segment.atoms:
                        if len(atom.objects) > 0:
                            encoded_state[key][1].append(state[atom.name])
                            encoded_state["goal_" + key][1].append(state[atom.name])
                        for obj in atom.objects:
                            if obj.encoding_id not in obj_list:
                                obj_list.append(obj.encoding_id)
                                encoded_state[key][0].append(obj.encoding_id)
                                encoded_state["goal_" + key][0].append(obj.encoding_id)
                    for a in segment.alpha:
                        encoded_state[key][1].append(a)
                        encoded_state["goal_" + key][1].append(a)
                    k = segment.k_expr[0]
                    #for i in segment.k_expr[1]:
                    #    k = k.replace(i, str(state[i]))
                    #k = eval(k)
                    encoded_state[key][1].append(k)
                    encoded_state["goal_" + key][1].append(k)
        else:
            for segment in value.segments:    
                obj_list = list()
                for atom in segment.atoms:
                    if len(atom.objects) > 0:
                        encoded_state["goal_" + key][1].append(state[atom.name])
                    for obj in atom.objects:
                        if obj.encoding_id not in obj_list:
                            obj_list.append(obj.encoding_id)
                            encoded_state["goal_" + key][0].append(obj.encoding_id)
                            
                for a in segment.alpha:
                    encoded_state["goal_" + key][1].append(a)
                    
                k = segment.k_expr[0]
                #for i in segment.k_expr[1]:
                #    k = k.replace(i, str(state[i]))
                #k = eval(k)
                encoded_state["goal_" + key][1].append(k)

            
    return encoded_state


def extract_general_goals_objects(state,key,values,encoded_state):
    encoded_state.setdefault(key,[])
    encoded_state.setdefault("goal_" + key,[])
    for value in values:
        obj_list = list()
        if value.checkGoal(state):
                for segment in value.segments:
                    obj_list = list()
                    for atom in segment.atoms:

                        for obj in atom.objects:
                            if obj.encoding_id not in obj_list:
                                obj_list.append(obj.encoding_id)
                                encoded_state[key].append(obj.encoding_id)
                                encoded_state["goal_" + key].append(obj.encoding_id)
        else:
            for segment in value.segments:    
                obj_list = list()
                for atom in segment.atoms:
                    for obj in atom.objects:
                        if obj.encoding_id not in obj_list:
                            obj_list.append(obj.encoding_id)
                            encoded_state["goal_" + key].append(obj.encoding_id)
    return encoded_state