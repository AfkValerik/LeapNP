from unified_planning.io.pddl_reader import PDDLReader
from unified_planning.engines.compilers.grounder import Grounder
from data_structures.grounders import ENHSPGrounder

def get_problem(domain_file: str, problem_file: str):
    reader = PDDLReader()
    problem = reader.parse_problem(domain_file, problem_file)
    return problem



def get_grounded_problem(problem,grounderName = ""):
    if grounderName == "enhsp":
        grounder = ENHSPGrounder()
    else:
        grounder = Grounder()
    groundedProblem = grounder.compile(problem=problem)

    return groundedProblem
    




