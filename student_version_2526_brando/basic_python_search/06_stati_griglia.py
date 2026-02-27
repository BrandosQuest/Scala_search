"""Base: piccoli mattoni da usare poi negli algoritmi su griglia.
"""


def neighbors4(state):
    """TODO 1: ritorna 4 vicini ortogonali."""
    raise NotImplementedError("TODO 1")


def valid_neighbors(state, w, h, walls):
    """TODO 2: usa neighbors4 + filtri in_bounds e not wall."""
    raise NotImplementedError("TODO 2")


def one_step_expand(frontier, reached, w, h, walls):
    """TODO 3: espandi una frontier (lista), ritorna next_frontier.
    Aggiorna reached con i nuovi stati.
    """
    raise NotImplementedError("TODO 3")


def _self_check():
    walls = {(1, 1)}
    v = valid_neighbors((1, 0), 4, 4, walls)
    assert set(v) == {(0, 0), (2, 0)}

    reached = {(0, 0)}
    nf = one_step_expand([(0, 0)], reached, 3, 3, set())
    assert set(nf) == {(1, 0), (0, 1)}
    assert set(nf).issubset(reached)

    print("06_stati_griglia: OK")


if __name__ == "__main__":
    _self_check()
