"""Base: FIFO e LIFO senza algoritmo completo.

Obiettivo: capire il comportamento diverso delle due frontiere.
"""

from collections import deque


def fifo_process(items):
    """TODO 1: usa deque e ritorna ordine di uscita FIFO."""
    raise NotImplementedError("TODO 1")


def lifo_process(items):
    """TODO 2: usa list come stack e ritorna ordine di uscita LIFO."""
    raise NotImplementedError("TODO 2")


def push_neighbors_lifo(stack, neighbors):
    """TODO 3: pusha i neighbors in ordine inverso per visita stabile.
    Ritorna stack aggiornato.
    """
    raise NotImplementedError("TODO 3")


def _self_check():
    assert fifo_process([1, 2, 3, 4]) == [1, 2, 3, 4]
    assert lifo_process([1, 2, 3, 4]) == [4, 3, 2, 1]

    st = ["A"]
    out = push_neighbors_lifo(st, ["B", "C", "D"])
    assert out[-1] == "B"
    print("04_fifo_lifo_pratica: OK")


if __name__ == "__main__":
    _self_check()
