"""Base: set e membership O(1).

Obiettivo: usare set per reached/visited.
"""


def add_if_new(reached, state):
    """TODO 1: aggiungi state a reached solo se assente.
    Ritorna True se aggiunto, False altrimenti.
    """
    if state in reached:
        return False
    reached.add(state)
    return True

    #raise NotImplementedError("TODO 1")


def remove_walls(candidates, walls):
    """TODO 2: data lista candidates e set walls, ritorna lista senza muri."""
    for candidate in candidates:
        if candidate in walls:
            candidates.remove(candidate)
    return candidates
    raise NotImplementedError("TODO 2")


def unseen_only(candidates, reached):
    """TODO 3: ritorna lista di candidati non presenti in reached."""
    for candidate in candidates:
        if candidate in reached:
            candidates.remove(candidate)
    return candidates
    raise NotImplementedError("TODO 3")


def _self_check():
    reached = {(0, 0)}
    assert add_if_new(reached, (1, 0)) is True
    assert add_if_new(reached, (1, 0)) is False

    c = [(0, 1), (1, 1), (2, 1)]
    w = {(1, 1)}
    assert remove_walls(c, w) == [(0, 1), (2, 1)]

    assert unseen_only([(0, 0), (0, 2), (1, 0)], {(0, 0), (1, 1)}) == [(0, 2), (1, 0)]
    print("02_set_e_membership: OK")


if __name__ == "__main__":
    _self_check()
