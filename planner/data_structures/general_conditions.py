from data_structures.extended_conditions import  checkIfNumeric, standardizeGoal, extractPreconditionRecursive, normalize_conditions
from data_structures.goals import Goal
import re
from fractions import Fraction

class AugmentedGoal(Goal):
    def __init__(self, goal_expr,atoms,bool_goal, segments,k ,kfluents):
        super().__init__(goal_expr,atoms,bool_goal)
        self.segments = segments
        self.k = k
        self.kfluents = kfluents
        
    def __eq__(self, other):
        if not isinstance(other, AugmentedGoal):
            return False
        return self.goal_expr == other.goal_expr

class Segments:
    def __init__(self, atoms,alpha):
        self.alpha = alpha
        self.atoms = atoms

def getGeneralGoalsMap(goals,objects,obj_encoding):
    augmented_goals_map = dict()
    for goal in goals:
        
        if not goal.bool_goal:
            conditions = extractNormalization(goal.goal_expr,objects)


            for atom in goal.atoms:
                atom.addObjectEncoding(obj_encoding)

                segments = list()
            for i in conditions[1][0]["segments"]:
                atoms = list()
                for j in goal.atoms:
                    if j.name in i["fluents"]:
                        atoms.append(j)
                segments.append(Segments(atoms,i["alpha"]))
            specialGoal = AugmentedGoal(goal.goal_expr,goal.atoms,goal.bool_goal,segments,conditions[1][0]["k"],conditions[1][0]["kfluents"])
            if conditions[0][0] not in augmented_goals_map:
                augmented_goals_map.setdefault(conditions[0][0],[])
            augmented_goals_map[conditions[0][0]].append(specialGoal)

            
    return augmented_goals_map

def getGeneralPreconditionsMap(actions,objects,obj_encoding):
    preconditions_map = dict()
    for action in actions:
        for precondition in action.preconditions:
            if not precondition.is_bool:
                conditions = extractNormalization(precondition.name,objects)
                for atom in precondition.atoms:
                    atom.addObjectEncoding(obj_encoding)
                segments = list()
                for i in conditions[1][0]["segments"]:
                    atoms = list()
                    for j in precondition.atoms:
                        if j.name in i["fluents"]:
                            atoms.append(j)
                    segments.append(Segments(atoms,i["alpha"]))
                specialPrecondition = AugmentedGoal(precondition.name,precondition.atoms,precondition.is_bool,segments,conditions[1][0]["k"],conditions[1][0]["kfluents"])
                if conditions[0][0] not in preconditions_map:
                    preconditions_map.setdefault(conditions[0][0],[])
                if specialPrecondition not in  preconditions_map[conditions[0][0]]:
                    preconditions_map[conditions[0][0]].append(specialPrecondition)
                    
    return preconditions_map


def extractNormalization(condition,parameters):

        cond_list = list()


        goals = extractGeneralCondition(condition)

        cond_list = generalize_condition(goals,parameters)

        out_list = (cond_list,goals)
        return out_list
  
def generalize_condition(conditions,parameters):
        new_conditions = list()
        sorted_parameters = sorted(parameters, key=lambda p: len(p.name), reverse=True)
        for condition in conditions:
            for segment in condition["segments"]:
                current_formula = segment['formula']
            
                for param in sorted_parameters:
                    p_name = param.name
                    p_type = param.type.name
                    
                    # Creiamo un pattern dinamico. 
                    # re.escape protegge la stringa se p_name contiene caratteri speciali
                    pattern = r'\b' + re.escape(p_name) + r'\b'
                    
                    # Sostituiamo tutte le occorrenze esatte di p_name con p_type
                    current_formula = re.sub(pattern, p_type, current_formula)
                
            # Salviamo la formula aggiornata
                current_formula = re.sub(r'(<=|>=|==|!=|<|>)\s*.*', r'\1 k', current_formula)
                new_conditions.append(current_formula)
        
        return new_conditions
