from .canvas import _current_canvas

def plot_static_continuous_choropleth(
    gdf,
    column,
    title,
    legend_title,
    fig=None,
    ax=None,
    vmin=None,
    vmax=None,
    reverse=False,
    zorder=1,
):
    """Plots a choropleth map layer onto a Matplotlib axes.

    Args:
        gdf (gpd.GeoDataFrame): GeoDataFrame with data and geometry column for plotting.
        column (str): Column name to use for the choropleth colour scale.
        title (str): Title of the map.
        legend_title (str): Label for the legend colourbar.
        fig (matplotlib.figure.Figure): Figure object. Defaults to current canvas.
        ax (matplotlib.axes.Axes): Axes object to plot onto. Defaults to current canvas.
        vmin (float): Minimum value for the colour scale. Defaults to column minimum.
        vmax (float): Maximum value for the colour scale. Defaults to column maximum.
        reverse (bool): If True, reverses the colourmap (RdYlBu_r). Defaults to False.
        zorder (int): Layering order. Higher values plot on top. Defaults to 1.

    Returns:
        ax (matplotlib.axes.Axes): Axes object with choropleth layer added.
    """
    fig = fig or _current_canvas['fig']
    ax = ax or _current_canvas['ax']

    colormap = 'RdYlBu_r' if reverse else 'RdYlBu'
    vmin = gdf[column].min() if vmin is None else vmin
    vmax = gdf[column].max() if vmax is None else vmax

    cax = fig.add_axes([1, 0.2, 0.025, 0.5])

    gdf.plot(
        column=column,
        cmap=colormap,
        ax=ax,
        legend=True,
        legend_kwds={
            "label": legend_title,
            "cax": cax,
        },
        edgecolor="black",
        linewidth=0.1,
        zorder=zorder,
        vmin=vmin,
        vmax=vmax,
    )

    fig.suptitle(title, fontsize=20, x=0.5, y=0.97)

    return ax


def plot_static_categorical_choropleth(
    gdf,
    column,
    title,
    legend_title,
    categories,
    fig=None,
    ax=None,
    reverse=False,
    zorder=1,
):
    """Plots a categorical choropleth map layer onto a Matplotlib axes.

    Args:
        gdf (gpd.GeoDataFrame): GeoDataFrame with data and geometry column for plotting.
        column (str): Column name to use for the choropleth categories.
        title (str): Title of the map.
        legend_title (str): Label for the legend.
        categories (list): Ordered list of category values to display, e.g. range(1, 11).
        fig (matplotlib.figure.Figure): Figure object. Defaults to current canvas.
        ax (matplotlib.axes.Axes): Axes object to plot onto. Defaults to current canvas.
        reverse (bool): If True, reverses the colourmap (RdYlBu_r). Defaults to False.
        zorder (int): Layering order. Higher values plot on top. Defaults to 1.

    Returns:
        ax (matplotlib.axes.Axes): Axes object with choropleth layer added.
    """
    fig = fig or _current_canvas['fig']
    ax = ax or _current_canvas['ax']

    colormap = "RdYlBu_r" if reverse else "RdYlBu"

    gdf.plot(
        column=column,
        cmap=colormap,
        ax=ax,
        categorical=True,
        categories=categories,
        legend=True,
        legend_kwds={
            "title": legend_title,
            "loc": "lower right",
        },
        edgecolor="black",
        linewidth=0.1,
        zorder=zorder,
    )

    fig.suptitle(title, fontsize=20, x=0.5, y=0.97)

    return ax

