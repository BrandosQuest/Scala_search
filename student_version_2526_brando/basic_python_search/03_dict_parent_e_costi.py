"""Base: dizionari per parent map e cost map.

Obiettivo: ricostruzione percorso e aggiornamento costo migliore.
"""


def set_parent(parent, child, p):
    """TODO 1: salva parent[child] = p."""
    raise NotImplementedError("TODO 1")


def reconstruct(parent, goal):
    """TODO 2: ricostruisci path fino a parent None.
    Esempio: A<-B<-C (goal C) -> [A,B,C]
    """
    raise NotImplementedError("TODO 2")


def update_best_cost(g_best, node, new_cost):
    """TODO 3: aggiorna g_best[node] solo se costo migliore.
    Ritorna True se aggiornato, False altrimenti.
    """
    raise NotImplementedError("TODO 3")


def _self_check():
    parent = {"A": None}
    set_parent(parent, "B", "A")
    set_parent(parent, "C", "B")
    assert reconstruct(parent, "C") == ["A", "B", "C"]

    g = {"A": 0, "B": 5}
    assert update_best_cost(g, "B", 4) is True
    assert g["B"] == 4
    assert update_best_cost(g, "B", 7) is False
    assert update_best_cost(g, "C", 3) is True
    assert g["C"] == 3

    print("03_dict_parent_e_costi: OK")


if __name__ == "__main__":
    _self_check()
