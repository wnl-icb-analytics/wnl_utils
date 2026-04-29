import pytest
import geopandas as gpd
from matplotlib.axes import Axes
import matplotlib.pyplot as plt
from wnl_utils.mapkit.choropleth import plot_static_categorical_choropleth, plot_static_continuous_choropleth


@pytest.fixture
def choropleth_gdf(valid_polygon):
    """Minimal GeoDataFrame with geometry, AREA_NAME, and plotting data"""
    return gpd.GeoDataFrame(
        {"AREA_NAME": ["Test Borough"],
        "TEST_COLUMN" : [3]},
        geometry=[valid_polygon],
        crs="EPSG:4326"
    )


def test_continuous_choropleth_raises_without_legend_title(choropleth_gdf):
    fig, ax = plt.subplots()
    with pytest.raises(ValueError, match="legend_title is required"):
        plot_static_continuous_choropleth(
            choropleth_gdf, column="TEST_COLUMN", legend_title=None, ax=ax, fig=fig
        )
    plt.close("all")


def test_continuous_choropleth_runs_without_title(choropleth_gdf):
    fig, ax = plt.subplots()
    result = plot_static_continuous_choropleth(
        choropleth_gdf, column="TEST_COLUMN", legend_title="My Legend", ax=ax, fig=fig
    )
    assert isinstance(result, Axes)
    plt.close("all")

def test_categorical_choropleth_raises_without_legend_title(choropleth_gdf):
    fig, ax = plt.subplots()
    with pytest.raises(ValueError, match="legend_title is required"):
        plot_static_categorical_choropleth(
            choropleth_gdf, column="TEST_COLUMN", legend_title=None, ax=ax, fig=fig, categories=[3]
        )
    plt.close("all")


def test_categorical_choropleth_runs_without_title(choropleth_gdf):
    fig, ax = plt.subplots()
    result = plot_static_categorical_choropleth(
        choropleth_gdf, column="TEST_COLUMN", legend_title="My Legend", ax=ax, fig=fig, categories=[3]
    )
    assert isinstance(result, Axes)
    plt.close("all")

def test_plot_static_continuous_choropleth_respects_vmin_vmax(choropleth_gdf):
    fig, ax = plt.subplots()
    result = plot_static_continuous_choropleth(
        choropleth_gdf,
        column="TEST_COLUMN",
        legend_title="My Legend",
        ax=ax,
        fig=fig,
        vmin=0,
        vmax=10,
    )
    assert isinstance(result, Axes)
    plt.close("all")


def test_plot_static_categorical_choropleth_runs_with_categories(choropleth_gdf):
    fig, ax = plt.subplots()
    result = plot_static_categorical_choropleth(
        choropleth_gdf,
        column="TEST_COLUMN",
        legend_title="My Legend",
        categories=[3],
        ax=ax,
        fig=fig,
    )
    assert isinstance(result, Axes)
    plt.close("all")

def test_plot_static_categorical_choropleth_raises_without_categories(choropleth_gdf):
    fig, ax = plt.subplots()
    with pytest.raises(ValueError, match="categories is required"):
        plot_static_categorical_choropleth(
            choropleth_gdf,
            column="TEST_COLUMN",
            legend_title="My Legend",
            ax=ax,
            fig=fig,
        )
    plt.close("all")

def test_plot_static_continuous_choropleth_raises_without_canvas(choropleth_gdf):
    """Raises RuntimeError when no ax is passed and canvas has not been initialised."""
    with pytest.raises(RuntimeError, match="plot_map_canvas"):
        plot_static_continuous_choropleth(
            choropleth_gdf,
            column="TEST_COLUMN",
            legend_title="My Legend",
        )


def test_plot_static_categorical_choropleth_raises_without_canvas(choropleth_gdf):
    """Raises RuntimeError when no ax is passed and canvas has not been initialised."""
    with pytest.raises(RuntimeError, match="plot_map_canvas"):
        plot_static_categorical_choropleth(
            choropleth_gdf,
            column="TEST_COLUMN",
            legend_title="My Legend",
            categories=[3],
        )



