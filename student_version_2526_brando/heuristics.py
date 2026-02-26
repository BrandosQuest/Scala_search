"""Heuristic functions for A*.

Each heuristic must return a non-negative integer estimate of the
remaining cost from `start` to `goal`.
"""


# Return Manhattan distance between two grid states.
def manhattan(start: tuple[int, int], goal: tuple[int, int]) -> int:
    raise NotImplementedError("To be implemented")


# Return a blind heuristic value (always 0).
def blind(start: tuple[int, int], goal: tuple[int, int]) -> int:
    raise NotImplementedError("To be implemented")



#da modicicare