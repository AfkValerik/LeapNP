from search_algorithms.SearchAlgorithm import SearchAlgorithm
from queue import PriorityQueue
from data_structures import State, CostState

class IWDBFSState(State):
    def __init__(self, values, g = 0, h = 0, parent = None, action = None) -> None:
        super().__init__(values, g, h, parent, action)
    
    def _cmp_key(self):
        return (self.h,self.g)  
    
    def __eq__(self, other):
        return self._cmp_key() == other._cmp_key()
    
    def __lt__(self,other):
        return self._cmp_key() < other._cmp_key()
    
    def __hash__(self):
        return hash(self.id)
    
    def __neighbors__ (self, actions):
        neighbors = list()
        for action in actions:
            if action.checkPreconditions(self.values):
                new_values = self.values.copy()
                action.applyEffects(new_values)
                neighbors.append(IWDBFSState(new_values,self.g + 1, 0, self.id, action))
        return neighbors
    
    
class IWDBFS(SearchAlgorithm):
    """Best First Search

    Args:
        heuristic, weight, the weight is not used for BFS, use  WAStar for that
        
        version with deferred evaluation to speed up GNN-based heuristics, slower for classical heuristics, might lead to memory issues with large problems
    """
    def __init__(self, heuristic = lambda x,y : 0, w = 1) -> None:
        super().__init__()
        self.heuristic = heuristic
        self.w = w
        

    def solve(self, problem, memory_limit = 8000) -> list:
        cost = dict()
        frontier = PriorityQueue()
        n = IWDBFSState(problem.init)
        mem1, basemem = self.heuristic.__calculate_state_memory_usage__(n)
        depth = 1
        
        frontier.put(n)
        #TODO: change values inside state to a list in order to use the cost dict correctly
        cost[str(n.id)] = CostState(n.g)
        #cost[problem.init] = 0
        self.reset_expanded()
        self.reset_states_evaluated()
        n = frontier.get()
        self.update_expanded()
        self.update_states_evaluated()
        if (problem.isGoal(n)):
            return self.extract_solution(n,cost)
        toEvaluate = list()
        for s in problem.getSuccessors(n):
            if str(s.id) not in cost or s.g < cost[str(s.id)].g:
                toEvaluate.append(s)
                cost[str(s.id)] = CostState(s.g,s.parent,s.action.name)
        
        mem2, numstates = self.heuristic.__calculate_states_memory_usage__(toEvaluate)
        mem2 = mem2 - basemem
        mem = (mem2 - mem1)/(numstates - 1)
        bf = len(problem.actions)
        print("currently running with depth: ", depth)
        print(f"Estimated memory usage for inference operations: {mem*bf:.2f} MB") 
        expanded_count_d1 = 0
        actual_successors = 0
        for t in toEvaluate:
            t.__updatef__()
            self.update_states_evaluated()

            if (problem.isGoal(t)):
                return self.extract_solution(t,cost)
            frontier.put(t)
            
        besth = 1000000
        #main loop
        #local_minima = 0
        while (not frontier.empty()):
                n = frontier.get()
                if n.h < besth:
                    besth = n.h
                    local_minima = 0
                else:
                    #let's try to introduce a depth increase when we are in local minima instead changing it instantly when the h does not improve
                    if local_minima > 5:
                        local_minima = 0
                        if depth == 1:
                            bf = actual_successors / expanded_count_d1
                            print("average branching factor calculated at depth 1: ", bf)
                        if mem * (bf**(depth + 1)) < memory_limit:
                            depth += 1
                            print("increasing depth to: ", depth)
                            print(f"Estimated memory usage for inference operations: {mem*(bf**depth):.2f} MB") 
                    else:
                        local_minima += 1
                
            #TODO: understand why this is here
            #if cost[n.state] == n.g:
                self.update_expanded()
                toEvaluate = list()
                successors = problem.getSuccessors(n)
                for s in successors:
                    if str(s.id) not in cost or s.g < cost[str(s.id)].g:
                        toEvaluate.append(s)
                        cost[str(s.id)] = CostState(s.g,s.parent,s.action.name)
                        if (problem.isGoal(s)):
                            return self.extract_solution(s,cost)
                if depth == 1:
                    expanded_count_d1 += 1
                    actual_successors += len(successors)
                else:
                    toEvaluate, check = self.deferred_evaluation(problem,toEvaluate,cost,depth)
                    if check:
                        return self.extract_solution(toEvaluate,cost)
                if len(toEvaluate) > 0:
                    self.heuristic.__valuateStates__(toEvaluate)
                    for t in toEvaluate:
                        t.__updatef__()
                        self.update_states_evaluated()
                        frontier.put(t)
        return None


    def deferred_evaluation(self, problem, toEvaluate, cost, depth):
        current_frontier = list(toEvaluate)

        # Eseguiamo il ciclo depth - 1 volte
        for i in range(depth - 1):
            next_frontier = []
            all_nodes = []
            for t in current_frontier:
                for s in problem.getSuccessors(t):
                    if str(s.id) not in cost or s.g < cost[str(s.id)].g:
                        
                        all_nodes.append(s)
                        next_frontier.append(s)
                        
                        cost[str(s.id)] = CostState(s.g, s.parent, s.action.name)
                        if problem.isGoal(s):
                            return s, True
            # Se non abbiamo generato nuovi nodi, interrompiamo il ciclo per efficienza
            if not next_frontier:
                break
                
            # Passo Cruciale:
            # I nodi da espandere al prossimo giro diventano i figli appena trovati
            current_frontier = next_frontier

        return list(all_nodes), False
    
