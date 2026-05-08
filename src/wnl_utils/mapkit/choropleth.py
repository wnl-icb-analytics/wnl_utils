from .canvas import _current_canvas
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt 
import matplotlib.patches as mpatches 


def _resolve_continuous_cmap(cmap, reverse):
    """Returns a Matplotlib colormap name for continuous/sequential use."""
    options = {
        "diverging":  ("RdYlBu_r" if reverse else "RdYlBu"),
        "sequential": ("Blues_r"  if reverse else "Blues"),
    }
    if cmap not in options:
        raise ValueError(
            f"Invalid cmap '{cmap}'. Choose from: {list(options.keys())}."
        )
    return options[cmap]


def _resolve_categorical_cmap(cmap, reverse):
    """Returns a Matplotlib colormap name for categorical use."""
    options = {
        "diverging":   ("RdYlBu_r" if reverse else "RdYlBu"),
        "sequential":  ("Blues_r"  if reverse else "Blues"),
        "qualitative": "Set2",   # reverse has no meaningful effect on qualitative
    }
    if cmap not in options:
        raise ValueError(
            f"Invalid cmap '{cmap}'. Choose from: {list(options.keys())}."
        )
    return options[cmap]


def plot_static_continuous_choropleth(
    gdf,
    column,
    legend_title,       
    title=None,          
    fig=None,
    ax=None,
    vmin=None,
    vmax=None,
    cmap="diverging",
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
        cmap (str): Colour map style. One of "diverging" (RdYlBu) or "sequential" (Blues).
            Defaults to "diverging".
        reverse (bool): If True, reverses the colourmap. Defaults to False.
        zorder (int): Layering order. Higher values plot on top. Defaults to 1.

    Returns:
        ax (matplotlib.axes.Axes): Axes object with choropleth layer added.
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
    
    if column is None:
        raise ValueError(
            "column is required. Provide a column with data values for plotting."
        )

    if legend_title is None:
        raise ValueError(
            "legend_title is required. Provide a label for the choropleth colour scale."
        )

    fig = fig or _current_canvas["fig"]
    ax = ax or _current_canvas["ax"]
   
    if ax is None:
        raise RuntimeError(
            "No axes object found. Call plot_map_canvas() before plotting, "
            "or pass an explicit ax argument."
        )

    colormap = _resolve_continuous_cmap(cmap, reverse)

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
    
    if title:
        fig.suptitle(title, fontsize=20, x=0.5, y=0.97)

    return ax


def plot_static_categorical_choropleth(
    gdf,
    column,
    legend_title,
    categories=None,     
    title=None,
    fig=None,
    ax=None,
    cmap="diverging",
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
        cmap (str): Colour map style. One of "diverging" (RdYlBu), "sequential" (Blues),
            or "qualitative" (Set2). Defaults to "diverging".
        reverse (bool): If True, reverses the colourmap (no effect for "qualitative").
            Defaults to False.
        zorder (int): Layering order. Higher values plot on top. Defaults to 1.

    Returns:
        ax (matplotlib.axes.Axes): Axes object with choropleth layer added.
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

    if column is None:
        raise ValueError(
            "column is required. Provide a column with data values for plotting."
        )

    if legend_title is None:
        raise ValueError(
            "legend_title is required. Provide a label for the choropleth legend."
        )

    fig = fig or _current_canvas["fig"]
    ax = ax or _current_canvas["ax"]

    if ax is None:
        raise RuntimeError(
            "No axes object found. Call plot_map_canvas() before plotting, "
            "or pass an explicit ax argument."
        )

    colormap = _resolve_categorical_cmap(cmap, reverse)

    if cmap == "qualitative" and categories is not None and len(categories) > 8:
        raise ValueError(
            f"qualitative cmap 'Set2' supports a maximum of 8 categories, "
            f"but {len(categories)} were provided. Consider using cmap='diverging' "
            "or 'sequential', or reducing the number of categories."
        )

    if categories is not None:
        cat_type = type(categories[0])
        unmatched = {val for val in gdf[column].dropna().unique() if cat_type(val) not in set(categories)}
        if unmatched:
            raise ValueError(
                f"Column '{column}' contains values not found in categories: {sorted(unmatched)}. "
                "Ensure all values in the column are represented in the categories list."
            )

        gdf[column] = pd.Categorical(gdf[column], categories=categories, ordered=True)

        cmap_obj = plt.colormaps[colormap].resampled(len(categories))
        category_colors = {cat: matplotlib.colors.to_hex(cmap_obj(i)) for i, cat in enumerate(categories)}

        colors = [category_colors.get(val, "#000000") for val in gdf[column]]
        
        gdf.plot(
            color=colors,
            ax=ax,
            edgecolor="black",
            linewidth=0.1,
            zorder=zorder,
        )

        handles = [
            mpatches.Patch(facecolor=category_colors[cat], edgecolor="black", label=str(cat))
            for cat in categories
        ]

        ax.legend(
            handles=handles,
            title=legend_title,
            loc="lower right",
        )

    else:
        gdf.plot(
            column=column,
            cmap=colormap,
            ax=ax,
            categorical=True,
            legend=True,
            legend_kwds={
                "title": legend_title,
                "loc": "lower right",
            },
            edgecolor="black",
            linewidth=0.1,
            zorder=zorder,
        )

    if title:
        fig.suptitle(title, fontsize=20, x=0.5, y=0.97)

    return ax