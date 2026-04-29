from .canvas import _current_canvas
from ._constants import _WNL_PASTEL_COLOUR_MAP, _WNL_BOLD_COLOUR_MAP, _WNL_PLAIN_FILLCOLOR, _WNL_FALLBACK_COLOR


def _plot_centroid_labels(gdf, ax, zorder, fontsize=16):
    """Private helper that plots area name annotations at each polygon's centroid.

    Args:
        gdf (gpd.GeoDataFrame): GeoDataFrame containing geometries and 'AREA_NAME' column.
        ax (matplotlib.axes.Axes): Axes object to plot onto.
        zorder (int): Layering order for the annotations.
        fontsize (int): Font size for the labels. Defaults to 16.
    """
    for _, row in gdf.iterrows():
        name = row["AREA_NAME"].replace(" ", "\n")
        cx, cy = row.geometry.centroid.coords[0]

        ax.annotate(
            name,
            xy=(cx, cy),
            xycoords="data",
            ha="center",
            va="center",
            multialignment="center",
            fontsize=fontsize,
            color="black",
            bbox=dict(
                boxstyle="square,pad=0.15",
                fc="white",
                ec="none",
                alpha=0.7,
            ),
            zorder=zorder + 1,
        )


def plot_static_boundaries(
    gdf,
    ax=None,
    linewidth=1,
    linecolor="white",
    zorder=2,
    labels=False,
):
    """Plots boundary outlines of a GeoDataFrame as a map layer, with optional labels.

    Args:
        gdf (gpd.GeoDataFrame): GeoDataFrame containing the boundary geometries to plot.
        ax (matplotlib.axes.Axes): Axes object to plot onto. Defaults to current canvas.
        linewidth (float): Width of the boundary lines. Defaults to 1.
        linecolor (str): Colour of the boundary lines. Defaults to 'white'.
        zorder (int): Layering order. Higher values plot on top. Defaults to 2.
        labels (bool): If True, plots area name annotations at each polygon's centroid.
            Defaults to False.

    Returns:
        ax (matplotlib.axes.Axes): Axes object with boundary layer added.
    """

    if gdf is None:
        raise ValueError(
            "gdf is required. Provide a GeoDataFrame prepared with prepare_geo_data()."
        )

    if "geometry" not in gdf.columns:
        raise ValueError(
            "gdf must contain a valid geometry column. "
            "Ensure your data has been prepared using prepare_geo_data()."
        )

    if gdf.geometry.notna().sum() == 0:
        raise ValueError(
            "gdf contains no valid geometries. "
            "Ensure your data has been prepared using prepare_geo_data()."
        )
            
    ax = ax or _current_canvas["ax"]

    if ax is None:
        raise RuntimeError(
            "No axes object found. Call plot_map_canvas() before plotting, "
            "or pass an explicit ax argument."
        )

    gdf.boundary.plot(
        ax=ax,
        color=linecolor,
        linewidth=linewidth,
        zorder=zorder,
    )

    if labels:
        _plot_centroid_labels(gdf, ax, zorder)

    return ax


def plot_wnl_boroughs_base(
    gdf,
    ax=None,
    linewidth=1,
    linecolor="white",
    zorder=2,
    fillstyle="pastel",
):
    """Plots WNL borough polygons with branded fill colours.

    Args:
        gdf (gpd.GeoDataFrame): GeoDataFrame containing borough geometries
            and an 'AREA_NAME' column.
        ax (matplotlib.axes.Axes): Axes object to plot onto.
            Defaults to current canvas.
        linewidth (float): Width of the boundary lines.
        linecolor (str): Colour of the boundary lines.
        zorder (int): Layering order.
        fillstyle (str): Fill style for borough polygons.
            Options: 'plain', 'pastel', 'bold'.

    Returns:
        matplotlib.axes.Axes
    """
    if gdf is None:
        raise ValueError(
            "gdf is required. Provide a GeoDataFrame prepared with prepare_geo_data()."
        )

    if "geometry" not in gdf.columns:
        raise ValueError(
            "gdf must contain a valid geometry column. "
            "Ensure your data has been prepared using prepare_geo_data()."
        )

    if gdf.geometry.notna().sum() == 0:
        raise ValueError(
            "gdf contains no valid geometries. "
            "Ensure your data has been prepared using prepare_geo_data()."
        )

    ax = ax or _current_canvas["ax"]

    if ax is None:
        raise RuntimeError(
            "No axes object found. Call plot_map_canvas() before plotting, "
            "or pass an explicit ax argument."
        )

    if fillstyle == "plain":
        gdf.plot(
            ax=ax,
            color=_WNL_PLAIN_FILLCOLOR,
            edgecolor=linecolor,
            linewidth=linewidth,
            zorder=zorder,
        )

    elif fillstyle in ("pastel", "bold"):
        colour_map = (
            _WNL_PASTEL_COLOUR_MAP
            if fillstyle == "pastel"
            else _WNL_BOLD_COLOUR_MAP
        )

        colors = [
            colour_map.get(name, _WNL_FALLBACK_COLOR)
            for name in gdf["AREA_NAME"]
        ]

        gdf.plot(
            ax=ax,
            color=colors,
            edgecolor=linecolor,
            linewidth=linewidth,
            zorder=zorder,
        )

    else:
        raise ValueError(
            f"Invalid fillstyle '{fillstyle}'. "
            "Choose from 'plain', 'pastel', or 'bold'."
        )

    return ax

