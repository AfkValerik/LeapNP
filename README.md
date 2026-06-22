This repository contains the LeapNP framework, which stands for *Learning and Planning Framework for Numeric Problems*. It is a lightweight framework fully implemented in python, that supports classical and numeric planning tasks, designed to ease the integration of deep learning methods.

You can run the framework using the `main.py` script. The script uses command-line arguments to specify the domain, problem, model, and various execution parameters.

### Basic Usage

To execute the script, you must provide at least the path to the domain file (`--o`) and the problem file (`--f`):

```bash
python main.py --o path/to/domain.pddl --f path/to/problem.pddl
```

To run the framework with GNN-based heuristics, you also have to specify the model path (`--model`):

```bash
python main.py --o path/to/domain.pddl --f path/to/problem.pddl --model path/to/model.ckpt
```
### Additional Arguments
- "--h" specifies the heuristic to use. Default is "gnnval", the gnn heuristic from the AAAI paper. The models trained are in the models directory, under the hn subdirectory. The models under hgeneral are meant to be used with the gnngeneral heuristic, but i recommend not using it since it is still under development and might be bugged. Currently there arent symbolic heuristics implemented.
- "--s" specifies the search algorithm to use. Default is "bfs". (Which is actually Greedy Best First Search).
- "--multiple_eval" is set to True, all successors are evaluated in a single batch, which can speed up the evaluation of the heuristic. Default is True. this should always be used with Gnn heuristics.
- "--seed" specifies the random seed to use for reproducibility. Default is 17.
- "--grounder" specifies the grounder to use. Default is "enhsp", all the grounders implemented in the unified planning framework should work, but they might generate some errors.