"""Base: cicli for, if, filtro elementi.

Obiettivo: filtrare stati validi con condizioni semplici.
"""


def only_even_x(states):
    """TODO 1: ritorna solo gli stati con x pari."""
    for state in states:
        if state[0] % 2 != 0:
            states.remove(state)
    return states
    raise NotImplementedError("TODO 1")


def in_bounds(states, w, h):
    """TODO 2: ritorna solo stati dentro griglia [0,w) x [0,h)."""
    for state in states:
        if state[0]<0 or state[0]>=w or state[1]<0 or state[1]>=h:
            states.remove(state)
    return states
    raise NotImplementedError("TODO 2")


def count_goal_hits(states, goal):
    """TODO 3: conta quante volte 'goal' appare in states."""
    counter = 0
    for state in states:
        if state==goal:
            counter += 1
    return counter
    raise NotImplementedError("TODO 3")


def _self_check():
    s = [(0, 0), (1, 1), (2, 2), (3, 0)]
    assert only_even_x(s) == [(0, 0), (2, 2)]
    assert in_bounds([(-1, 0), (0, 0), (3, 3), (4, 1)], 4, 4) == [(0, 0), (3, 3)]
    assert count_goal_hits([(1, 1), (2, 2), (1, 1)], (1, 1)) == 2
    print("01_cicli_e_filtri: OK")


if __name__ == "__main__":
    _self_check()
