# tests/test_boundaries.py

import pytest
import geopandas as gpd
from matplotlib.axes import Axes
import matplotlib.pyplot as plt
from wnl_utils.mapkit.boundaries import plot_static_boundaries, plot_wnl_boroughs_base


@pytest.fixture
def boundary_gdf(valid_polygon):
    """Minimal GeoDataFrame with geometry and AREA_NAME, mimicking real boundary data."""
    return gpd.GeoDataFrame(
        {"AREA_NAME": ["Test Borough"]},
        geometry=[valid_polygon],
        crs="EPSG:4326"
    )


def test_plot_static_boundaries_returns_axes(boundary_gdf):
    fig, ax = plt.subplots()
    result = plot_static_boundaries(boundary_gdf, ax=ax)
    assert isinstance(result, Axes)
    plt.close("all")


def test_plot_static_boundaries_with_labels_runs(boundary_gdf):
    fig, ax = plt.subplots()
    result = plot_static_boundaries(boundary_gdf, ax=ax, labels=True)
    assert isinstance(result, Axes)
    plt.close("all")


def test_plot_wnl_boroughs_base_plain_fillstyle_runs(boundary_gdf):
    fig, ax = plt.subplots()
    result = plot_wnl_boroughs_base(boundary_gdf, ax=ax, fillstyle="plain")
    assert isinstance(result, Axes)
    plt.close("all")


def test_plot_wnl_boroughs_base_invalid_fillstyle_raises(boundary_gdf):
    fig, ax = plt.subplots()
    with pytest.raises(ValueError, match="fillstyle"):
        plot_wnl_boroughs_base(boundary_gdf, ax=ax, fillstyle="invalid")
    plt.close("all")

