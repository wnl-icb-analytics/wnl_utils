import pytest
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from wnl_utils.mapkit.canvas import plot_map_canvas, get_map_canvas

def test_plot_map_canvas_creates_fig_and_ax():
    plot_map_canvas()
    fig, ax = get_map_canvas()
    assert isinstance(fig, plt.Figure)
    assert isinstance(ax, plt.Axes)
    plt.close("all")



