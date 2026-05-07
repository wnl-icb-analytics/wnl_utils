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

# def test_plot_static_categorical_choropleth_raises_without_categories(choropleth_gdf):
#     fig, ax = plt.subplots()
#     with pytest.raises(ValueError, match="categories is required"):
#         plot_static_categorical_choropleth(
#             choropleth_gdf,
#             column="TEST_COLUMN",
#             legend_title="My Legend",
#             ax=ax,
#             fig=fig,
#         )
#     plt.close("all")

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

def test_categorical_choropleth_legend_contains_all_categories(choropleth_gdf):
    """Legend should contain all user-defined categories even if some are absent from the data."""
    fig, ax = plt.subplots()
    result = plot_static_categorical_choropleth(
        choropleth_gdf,
        column="TEST_COLUMN",
        legend_title="My Legend",
        categories=[1, 2, 3, 4, 5],  # data only contains 3, rest are missing
        ax=ax,
        fig=fig,
    )
    legend = result.get_legend()
    legend_labels = [t.get_text() for t in legend.get_texts()]
    assert legend_labels == ["1", "2", "3", "4", "5"]
    plt.close("all")


def test_categorical_choropleth_legend_respects_order(choropleth_gdf):
    """Legend order should match the user-defined categories list exactly."""
    fig, ax = plt.subplots()
    categories = [5, 4, 3, 2, 1]  # reversed order
    result = plot_static_categorical_choropleth(
        choropleth_gdf,
        column="TEST_COLUMN",
        legend_title="My Legend",
        categories=categories,
        ax=ax,
        fig=fig,
    )
    legend = result.get_legend()
    legend_labels = [t.get_text() for t in legend.get_texts()]
    assert legend_labels == ["5", "4", "3", "2", "1"]
    plt.close("all")


def test_categorical_choropleth_legend_title_is_set(choropleth_gdf):
    """Legend title should match the legend_title argument."""
    fig, ax = plt.subplots()
    result = plot_static_categorical_choropleth(
        choropleth_gdf,
        column="TEST_COLUMN",
        legend_title="My Legend Title",
        categories=[3],
        ax=ax,
        fig=fig,
    )
    legend = result.get_legend()
    assert legend.get_title().get_text() == "My Legend Title"
    plt.close("all")


def test_categorical_choropleth_sets_figure_title(choropleth_gdf):
    """Figure suptitle should be set when title argument is provided."""
    fig, ax = plt.subplots()
    plot_static_categorical_choropleth(
        choropleth_gdf,
        column="TEST_COLUMN",
        legend_title="My Legend",
        categories=[3],
        title="My Map Title",
        ax=ax,
        fig=fig,
    )
    assert fig.texts[0].get_text() == "My Map Title"
    plt.close("all")


def test_categorical_choropleth_no_title_sets_no_suptitle(choropleth_gdf):
    """No figure suptitle should be set when title is omitted."""
    fig, ax = plt.subplots()
    plot_static_categorical_choropleth(
        choropleth_gdf,
        column="TEST_COLUMN",
        legend_title="My Legend",
        categories=[3],
        ax=ax,
        fig=fig,
    )
    assert len(fig.texts) == 0
    plt.close("all")


def test_categorical_choropleth_reverse_produces_different_colors(choropleth_gdf):
    """reverse=True should produce a different colour for the same category than reverse=False."""
    categories = [1, 2, 3]

    fig, ax = plt.subplots()
    plot_static_categorical_choropleth(
        choropleth_gdf,
        column="TEST_COLUMN",
        legend_title="My Legend",
        categories=categories,
        ax=ax,
        fig=fig,
        reverse=False,
    )
    handles_normal = ax.get_legend().legend_handles
    colors_normal = [h.get_facecolor() for h in handles_normal]
    plt.close("all")

    fig, ax = plt.subplots()
    plot_static_categorical_choropleth(
        choropleth_gdf,
        column="TEST_COLUMN",
        legend_title="My Legend",
        categories=categories,
        ax=ax,
        fig=fig,
        reverse=True,
    )
    handles_reversed = ax.get_legend().legend_handles
    colors_reversed = [h.get_facecolor() for h in handles_reversed]
    plt.close("all")

    assert colors_normal != colors_reversed


def test_categorical_choropleth_raises_without_gdf():
    """Should raise ValueError when gdf is None."""
    fig, ax = plt.subplots()
    with pytest.raises(ValueError, match="gdf is required"):
        plot_static_categorical_choropleth(
            None,
            column="TEST_COLUMN",
            legend_title="My Legend",
            categories=[3],
            ax=ax,
            fig=fig,
        )
    plt.close("all")


def test_categorical_choropleth_raises_without_column(choropleth_gdf):
    """Should raise ValueError when column is None."""
    fig, ax = plt.subplots()
    with pytest.raises(ValueError, match="column is required"):
        plot_static_categorical_choropleth(
            choropleth_gdf,
            column=None,
            legend_title="My Legend",
            categories=[3],
            ax=ax,
            fig=fig,
        )
    plt.close("all")



