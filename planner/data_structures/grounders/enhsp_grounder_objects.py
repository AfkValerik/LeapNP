import os
import pkg_resources
import unified_planning as up
from unified_planning.engines import PlanGenerationResult, PlanGenerationResultStatus
from unified_planning.model import ProblemKind
from unified_planning.engines import PDDLPlanner, PDDLAnytimePlanner, Credits, LogMessage
from typing import Optional, List, Union, Iterator, IO
from unified_planning.engines.engine import Engine
from unified_planning.engines.mixins.compiler import CompilerMixin, CompilationKind
from unified_planning.model import FNode, Problem, ProblemKind, MinimizeActionCosts
from unified_planning.engines.results import CompilerResult
from unified_planning.io.pddl_reader import PDDLReader
from unified_planning.io.pddl_writer import PDDLWriter
from unified_planning.shortcuts import *
from unified_planning.engines.compilers.grounder import Grounder
from itertools import count, product
from typing import Callable, Set
from unified_planning.engines.compilers.utils import lift_action_instance
from functools import partial
import re

credits = Credits('ENHSP',
                  'Enrico Scala',
                  'enricos83@gmail.com',
                  'https://sites.google.com/view/enhsp/',
                  'GPL',
                  'Expressive Numeric Heuristic Search Planner.',
                  'ENHSP is a planner supporting (sub)optimal classical and numeric planning with linear and non-linear expressions.')