def extractGeneralCondition(condition):
        FLIP_OPS = {
            '<=': '<=', '>=': '<=', '<': '<', '>': '<', '==': '==', '!=': '!='
        }

        # 1. Trova l'operatore
        op_match = re.search(r'(<=|>=|==|!=|<|>)', condition)
        if not op_match:
            return []
        
        raw_op = op_match.group(1)
        final_operator = FLIP_OPS.get(raw_op, raw_op)

        # 2. Splittiamo per trovare le variabili
        parts = condition.split(raw_op, 1)
        left_part = parts[0]
        right_part = parts[1] if len(parts) > 1 else ""

        # --- BLOCCO: ESTRAZIONE FLUENTI NORMALI ---
        # Aggiunto [+-]?\s* nel gruppo finale per supportare i moltiplicatori negativi a destra (es. * -1)
        pattern_fluents = r'([+-]?)\s*(?:(\d+(?:[./]\d+)?)\s*\*\s*)?(\w+)\(([^)]+)\)(?:\s*\*\s*([+-]?\s*\d+(?:[./]\d+)?))?'
        
        left_matches = re.findall(pattern_fluents, left_part)
        left_terms = []
        for sign, num_before, func, arg, num_after in left_matches:
            num = num_before or num_after or "1"
            # Aggiunto replace(' ', '') per tollerare spazi tra il meno e il numero (es. "- 1")
            val = float(Fraction(num.replace(' ', '')))
            if sign == '-': val = -val
            left_terms.append((val, f"{func}({arg})"))

        right_matches = re.findall(pattern_fluents, right_part)
        right_terms = []
        for sign, num_before, func, arg, num_after in right_matches:
            num = num_before or num_after or "1"
            val = float(Fraction(num.replace(' ', '')))
            if sign == '-': val = -val
            right_terms.append((-val, f"{func}({arg})"))

        terms = left_terms + right_terms

        # --- BLOCCO: ESTRAZIONE FLUENTI 0-ARY E COSTANTI EXTRA ---
        left_no_fluents = re.sub(pattern_fluents, ' ', left_part)
        right_no_fluents = re.sub(pattern_fluents, ' ', right_part)

        # Aggiunto [+-]?\s* anche qui per coerenza
        pattern_0ary = r'([+-]?)\s*(?:(\d+(?:[./]\d+)?)\s*\*\s*)?([a-zA-Z_]\w*)(?!\s*\()(?:\s*\*\s*([+-]?\s*\d+(?:[./]\d+)?))?'
        
        left_0ary_matches = re.findall(pattern_0ary, left_no_fluents)
        right_0ary_matches = re.findall(pattern_0ary, right_no_fluents)

        k_terms = []
        for sign, num_before, func, num_after in left_0ary_matches:
            num = num_before or num_after or "1"
            val = float(Fraction(num.replace(' ', '')))
            if sign == '-': val = -val
            k_terms.append((-val, func)) 

        for sign, num_before, func, num_after in right_0ary_matches:
            num = num_before or num_after or "1"
            val = float(Fraction(num.replace(' ', '')))
            if sign == '-': val = -val
            k_terms.append((val, func)) 

        left_only_consts = re.sub(pattern_0ary, ' ', left_no_fluents)
        right_only_consts = re.sub(pattern_0ary, ' ', right_no_fluents)

        const_pattern = r'[+-]?\s*\d+(?:[./]\d+)?'
        left_constants = re.findall(const_pattern, left_only_consts)
        right_constants = re.findall(const_pattern, right_only_consts)

        left_extra = sum(float(Fraction(c.replace(' ', ''))) for c in left_constants)
        right_extra = sum(float(Fraction(c.replace(' ', ''))) for c in right_constants)

        threshold = right_extra - left_extra

        # --- BLOCCO: INVERSIONE ALGEBRICA FINALE ---
        if final_operator != raw_op:
            terms = [(-c, v) for c, v in terms]
            k_terms = [(-c, f) for c, f in k_terms]
            threshold = -threshold

        terms = sorted(terms, key=lambda x: x[1])

        # --- BLOCCO: COSTRUZIONE K_STR E STRINGHE GLOBALI ---
        k_str = str(threshold)
        for c, f in k_terms:
            if c == 1.0:
                k_str += f" + {f}"
            elif c == -1.0:
                k_str += f" - {f}"
            elif c > 0:
                k_str += f" + {c} * {f}"
            else:
                k_str += f" - {abs(c)} * {f}"

        kfluents = list(set([f for c, f in k_terms]))
        final_k = k_str if kfluents else threshold
        
        # Fluenti globali (per la valutazione)
        global_fluents = [v for c, v in terms]
        
        # Costruiamo eval_formula
        lhs_parts = []
        for c, v in terms:
            if c == 1.0:
                lhs_parts.append(v)
            elif c == -1.0:
                lhs_parts.append(f"-{v}")
            else:
                lhs_parts.append(f"{c} * {v}")
        
        lhs_str = " + ".join(lhs_parts).replace("+ -", "- ") if lhs_parts else "0"
        eval_formula = f"{lhs_str} {final_operator} {k_str}"

        # --- BLOCCO: COSTRUZIONE DEI SEGMENTI ---
        segments = []
        if len(terms) == 1:
            c, v = terms[0]
            segments.append({
                "formula": f"{v} {final_operator} {k_str}",
                "alpha": [c],
                "fluents": [v]
            })
        elif len(terms) > 1:
            for i in range(len(terms) - 1):
                (c1, v1), (c2, v2) = terms[i], terms[i+1]
                segments.append({
                    "formula": f"{v1} + {v2} {final_operator} {k_str}",
                    "alpha": [c1, c2],
                    "fluents": [v1, v2]
                })

        extracted_relations = []
        if segments:
            extracted_relations.append({
                "eval_formula": eval_formula,
                "operator": final_operator,
                "k": final_k,
                "kfluents": kfluents,
                "fluents": global_fluents, # <--- I fluenti della formula intera
                "segments": segments       # <--- La lista delle coppie frammentate
            })
                
        return extracted_relations

def extract_general_goals_pairs(state,key,values,encoded_state):
    encoded_state.setdefault(key,[[],[]])
    encoded_state.setdefault("false_" + key,[[],[]])
    for value in values:
        obj_list = list()
        k = value.k
        kfluents = value.kfluents
        if kfluents:
            for kf in kfluents:
                if kf in state:
                    k = k.replace(kf, str(state[kf]))
            k = eval(k)
        #TODO: check if this stands with atoms without objects
        if value.checkGoal(state):
                for segment in value.segments:
                    obj_list = list()
                    for atom in segment.atoms:
                        if len(atom.objects) > 0:
                            encoded_state[key][1].append(state[atom.name])
                        for obj in atom.objects:
                            if obj.encoding_id not in obj_list:
                                obj_list.append(obj.encoding_id)
                                encoded_state[key][0].append(obj.encoding_id)
                    for a in segment.alpha:
                        encoded_state[key][1].append(a)
                    encoded_state[key][1].append(k)
        else:
            for segment in value.segments:    
                obj_list = list()
                for atom in segment.atoms:
                    if len(atom.objects) > 0:
                        encoded_state["false_" + key][1].append(state[atom.name])
                    for obj in atom.objects:
                        if obj.encoding_id not in obj_list:
                            obj_list.append(obj.encoding_id)
                            encoded_state["false_" + key][0].append(obj.encoding_id)
                            
                for a in segment.alpha:
                    encoded_state["false_" + key][1].append(a)
                encoded_state["false_" + key][1].append(k)

            
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