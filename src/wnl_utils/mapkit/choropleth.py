from .canvas import _current_canvas

def plot_static_continuous_choropleth(
    gdf,
    column,
    legend_title,       
    title=None,          
    fig=None,
    ax=None,
    vmin=None,
    vmax=None,
    reverse=False,
    zorder=1,
):

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

    colormap = "RdYlBu_r" if reverse else "RdYlBu"

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
        vmax=vmax
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
    reverse=False,
    zorder=1,
):

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

    if categories is None:
        raise ValueError(
            "categories is required. Provide an ordered list of category values "
            "to display, e.g. categories=[1, 2, 3, 4, 5] or categories=['low', 'medium', 'high']."
        )

    fig = fig or _current_canvas["fig"]
    ax = ax or _current_canvas["ax"]
    
    if ax is None:
        raise RuntimeError(
            "No axes object found. Call plot_map_canvas() before plotting, "
            "or pass an explicit ax argument."
        )

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

    if title:
        fig.suptitle(title, fontsize=20, x=0.5, y=0.97)

    return ax