class ENHSPGrounder(Engine,CompilerMixin):
    def __init__(self):
        Engine.__init__(self)
        CompilerMixin.__init__(self,CompilationKind.GROUNDING)
        
        
        
    @property
    def name(self) -> str:
        return 'enhsp grounder'
    
    
    @staticmethod
    def supported_kind() -> 'ProblemKind':
        supported_kind = ProblemKind(version=2)
        supported_kind.set_problem_class('ACTION_BASED')
        supported_kind.set_typing('FLAT_TYPING')
        supported_kind.set_typing('HIERARCHICAL_TYPING')
        supported_kind.set_initial_state('UNDEFINED_INITIAL_NUMERIC')
        supported_kind.set_fluents_type("INT_FLUENTS")
        supported_kind.set_fluents_type("REAL_FLUENTS")
        supported_kind.set_conditions_kind('NEGATIVE_CONDITIONS')
        supported_kind.set_conditions_kind('DISJUNCTIVE_CONDITIONS')
        supported_kind.set_conditions_kind('EXISTENTIAL_CONDITIONS')
        supported_kind.set_conditions_kind('UNIVERSAL_CONDITIONS')
        supported_kind.set_conditions_kind('EQUALITIES')
        supported_kind.set_problem_type('SIMPLE_NUMERIC_PLANNING')
        supported_kind.set_problem_type('GENERAL_NUMERIC_PLANNING')
        supported_kind.set_effects_kind('INCREASE_EFFECTS')
        supported_kind.set_effects_kind('DECREASE_EFFECTS')
        supported_kind.set_effects_kind('FORALL_EFFECTS')
        supported_kind.set_effects_kind('CONDITIONAL_EFFECTS')
        supported_kind.set_effects_kind('STATIC_FLUENTS_IN_BOOLEAN_ASSIGNMENTS')
        supported_kind.set_effects_kind('STATIC_FLUENTS_IN_NUMERIC_ASSIGNMENTS')
        supported_kind.set_effects_kind('FLUENTS_IN_BOOLEAN_ASSIGNMENTS')
        supported_kind.set_effects_kind('FLUENTS_IN_NUMERIC_ASSIGNMENTS')
        supported_kind.set_quality_metrics("ACTIONS_COST")
        supported_kind.set_quality_metrics("PLAN_LENGTH")
        supported_kind.set_quality_metrics("FINAL_VALUE")
        supported_kind.set_actions_cost_kind("STATIC_FLUENTS_IN_ACTIONS_COST")
        supported_kind.set_actions_cost_kind("FLUENTS_IN_ACTIONS_COST")
        supported_kind.set_actions_cost_kind("INT_NUMBERS_IN_ACTIONS_COST")
        supported_kind.set_actions_cost_kind("REAL_NUMBERS_IN_ACTIONS_COST")
        return supported_kind

    @staticmethod
    def supports(problem_kind: 'ProblemKind') -> bool:
        return problem_kind <= ENHSPGrounder.supported_kind()

    @staticmethod
    def get_credits(**kwargs) -> Optional['Credits']:
        return credits

    @staticmethod
    def _slugify(name: str) -> str:
        slug = "".join(ch if ch.isalnum() else "-" for ch in str(name)).strip("-")
        return slug or "type"

    @staticmethod
    def _find_named_block(domain_text: str, block_name: str):
        block_header = f"(:{block_name}"
        block_start = domain_text.find(block_header)
        if block_start < 0:
            return None

        depth = 0
        for idx in range(block_start, len(domain_text)):
            char = domain_text[idx]
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
                if depth == 0:
                    return block_start, idx + 1
        return None

    def _inject_dummy_actions(self, domain_text: str, problem: Problem) -> str:
        user_types = problem.user_types
        if callable(user_types):
            user_types = user_types()
        user_types = [t for t in user_types if t.name not in {"object", "bool"}]
        if not user_types:
            return domain_text

        predicates = []
        actions = []
        for user_type in user_types:
            predicate_name = f"plannerdummy{self._slugify(user_type.name)}"
            action_name = f"plannerdummyactionfor{self._slugify(user_type.name)}"
            predicates.append(f"    ({predicate_name} ?x - {user_type.name})")
            actions.append(
                f"(:action {action_name}\n"
                f" :parameters (?x - {user_type.name})\n"
                f" :precondition (and)\n"
                f" :effect ({predicate_name} ?x)\n"
                f")"
            )

        predicates_block = self._find_named_block(domain_text, "predicates")
        if predicates_block is not None:
            block_start, block_end = predicates_block
            insert_at = block_end - 1
            inserted = "\n".join(predicates) + "\n"
            domain_text = domain_text[:insert_at] + inserted + domain_text[insert_at:]
        else:
            action_insert_at = domain_text.find("(:action")
            if action_insert_at < 0:
                return domain_text
            inserted = "(:predicates\n" + "\n".join(predicates) + "\n)\n"
            domain_text = domain_text[:action_insert_at] + inserted + domain_text[action_insert_at:]

        action_insert_at = domain_text.find("(:action")
        if action_insert_at >= 0:
            inserted_actions = "\n".join(actions) + "\n"
            domain_text = domain_text[:action_insert_at] + inserted_actions + domain_text[action_insert_at:]

        return domain_text

    def _expand_forall_conditions(self, domain_text: str, objects) -> str:
        def get_objects_by_type(type_name):
            return [o.name for o in objects if getattr(o.type, 'name', None) == type_name]

        pos = 0
        while True:
            match = re.search(r"\b[Ff]orall\s*\(", domain_text[pos:])
            if not match:
                break
            start = pos + match.start()
            while start > 0 and domain_text[start - 1].isspace():
                start -= 1
            if start > 0 and domain_text[start - 1] == "(":
                start -= 1
            depth = 0
            end = start
            while end < len(domain_text):
                if domain_text[end] == "(":
                    depth += 1
                elif domain_text[end] == ")":
                    depth -= 1
                    if depth == 0:
                        end += 1
                        break
                end += 1
            if depth != 0:
                break
            forall_text = domain_text[start:end]
            header_match = re.search(r"\b[Ff]orall\s*\(\s*([^)]+?)\s*\)\s*\(", forall_text)
            if not header_match:
                pos = end
                continue
            header = header_match.group(1)
            body = forall_text[header_match.end() - 1:-1].strip()
            variables = re.findall(r"\?([A-Za-z0-9_]+)\s*-\s*([A-Za-z0-9_]+)", header)
            if not variables:
                typed_vars = re.findall(r"([A-Za-z0-9_]+)\s*-\s*([A-Za-z0-9_]+)\s+([A-Za-z0-9_]+)", header)
                variables = [(var_name, type_name) for type_name, _, var_name in typed_vars]
            if not variables:
                replacement = "(and)"
            else:
                type_object_lists = []
                for _, type_name in variables:
                    type_object_lists.append(get_objects_by_type(type_name))
                if any(len(lst) == 0 for lst in type_object_lists):
                    replacement = "(and)"
                else:
                    instantiations = []
                    for combo in product(*type_object_lists):
                        instantiated_body = body
                        for (var_name, _), obj_name in zip(variables, combo):
                            instantiated_body = re.sub(rf"(?:\?)?{re.escape(var_name)}\b", obj_name, instantiated_body)
                        instantiations.append(instantiated_body)
                    replacement = "(and " + " ".join(instantiations) + ")" if len(instantiations) > 1 else instantiations[0]
            domain_text = domain_text[:start] + replacement + domain_text[end:]
            pos = start + len(replacement)
        return domain_text
    
    @staticmethod
    def supports_compilation(compilation_kind: CompilationKind) -> bool:
        return compilation_kind == CompilationKind.GROUNDING

    @staticmethod
    def resulting_problem_kind(
        problem_kind: ProblemKind, compilation_kind: Optional[CompilationKind] = None
    ) -> ProblemKind:
        return problem_kind.clone()
    
    def add_numeric_assignments(self):
        grounded_domain_file= open("domain.pddl","r")
        grounded_domain = grounded_domain_file.read()
        grounded_domain_file.close()
        assignments = grounded_domain.split("assign")[1:]
        used_func_names = set()
        new_funcs = list()
        for i in assignments:
            to_add = i.split(")")[0].replace(" ","")
            to_add = to_add + ")\n"
            if to_add not in used_func_names:
                new_funcs.append(to_add)
                used_func_names.add(to_add)
            
        first_func,after_func = grounded_domain.split("functions")
        new_file = first_func + "functions" + "".join(new_funcs) + after_func
        with open("domain.pddl","w") as f:
            f.write(new_file)

    @staticmethod
    def _flatten_preconditions(preconditions):
        flattened = []
        for precondition in preconditions:
            if precondition is None:
                continue
            if getattr(precondition, "is_and", lambda: False)():
                flattened.extend(ENHSPGrounder._flatten_preconditions(precondition.args))
            else:
                flattened.append(precondition)
        return flattened

    @staticmethod
    def _extract_declared_object_names(problem_path):
        try:
            with open(problem_path, "r") as problem_file:
                problem_text = problem_file.read()
        except OSError:
            return []

        objects_match = re.search(r"\(:objects\b(.*?)\)\s*\(:init", problem_text, re.S | re.I)
        if not objects_match:
            return []

        object_block = objects_match.group(1)
        names = []
        for match in re.finditer(r"([A-Za-z0-9_]+)\s*(?:-\s*[A-Za-z0-9_]+)?", object_block):
            token = match.group(1)
            if token.lower() in {"objects", "object"}:
                continue
            if token not in names:
                names.append(token)
        return names

    def _build_object_name_replacements(self, objects, problem_path=None):
        replacements = {}
        declared_names = self._extract_declared_object_names(problem_path) if problem_path else []
        ordered_names = declared_names or [obj.name for obj in objects]
        existing_names = set(ordered_names)
        for obj in objects:
            if "_" in obj.name:
                replacements[obj.name.replace("_", " ")] = obj.name
        used_placeholders = set(replacements.keys())
        for index, obj_name in enumerate(ordered_names):
            placeholder = chr(ord("a") + index)
            if placeholder in existing_names or placeholder in used_placeholders:
                continue
            replacements[placeholder] = obj_name
            used_placeholders.add(placeholder)
        return replacements

    @staticmethod
    def _replace_tokens(text, replacements):
        for key, value in sorted(replacements.items(), key=lambda item: -len(item[0])):
            pattern = re.compile(rf"(?<![A-Za-z0-9_]){re.escape(key)}(?![A-Za-z0-9_])")
            text = pattern.sub(value, text)
        return text
            
    def ground_problem(self,domain,problem,objects,fluents,init_values,base_domain_path=None):
        updomain = open(base_domain_path or domain,"r").read()
        #base_command = ['java', '-jar', pkg_resources.resource_filename(__name__, 'ENHSP_GROUNDER/jpddlplus.jar'), '-o', domain, '-f', problem, '-gro', 'internal']
        base_command = ['java', '-jar', '/home/vborelli/LeapNP/planner/data_structures/grounders/ENHSP_GROUNDER/jpddlplus.jar', '-o', domain, '-f', problem, '-gro', 'internal']
        out = " ".join(map(str,base_command))
        os.system(out)
        #self.add_numeric_assignments()
        grounded_domain_file= open(domain,"r")
        grounded_domain = grounded_domain_file.read()
        swapping = dict()
        swap_objects = dict()
        swap_fluents = dict()
        for i in objects:
            if "_" in i.name:
                swap_objects[i.name.replace("_"," ")] = i.name

        object_name_replacements = self._build_object_name_replacements(objects, problem)
                
        for i in fluents:
            if "_" in i.name:
                swap_fluents[i.name.replace("_"," ")] = i.name
       
        for i in init_values:
        
                old_pred = "(" + str(i).replace("(","_").replace(")","").replace(",","_").replace(" ","") + ")"
                new_pred = old_pred.replace(" ","").replace("__","* ").replace("_"," ").replace("*","_")
                swapping[old_pred] = new_pred

                
        grounded_problem_file= open(problem,"r")
        grounded_instance = grounded_problem_file.read()
        for key in swapping:
            grounded_domain = grounded_domain.replace(key,swapping[key])
            grounded_instance = grounded_instance.replace(key,swapping[key])
        grounded_domain = self._replace_tokens(grounded_domain, swap_objects)
        grounded_instance = self._replace_tokens(grounded_instance, swap_objects)
        grounded_domain = self._replace_tokens(grounded_domain, object_name_replacements)
        grounded_instance = self._replace_tokens(grounded_instance, object_name_replacements)
        #for key in swap_fluents:
        grounded_domain = self._replace_tokens(grounded_domain, swap_fluents)
        grounded_instance = self._replace_tokens(grounded_instance, swap_fluents)
        to_keep = []
        for action_block in grounded_domain.split("(:action")[1:]:
            if "plannerdummyactionfor" in action_block:
                continue
            to_keep.append(action_block)
        #to_keep[-1] = to_keep[-1]
        new_domain = updomain.split("(:action")[0] 
        for i in to_keep:
            action_name,actionparams = i.split(":parameters")
            action_name = action_name.replace("__","_")
            new_domain = new_domain + "(:action" + action_name + ":parameters" + actionparams
            
        #new_domain = new_domain + ")"
        if "constants" in new_domain:
            before,after = new_domain.split("(:constants")
            _,after = new_domain.split("(:predicates")
        elif "predicates" in new_domain:
            before,after = new_domain.split("(:predicates")
        else:
            before,after = new_domain.split("(:functions")
        before = before + "(:constants\n"
        for i in objects:
            before = before +"\t" + i.name + " - " + i.type.name + "\n"
        if "predicates" in new_domain:
            new_domain = before + ")\n(:predicates" + after
        else:
            new_domain = before + ")\n(:functions" + after
            
        before,after = grounded_instance.split("(:objects")
        _,after = after.split("(:init")
        grounded_instance = before + "(:objects\n ) \n (:init\n" +  after
       # with open(domain,"w") as f:
       #     f.write(new_domain)
       # with open(problem,"w") as f:
       #     f.write(grounded_instance)

        new_domain = self._expand_forall_conditions(new_domain, objects)
        grounded_problem = PDDLReader().parse_problem_string(new_domain,grounded_instance)
        for action in grounded_problem.actions:
            flattened_preconditions = self._flatten_preconditions(action.preconditions)
            action.clear_preconditions()
            for precondition in flattened_preconditions:
                action.add_precondition(precondition)
        return grounded_problem
    
   #currently not used
    def _get_fnode(
        self,
        fact,
        problem: "up.model.AbstractProblem",
        get_item_named: Callable[
            [str],
            Union[
                "up.model.Type",
                "up.model.Action",
                "up.model.Fluent",
                "up.model.Object",
                "up.model.Parameter",
                "up.model.Variable",
            ],
        ],
    ) -> FNode:
        """Translates a Fast Downward fact back into a FNode."""
        exp_manager = problem.environment.expression_manager
        fluent = get_item_named(fact)
        args = [problem.object(o) for o in fact.args]
        fnode = exp_manager.FluentExp(fluent, args)
        if fact.negated:
            return exp_manager.Not(fnode)
        else:
            return fnode

    def _compile(self, problem: "up.model.AbstractProblem", compilation_kind: "CompilationKind") -> CompilerResult:
        assert isinstance(problem, Problem)
        #TODO: change as soon as the executable for enhsp grounder works correctly in saving the files
        #pddl_domain = "domain" + problem.name + ".pddl"
        #pddl_problem = "problem" + problem.name + ".pddl"
        pddl_domain = "domain.pddl"
        pddl_problem = "problem.pddl"
        writer = up.io.PDDLWriter(problem)
        writer.write_domain(pddl_domain)
        writer.write_problem(pddl_problem)

        with open(pddl_domain, "r") as domain_file:
            domain_text = domain_file.read()
        augmented_domain_text = self._inject_dummy_actions(domain_text, problem)
        augmented_domain_path = f"{pddl_domain}.grounded.pddl"
        with open(augmented_domain_path, "w") as domain_file:
            domain_file.write(augmented_domain_text)

        grounded_problem = self.ground_problem(augmented_domain_path,pddl_problem,problem.all_objects,problem.fluents,problem.explicit_initial_values,base_domain_path=pddl_domain)
        
        new_problem = problem.clone()
        new_problem.name = f"{self.name}_{problem.name}"
        new_problem.clear_actions()

        trace_back_map = dict()
        
        def fnode(fact, get_item_named: Callable[
            [str],
            Union[
                "up.model.Type",
                "up.model.Action",
                "up.model.Fluent",
                "up.model.Object",
                "up.model.Parameter",
                "up.model.Variable",
            ],
        ]):
            return self._get_fnode(fact, problem, get_item_named)
        actions = [a for a in grounded_problem.actions if not a.name.startswith("plannerdummyactionfor")]
        for a in actions:
            new_problem.add_action(a)
            actual_params = list()
            params = a.name.split("_")
            action_name = a.name
            for p in params:
                for o in new_problem.all_objects:
                    if p == o.name:
                        actual_params.append(o)
                        action_name = action_name.replace(p,"")
                        break
            action_name = action_name.rstrip("_ ")
            for act in problem.actions:
                if (act.name == action_name) or (act.name == action_name.replace("_","-")):
                    up_params = tuple(o for o in actual_params)
                    trace_back_map[a] = (act,up_params)
                    break
            
            

        mbai = partial(lift_action_instance, map=trace_back_map)

        return CompilerResult(
            new_problem,
            mbai,
            self.name,
        )
        
        

