"""Base: priority queue con queue.PriorityQueue.

Obiettivo: capire estrazione per priorita minima.
"""

from queue import PriorityQueue


def push_all(items_with_priority):
    """TODO 1: crea PriorityQueue e inserisci tuple (priority, item)."""
    raise NotImplementedError("TODO 1")


def pop_all_ordered(pq):
    """TODO 2: estrai tutto in ordine e ritorna solo item."""
    raise NotImplementedError("TODO 2")


def best_first(items_with_priority):
    """TODO 3: helper che combina TODO1+TODO2."""
    raise NotImplementedError("TODO 3")


def _self_check():
    data = [(5, "E"), (2, "B"), (4, "D"), (1, "A"), (3, "C")]
    pq = push_all(data)
    assert pop_all_ordered(pq) == ["A", "B", "C", "D", "E"]
    assert best_first(data) == ["A", "B", "C", "D", "E"]
    print("05_priority_queue_pratica: OK")


if __name__ == "__main__":
    _self_check()
