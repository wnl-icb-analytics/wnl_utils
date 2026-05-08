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

def test_categorical_choropleth_raises_on_unmatched_values(choropleth_gdf):
    fig, ax = plt.subplots()
    with pytest.raises(ValueError, match="not found in categories"):
        plot_static_categorical_choropleth(
            choropleth_gdf,
            column="TEST_COLUMN",
            legend_title="My Legend",
            categories=[1, 2],
            ax=ax,
            fig=fig,
        )
    plt.close("all")


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

CONTINUOUS_VALID_CMAPS = ["diverging", "sequential"]
CATEGORICAL_VALID_CMAPS = ["diverging", "sequential", "qualitative"]


def _get_legend_colors(ax):
    """Return face colours from all legend patch handles on ax."""
    return [h.get_facecolor() for h in ax.get_legend().legend_handles]



# Continuous choropleth – cmap

class TestContinuousChoropletCmap:

    @pytest.mark.parametrize("cmap", CONTINUOUS_VALID_CMAPS)
    def test_valid_cmap_returns_axes(self, choropleth_gdf, cmap):
        """Each valid cmap string should run without error and return an Axes."""
        fig, ax = plt.subplots()
        result = plot_static_continuous_choropleth(
            choropleth_gdf, column="TEST_COLUMN", legend_title="Legend", ax=ax, fig=fig, cmap=cmap
        )
        assert isinstance(result, Axes)
        plt.close("all")

    def test_invalid_cmap_raises(self, choropleth_gdf):
        """An unrecognised cmap value should raise ValueError."""
        fig, ax = plt.subplots()
        with pytest.raises(ValueError, match="Invalid cmap"):
            plot_static_continuous_choropleth(
                choropleth_gdf, column="TEST_COLUMN", legend_title="Legend", ax=ax, fig=fig, cmap="qualitative"
            )
        plt.close("all")

    @pytest.mark.parametrize("cmap", CONTINUOUS_VALID_CMAPS)
    def test_reverse_produces_different_colorbar_than_default(self, choropleth_gdf, cmap):
        """reverse=True should yield a different colormap to reverse=False for every valid cmap."""
        def _get_colormap_name(reverse):
            fig, ax = plt.subplots()
            result = plot_static_continuous_choropleth(
                choropleth_gdf,
                column="TEST_COLUMN",
                legend_title="Legend",
                ax=ax,
                fig=fig,
                cmap=cmap,
                reverse=reverse,
            )
            # The colormap is stored on the polycollection drawn by geopandas
            cmap_name = result.collections[0].cmap.name
            plt.close("all")
            return cmap_name

        assert _get_colormap_name(reverse=False) != _get_colormap_name(reverse=True)

    @pytest.mark.parametrize("bad_cmap", ["qualitative", "plasma", "viridis", "", None])
    def test_various_invalid_cmaps_raise(self, choropleth_gdf, bad_cmap):
        """Any value outside the accepted set should raise ValueError."""
        fig, ax = plt.subplots()
        with pytest.raises((ValueError, TypeError)):
            plot_static_continuous_choropleth(
                choropleth_gdf, column="TEST_COLUMN", legend_title="Legend", ax=ax, fig=fig, cmap=bad_cmap
            )
        plt.close("all")


# ---------------------------------------------------------------------------
# Categorical choropleth – cmap
# ---------------------------------------------------------------------------

