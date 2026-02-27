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
        if problem.isGoal(Node(problem.init)):
            return []

        while True:
            for state in self.expanded_sequence
                if state not in self.expanded_states:
                    self.expanded_states.add(state)
            self.update_expanded(Node(problem.init))
        raise NotImplementedError("To be implemented")
