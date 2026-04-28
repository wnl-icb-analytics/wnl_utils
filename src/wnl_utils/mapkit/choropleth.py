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
    if legend_title is None:
        raise ValueError(
            "legend_title is required. Provide a label for the choropleth colour scale."
        )

    fig = fig or _current_canvas["fig"]
    ax = ax or _current_canvas["ax"]
    ...
    if title:
        fig.suptitle(title, fontsize=20, x=0.5, y=0.97)

    return ax


def plot_static_categorical_choropleth(
    gdf,
    column,
    legend_title,
    categories=None,     # ← give it a default so the error message is what fires
    title=None,
    fig=None,
    ax=None,
    reverse=False,
    zorder=1,
):
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
    ...
    if title:
        fig.suptitle(title, fontsize=20, x=0.5, y=0.97)

    return ax

