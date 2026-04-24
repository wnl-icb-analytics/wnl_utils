import matplotlib.pyplot as plt

_current_canvas = {"fig": None, "ax": None}


def plot_map_canvas(figsize=(12, 10)):
    """Creates a Matplotlib figure and axes for map plotting, stored as the current canvas.

    Args:
        figsize (tuple): Width and height of the figure in inches. Defaults to (12, 10).
    """
    fig, ax = plt.subplots(1, 1, figsize=figsize)
    ax.axis("off")
    _current_canvas["fig"] = fig
    _current_canvas["ax"] = ax


def get_map_canvas():
    """Returns the current fig and ax created by plot_map_canvas().

    Returns:
        tuple: (fig, ax)
    """
    return _current_canvas["fig"], _current_canvas["ax"]

