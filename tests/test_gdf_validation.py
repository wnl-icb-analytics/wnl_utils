import pytest
import geopandas as gpd
import matplotlib.pyplot as plt
from wnl_utils.mapkit.boundaries import plot_static_boundaries, plot_wnl_boroughs_base
from wnl_utils.mapkit.choropleth import plot_static_continuous_choropleth, plot_static_categorical_choropleth
from wnl_utils.mapkit.coordinates import plot_static_coordinates

# --- Shared helpers ---

PLOTTING_FUNCTIONS = [
    lambda gdf, ax, fig: plot_static_boundaries(gdf, ax=ax),
    lambda gdf, ax, fig: plot_wnl_boroughs_base(gdf, ax=ax),
    lambda gdf, ax, fig: plot_static_continuous_choropleth(gdf, column="TEST_COLUMN", legend_title="My Legend", ax=ax, fig=fig),
    lambda gdf, ax, fig: plot_static_categorical_choropleth(gdf, column="TEST_COLUMN", legend_title="My Legend", categories=[3], ax=ax, fig=fig),
    lambda gdf, ax, fig: plot_static_coordinates(gdf, ax=ax),
]


@pytest.fixture
def null_geometry_gdf():
    """GeoDataFrame where all geometries are null."""
    return gpd.GeoDataFrame(
        {"TEST_COLUMN": [1], "AREA_NAME": ["A"]},
        geometry=[None],
        crs="EPSG:4326"
    )


@pytest.fixture
def no_geometry_column_df():
    """Plain DataFrame with no geometry column at all."""
    return gpd.GeoDataFrame(
        {"TEST_COLUMN": [1], "AREA_NAME": ["A"]}
    )


# --- gdf is None ---

@pytest.mark.parametrize("plot_fn", PLOTTING_FUNCTIONS)
def test_raises_when_gdf_is_none(plot_fn):
    fig, ax = plt.subplots()
    with pytest.raises(ValueError, match="gdf is required"):
        plot_fn(None, ax, fig)
    plt.close("all")


# --- No geometry column ---

@pytest.mark.parametrize("plot_fn", PLOTTING_FUNCTIONS)
def test_raises_when_no_geometry_column(plot_fn, no_geometry_column_df):
    fig, ax = plt.subplots()
    with pytest.raises(ValueError, match="geometry column"):
        plot_fn(no_geometry_column_df, ax, fig)
    plt.close("all")


# --- All null geometries ---

@pytest.mark.parametrize("plot_fn", PLOTTING_FUNCTIONS)
def test_raises_when_all_geometries_null(plot_fn, null_geometry_gdf):
    fig, ax = plt.subplots()
    with pytest.raises(ValueError, match="no valid geometries"):
        plot_fn(null_geometry_gdf, ax, fig)
    plt.close("all")