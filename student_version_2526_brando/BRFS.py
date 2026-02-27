# from search_algorithm import SearchAlgorithm
# from queue import Queue
# from search_algorithm import Node
#
#
# class BrFS(SearchAlgorithm):
#     """Breath First Search
#
#     Args:
#         Solver (_type_): This is an implementation for the Solver class
#     """
#     # Return a plan as a list of actions (e.g., ['N', 'E', ...]) from init to goal.
#     # Return None if no solution is found.
#     def solve(self, problem) -> list[str] | None:
#         self.reset_expanded()
#         current = Node(problem.init)
#         self.update_expanded(current.state)
#
#         if problem.isGoal(current.state):
#             return []
#
#         frontier = Queue()
#         frontier.put(current)
#         explored = set()
#
#         counter = 0
#
#         while not frontier.empty():
#             current = frontier.get()
#             self.update_expanded(current.state)
#
#
#             successors = list(problem.getSuccessors(current.state))
#             # if not successors:
#             #     return None
#             print(counter)
#             counter += 1
#
#             for successor in successors:
#                 action, next_state = successor
#                 node = Node(next_state, current, action, next_state)
#                 if next_state not in self.expanded_states and not node in frontier.queue:#lo stato non il nodo
#                     if problem.isGoal(next_state):
#                         return self.extract_solution( node)
#                         #return self.extract_solution(current)
#                     #action, next_state = successor
#                     frontier.put(node)
#
#             # if problem.isGoal(current.state):
#             #     return self.extract_solution(current)
#         return None
#         raise NotImplementedError("To be implemented")
from search_algorithm import SearchAlgorithm
from queue import Queue
from search_algorithm import Node


class BrFS(SearchAlgorithm):
    """Breath First Search

    Args:
        Solver (type): This is an implementation for the Solver class
    """

    # Return a plan as a list of actions (e.g., ['N', 'E', ...]) from init to goal.
    # Return None if no solution is found.
    def solve(self, problem) -> list[str] | None:
        self.reset_expanded()
        current = Node(problem.init)
        self.update_expanded(current.state)

        if problem.isGoal(current.state):
            return []

        frontier = Queue()
        frontier.put(current)
        explored = {current.state}

        while not frontier.empty():
            current = frontier.get()
            self.update_expanded(current.state)

            successors = list(problem.getSuccessors(current.state))

            for successor in successors:
                action, next_state = successor
                nuovoNodo = Node(next_state, current, action, current.g + problem.cost.get(action, 1))

                if next_state not in explored and next_state not in frontier.queue:
                    if problem.isGoal(next_state):
                        return self.extract_solution(nuovoNodo)

                    explored.add(next_state)
                    frontier.put(nuovoNodo)

        return None