from search_algorithm import SearchAlgorithm
from queue import PriorityQueue
from search_algorithm import Node

class AstarNode(Node):
    def __init__(self, state, parent = None, action = None, g = 0, h = 0) -> None:
        self.h = h
        super().__init__(state, parent, action, g)
        
    def __lt__(self, other):
        return self.g + self.h < other.g + other.h 
    
class AStar(SearchAlgorithm):
    """AStar First Search

    Args:
        Solver (_type_): This is an implementation for the Solver class
    """
    # `heuristic` is a function h(state, goal) -> estimated remaining cost.
    # Default: `lambda x, y: 0` (blind heuristic), so A* behaves like uniform-cost search.
    def __init__(self, heuristic = lambda x,y : 0, view = False, w = 1) -> None:
        self.heuristic = heuristic
        self.w = w
        super().__init__(view)

    # Return a plan as a list of actions (e.g., ['N', 'E', ...]) from init to goal.
    # Return None if no solution is found.
    def solve(self, problem) -> list[str] | None:
        self.reset_expanded()  # quando chiamiamo questi metodi del prof nel codice è per fare si che il rendering grazico funzioni correttamente, non sono necessari per giungere alla soluzione
        current = Node(problem.init)  # creiamo il nodo per poter utilizzare self.extract_solution(current), che prende un nodo
        self.update_expanded(current.state)  # quando chiamiamo questi metodi del prof nel codice è per fare si che il rendering grazico funzioni correttamente, non sono necessari per giungere alla soluzione
        if problem.isGoal(current.state):  # primo controllo
            return self.extract_solution(current)

        frontier_nodes = PriorityQueue()  # necessarie entambe per avere Lifo e un modo veloce di controllare la frontiera (set is hashtable o(1))
        frontier_states_set = set()  # necessarie entambe per avere Lifo e un modo veloce di controllare la frontiera (set is hashtable o(1))
        explored_states = set()  # stati esplorati
        frontier_nodes.put((0, current))
        frontier_states_set.add(current.state)

        while not frontier_nodes.empty():
            current = frontier_nodes.get()[1]  # pop from the list
            frontier_states_set.remove(current.state)
            explored_states.add(current.state)  # add to set

            successors = list(problem.getSuccessors(current.state))  # returns list of (action, state)
            for successor in successors:
                action, next_state = successor  # unpack the tuple
                # child = Node(next_state, current, action, current.g + problem.cost.get(action, 1))  # create the node
                child = Node(next_state, current, action, current.g + 1)  # create the node
                childH=abs(problem.goal[0]-next_state[0])+abs(problem.goal[1]-next_state[1])
                childF=childH+child.g
                if child.state not in explored_states and child.state not in frontier_states_set:  # here we use the frontier_states_set for fast lookup
                    if problem.isGoal(child.state):  # controllo
                        return self.extract_solution(child)
                    frontier_nodes.put(child)  # add to the list
                    frontier_states_set.add(child.state)
            self.update_expanded(current.state)  # per motivi grafici

        return None
        raise NotImplementedError("To be implemented")
