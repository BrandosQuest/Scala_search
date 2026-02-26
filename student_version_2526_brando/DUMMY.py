from random import choice
from search_algorithm import SearchAlgorithm
from search_algorithm import Node


class Dummy(SearchAlgorithm):
    """Random memoryless search.

    At each step it picks one random applicable action from the current state.
    It does not keep a reached/visited set and stops only when the goal is found
    (or when no successors are available).
    """

    def __init__(self, view=False, max_steps=50000) -> None:
        self.max_steps = max_steps
        super().__init__(view)

    def solve(self, problem) -> list:
        self.reset_expanded()
        current = Node(problem.init)
        self.update_expanded(current.state)

        if problem.isGoal(current.state):
            return []

        steps = 0
        while steps < self.max_steps:
            successors = list(problem.getSuccessors(current.state))
            if not successors:
                return None

            action, next_state = choice(successors)
            current = Node(next_state, current, action, current.g + problem.cost.get(action, 1))
            self.update_expanded(current.state)

            if problem.isGoal(current.state):
                return self.extract_solution(current)

            steps += 1

        return None
