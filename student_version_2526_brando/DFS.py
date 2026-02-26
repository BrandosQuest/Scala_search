from search_algorithm import SearchAlgorithm
from queue import LifoQueue
from search_algorithm import Node
class DFS(SearchAlgorithm):
    """Depth First Search

    Args:
        Solver (_type_): This is an implementation for the Solver class
    """

    # Return a plan as a list of actions (e.g., ['N', 'E', ...]) from init to goal.
    # Return None if no solution is found.
    def solve(self, problem) -> list[str] | None:
        raise NotImplementedError("To be implemented")
