from .canvas import _current_canvas
from ._constants import _POINT_STYLE_MAP


def plot_static_coordinates(
    gdf,
    ax=None,
    pointstyle="white",
    pointsize=25,
    zorder=3,
    labels=False,
    label_column=None,
):
    """Plots point coordinates from a GeoDataFrame as a map layer.

    Args:
        gdf (gpd.GeoDataFrame): GeoDataFrame containing point geometries to plot.
        ax (matplotlib.axes.Axes): Axes object to plot onto. Defaults to current canvas.
        pointstyle (str): Named preset for point appearance. Options:
            - 'white'    : White circle, black outline (default)
            - 'black'    : Black circle, white outline
            - 'red'      : Red circle, white outline
            - 'triangle' : White triangle, dark outline
            - 'diamond'  : Amber diamond, white outline
            - 'plus'     : Red plus, white outline
        pointsize (int): Size of the point markers. Defaults to 25.
        zorder (int): Layering order. Higher values plot on top. Defaults to 3.
        labels (bool): If True, plots point name annotations below each point. Defaults to False.
        label_column (str): Column name to use for point labels. Required if labels=True.

    Returns:
        ax (matplotlib.axes.Axes): Axes object with coordinate layer added.
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

    if labels and label_column is None:
        raise ValueError("label_column must be provided when labels=True.")
    
    
    ax = ax or _current_canvas["ax"]

    if ax is None:
        raise RuntimeError(
            "No axes object found. Call plot_map_canvas() before plotting, "
            "or pass an explicit ax argument."
        )

    style = _POINT_STYLE_MAP[pointstyle]

    gdf.plot(
        ax=ax,
        color=style["color"],
        edgecolor=style["edgecolor"],
        marker=style["marker"],
        markersize=pointsize,
        alpha=0.8,
        linewidth=0.5,
        zorder=zorder,
    )

    if labels:
        for _, row in gdf.iterrows():
            cx, cy = row.geometry.coords[0]
            name = row[label_column].replace(" ", "\n")

            ax.annotate(
                name,
                xy=(cx, cy),
                xycoords="data",
                xytext=(0, -10),
                textcoords="offset points",
                ha="center",
                va="top",
                multialignment="center",
                fontsize=10,
                color="black",
                bbox=dict(
                    boxstyle="square,pad=0.15",
                    fc="white",
                    ec="none",
                    alpha=0.7,
                ),
                zorder=zorder + 1,
            )

    return ax

