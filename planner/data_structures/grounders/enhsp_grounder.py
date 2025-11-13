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
from itertools import count
from typing import Callable, Set
from unified_planning.engines.compilers.utils import lift_action_instance
from functools import partial

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
            
    def ground_problem(self,domain,problem,objects,fluents,init_values):
        updomain =open(domain,"r").read()
        #base_command = ['java', '-jar', pkg_resources.resource_filename(__name__, 'ENHSP_GROUNDER/jpddlplus.jar'), '-o', domain, '-f', problem, '-gro', 'internal']
        base_command = ['java', '-jar', '/home/vborelli/planners/ENHSP_GROUNDER/jpddlplus.jar', '-o', domain, '-f', problem, '-gro', 'internal']
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
        for key in swap_objects:
            grounded_domain = grounded_domain.replace(key,swap_objects[key])
            grounded_instance = grounded_instance.replace(key,swap_objects[key])
        #for key in swap_fluents:
        for key in sorted(swap_fluents.keys(), key=lambda x: -len(x)):
            grounded_domain = grounded_domain.replace(key,swap_fluents[key])
            grounded_instance = grounded_instance.replace(key,swap_fluents[key])
        to_keep = grounded_domain.split("(:action")[1:]
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

        grounded_problem = PDDLReader().parse_problem_string(new_domain,grounded_instance)
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

        grounded_problem = self.ground_problem(pddl_domain,pddl_problem,problem.all_objects,problem.fluents,problem.explicit_initial_values)
        
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
        actions = grounded_problem.actions
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
        
        

