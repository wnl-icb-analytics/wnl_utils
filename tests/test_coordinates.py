# tests/test_coordinates.py

import pytest
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from shapely.geometry import Point
from wnl_utils.mapkit.coordinates import plot_static_coordinates


@pytest.fixture
def point_gdf():
    """Minimal GeoDataFrame with point geometries and a label column."""
    return gpd.GeoDataFrame(
        {"LOCATION_NAME": ["Test Point"]},
        geometry=[Point(0.5, 0.5)],
        crs="EPSG:4326"
    )


def test_plot_static_coordinates_runs_with_default_style(point_gdf):
    fig, ax = plt.subplots()
    result = plot_static_coordinates(point_gdf, ax=ax)
    assert isinstance(result, Axes)
    plt.close("all")


def test_plot_static_coordinates_with_labels_raises_without_label_column(point_gdf):
    fig, ax = plt.subplots()
    with pytest.raises(ValueError, match="label_column must be provided"):
        plot_static_coordinates(point_gdf, ax=ax, labels=True)
    plt.close("all")


def test_plot_static_coordinates_with_labels_runs_when_column_present(point_gdf):
    fig, ax = plt.subplots()
    result = plot_static_coordinates(point_gdf, ax=ax, labels=True, label_column="LOCATION_NAME")
    assert isinstance(result, Axes)
    plt.close("all")