class TestCategoricalChoropletCmap:

    @pytest.mark.parametrize("cmap", CATEGORICAL_VALID_CMAPS)
    def test_valid_cmap_returns_axes(self, choropleth_gdf, cmap):
        """Each valid cmap string should run without error and return an Axes."""
        fig, ax = plt.subplots()
        result = plot_static_categorical_choropleth(
            choropleth_gdf, column="TEST_COLUMN", legend_title="Legend", ax=ax, fig=fig,
            categories=[3], cmap=cmap
        )
        assert isinstance(result, Axes)
        plt.close("all")

    @pytest.mark.parametrize("bad_cmap", ["plasma", "viridis", "RdYlBu", "", None])
    def test_invalid_cmap_raises(self, choropleth_gdf, bad_cmap):
        """An unrecognised cmap value should raise ValueError."""
        fig, ax = plt.subplots()
        with pytest.raises((ValueError, TypeError)):
            plot_static_categorical_choropleth(
                choropleth_gdf, column="TEST_COLUMN", legend_title="Legend", ax=ax, fig=fig,
                categories=[3], cmap=bad_cmap
            )
        plt.close("all")

    @pytest.mark.parametrize("cmap", ["diverging", "sequential"])
    def test_reverse_produces_different_colors(self, choropleth_gdf, cmap):
        """reverse=True should produce different legend colours for diverging and sequential cmaps."""
        categories = [1, 2, 3]

        def _colors(reverse):
            fig, ax = plt.subplots()
            plot_static_categorical_choropleth(
                choropleth_gdf, column="TEST_COLUMN", legend_title="Legend",
                categories=categories, ax=ax, fig=fig, cmap=cmap, reverse=reverse,
            )
            cols = _get_legend_colors(ax)
            plt.close("all")
            return cols

        assert _colors(reverse=False) != _colors(reverse=True)

    def test_qualitative_cmap_reverse_has_no_effect(self, choropleth_gdf):
        """reverse has no meaningful effect on the qualitative cmap; colours should be identical."""
        categories = [1, 2, 3]

        def _colors(reverse):
            fig, ax = plt.subplots()
            plot_static_categorical_choropleth(
                choropleth_gdf, column="TEST_COLUMN", legend_title="Legend",
                categories=categories, ax=ax, fig=fig, cmap="qualitative", reverse=reverse,
            )
            cols = _get_legend_colors(ax)
            plt.close("all")
            return cols

        assert _colors(reverse=False) == _colors(reverse=True)

    def test_qualitative_cmap_raises_above_8_categories(self, choropleth_gdf):
        """qualitative cmap should raise ValueError when more than 8 categories are supplied."""
        fig, ax = plt.subplots()
        with pytest.raises(ValueError, match="maximum of 8 categories"):
            plot_static_categorical_choropleth(
                choropleth_gdf, column="TEST_COLUMN", legend_title="Legend",
                categories=list(range(1, 10)),  # 9 categories
                ax=ax, fig=fig, cmap="qualitative",
            )
        plt.close("all")

    def test_qualitative_cmap_accepts_exactly_8_categories(self, choropleth_gdf):
        """qualitative cmap should accept exactly 8 categories without error."""
        fig, ax = plt.subplots()

        # Extend the fixture data to cover all 8 categories
        import geopandas as gpd
        from shapely.geometry import Point
        poly = choropleth_gdf.geometry.iloc[0]
        extended_gdf = gpd.GeoDataFrame(
            {"AREA_NAME": [f"Borough {i}" for i in range(1, 9)],
             "TEST_COLUMN": list(range(1, 9))},
            geometry=[poly] * 8,
            crs="EPSG:4326",
        )

        result = plot_static_categorical_choropleth(
            extended_gdf, column="TEST_COLUMN", legend_title="Legend",
            categories=list(range(1, 9)),
            ax=ax, fig=fig, cmap="qualitative",
        )
        assert isinstance(result, Axes)
        plt.close("all")

    @pytest.mark.parametrize("cmap", CATEGORICAL_VALID_CMAPS)
    def test_different_cmaps_produce_different_colors(self, choropleth_gdf, cmap):
        """Each valid cmap should produce visually distinct colours from the others."""
        categories = [1, 2, 3]

        def _colors(c):
            fig, ax = plt.subplots()
            plot_static_categorical_choropleth(
                choropleth_gdf, column="TEST_COLUMN", legend_title="Legend",
                categories=categories, ax=ax, fig=fig, cmap=c,
            )
            cols = _get_legend_colors(ax)
            plt.close("all")
            return cols

        other_cmaps = [c for c in CATEGORICAL_VALID_CMAPS if c != cmap]
        colors_under_test = _colors(cmap)
        for other in other_cmaps:
            assert colors_under_test != _colors(other), (
                f"cmap='{cmap}' produced the same colours as cmap='{other}'"
            )


