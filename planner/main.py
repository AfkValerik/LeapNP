import argparse 
from pathlib import Path
import torch
import time
from data_structures import get_problem, get_grounded_problem
from npg import setup_problem

def _parse_arguments():
    parser = argparse.ArgumentParser()

    # default values for arguments

    default_gpus = 1
    default_h = "gnnval"
    default_s = "bfs"
    default_aggregation = 'add'
    default_multiple_eval = True
    default_heuristic_weight = 1
    default_grounder = "enhsp"
    default_seed = 17
    # required arguments or --resume that requires a path
    parser.add_argument('--o', required=True, type=str, help='path to domain file')
    parser.add_argument('--f', required=True, type=str, help='path to problem file')
    parser.add_argument('--model', default=None, type=Path, help='path to model (.ckpt)')
    
    # arguments with meaningful default values
    parser.add_argument('--seed', default=default_seed, type=int, help='random seed (default=17)')
    parser.add_argument('--grounder',default = default_grounder, type = str, help = f'grounder to use (default={default_grounder})')
    parser.add_argument('--multiple_eval', default=default_multiple_eval, type=bool, help=f'use multiple evaluations (default={default_multiple_eval})')
    parser.add_argument('--w',default = default_heuristic_weight, type = float, help = f'heuristic weight, only for WAstar (default={default_heuristic_weight})')
    parser.add_argument('--gpus', default=default_gpus, type=int, help=f'number of GPUs to use (default={default_gpus})')
    parser.add_argument('--h', default=default_h, type=str, help=f'heuristic to use (default={default_h})')
    parser.add_argument('--s', default=default_s, type=str, help=f'search algorithm to use (default={default_s})')
    parser.add_argument('--aggregation', default=default_aggregation, nargs='?', choices=['add', 'max', 'addmax', 'smoothmax','mean'], help=f'aggregation function for readout (default={default_aggregation})')
    parser.add_argument('--readout', action='store_true', help='use global readout')
    
    args = parser.parse_args()
    return args

def _process_args(args):
    if args.gpus > 0:
        if not torch.cuda.is_available(): args.gpus = 0  # Ignore GPUs if there is no CUDA capable device.
            

def _main(args):
    _process_args(args)
    problem = get_problem(args.o, args.f)
    start = time.time()
    groundedProblem = get_grounded_problem(problem,args.grounder)
    end = time.time()
    print("grounding done, time: ", (end - start))
    if args.multiple_eval:
        print("multiple evaluation enabled")
    else:
        print("multiple evaluation disabled")
    path,goal,expanded,evaluated,length = setup_problem(args.o,problem,groundedProblem,args.s,args.h,args.model,args.gpus,args.aggregation,args.readout,args.multiple_eval,args.w,args.seed)
    print("goal found:", goal)
    print("\n expanded nodes:", expanded)
    print("\n evaluated nodes:", evaluated)
    print("\n path to goal:\n", path)
    print("\n Plan-length:", length)
    
    
   

if __name__ == "__main__":
    args = _parse_arguments()
    _main(args)