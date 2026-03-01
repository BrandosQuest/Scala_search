from search_algorithm import SearchAlgorithm
from queue import Queue
from search_algorithm import Node


class BrFS(SearchAlgorithm):
    """Breath First Search

    Args:
        Solver (_type_): This is an implementation for the Solver class
    """
    # Return a plan as a list of actions (e.g., ['N', 'E', ...]) from init to goal.
    # Return None if no solution is found.
    def solve(self, problem) -> list[str] | None:
        self.reset_expanded() #quando chiamiamo questi metodi del prof nel codice è per fare si che il rendering grazico funzioni correttamente, non sono necessari per giungere alla soluzione
        current = Node(problem.init) #creiamo il nodo per poter utilizzare self.extract_solution(current), che prende un nodo
        self.update_expanded(current.state) #quando chiamiamo questi metodi del prof nel codice è per fare si che il rendering grazico funzioni correttamente, non sono necessari per giungere alla soluzione
        if problem.isGoal(current.state):#primo controllo
            return self.extract_solution(current)

        frontier_nodes = Queue() #necessarie entambe per avere fifo e un modo veloce di controllare la frontiera (set is hashtable o(1))
        frontier_states_set = set()#necessarie entambe per avere fifo e un modo veloce di controllare la frontiera (set is hashtable o(1))
        explored_states = set()#stati esplorati
        frontier_nodes.put(current)
        frontier_states_set.add(current.state)

        while not frontier_nodes.empty():
            current = frontier_nodes.get()#pop from the list
            frontier_states_set.remove(current.state)
            explored_states.add(current.state)#add to set

            successors = list(problem.getSuccessors(current.state))#returns list of (action, state)
            for successor in successors:
                action, next_state = successor#unpack the tuple
                child = Node(next_state, current, action, current.g + problem.cost.get(action, 1))#create the node
                if child.state not in explored_states and child.state not in frontier_states_set:#here we use the frontier_states_set for fast lookup
                    if problem.isGoal(child.state): #controllo
                        return self.extract_solution(child)
                    frontier_nodes.put(child)#add to the list
                    frontier_states_set.add(child.state)
            self.update_expanded(current.state)#per motivi grafici

        return None

    """
    Why
    the
    Performance is Different
    The
    difference
    comes
    down
    to
    how
    these
    data
    structures
    are
    built
    under
    the
    hood:

    Sets(item_set): In
    Python, a
    set is implemented as a
    Hash
    Table.When
    you
    ask if item not in item_set, Python
    runs
    a
    mathematical
    function(a
    hash) on
    the
    item
    to
    immediately
    calculate
    its
    exact
    memory
    location.It
    looks
    there
    instantly.This
    means
    membership
    testing
    takes
    O(1)(constant
    time).It
    takes
    the
    same
    amount
    of
    time
    whether
    your
    set
    has
    10
    items or 10
    million
    items.

    Queues(item_queue): The
    standard
    Python
    queue(collections.deque, queue.Queue, or a
    simple
    list) is built as an
    array or a
    doubly - linked
    list.To
    answer if item not in item_queue, Python
    has
    no
    shortcut.It
    must
    start
    at
    the
    front
    of
    the
    queue and check
    every
    single
    item
    one
    by
    one
    until
    it
    finds
    a
    match or reaches
    the
    end(a
    Linear
    Search).This
    takes
    O(n)(linear
    time).If
    your
    queue
    grows
    to
    10
    million
    items, the
    search
    takes
    10
    million
    times
    longer.
    """