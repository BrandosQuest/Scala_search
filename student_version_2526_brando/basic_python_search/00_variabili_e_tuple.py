"""Base: variabili, tuple, liste.

Obiettivo: imparare a rappresentare uno stato come (x, y).
"""


def make_state(x, y):
    """TODO 1: ritorna una tupla (x, y)."""
    return (x, y)
    raise NotImplementedError("TODO 1")


def move_east(state):
    """TODO 2: da (x, y) ritorna (x+1, y)."""
    return (state[0] + 1, state[1])
    raise NotImplementedError("TODO 2")


def states_to_string(states):
    """TODO 3: data lista di tuple, ritorna stringa 'x1,y1 | x2,y2 | ...'."""
    string = ""
    for state in states:
        string+= str(state[0]) + "," + str(state[1])+" | "
    return string[:len(string)-3]


    raise NotImplementedError("TODO 3")


def _self_check():
    s = make_state(2, 3)
    assert s == (2, 3)
    assert move_east(s) == (3, 3)
    out = states_to_string([(0, 0), (1, 2), (3, 4)])
    assert out == "0,0 | 1,2 | 3,4"
    print("00_variabili_e_tuple: OK")


if __name__ == "__main__":
    _self_check()
