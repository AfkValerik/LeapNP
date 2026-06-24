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

### Training a New Model
To train a new model, you can use the `train.py` script. The script uses command-line arguments to specify the training parameters.

### Basic Usage
- "--train" specifies the path to the training dataset.
- "--validation" specifies the path to the validation dataset.
- "--loss" specifies the loss function to use. Use "supervised_optimal", other configurations are not supported with the new code.
- "--resume" specifies the path to a checkpoint to resume training from. If not specified, training will start from scratch.
- "--domain_name" specifies the name of the domain. This is used to save the model and logs in a directory named after the domain, and to find the  file representing the domain in the dataset folders.

### Modes
There are two parameters that handles how the numeric parts of the domain is handled: "--numeric" and "--num_inputs". If both are set to False, the numeric parts of the domain are ignored and the model is trained on the boolean part only. If "--numeric" is set to True, numeric preconditions and goals are treated only as boolean conditions, without the associated numeric values. If  "--numeric" and "--num_inputs" are both set to True, the numeric values are used alongside the numeric conditions.

### Additional Arguments
- "--aggregation" specifies the aggregation function used in the GNN. Default is "add".
- "--size" specifies the embedding size to use in the GNN. Default is 60.
- "--iterations" specifies the number of iterations to use in the GNN. Default is 30.
- "--batch_size" specifies the batch size to use for training. Default is 64.
- "--max_epochs" specifies the number of epochs to train for. Default is 1000.
- "--learning_rate" specifies the learning rate to use for training. Default is 0.0002.
- "--patience" specifies the number of epochs to wait for improvement before stopping training. Default is 30.


