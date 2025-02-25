import numpy as np


def float_to_eng_string(f):
    """
    Convert a float to an engineering string
    """
    up = ["", "k", "M", "G", "T", "P", "E", "Z", "Y"]
    down = ["m", "µ", "n", "p", "f", "a", "z", "y"]

    if f == 0:
        return "0"

    degree = int(np.floor(np.log10(abs(f)) / 3))
    if degree > 0:
        value = f / 10 ** (3 * degree)
        unit = up[degree]
    else:
        value = f * 10 ** (-3 * degree)
        unit = down[-degree - 1]

    return f"{value:.2f} {unit}"
