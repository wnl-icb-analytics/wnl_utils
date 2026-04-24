# wnl-mapkit

A Python package for creating geospatial maps of WNL boroughs. Provides a set of composable plotting functions for building choropleth maps, boundary layers, and point overlays using GeoPandas and Matplotlib.

> **Note:** This package is designed primarily for use in Snowflake notebooks. It can be used in an IDE, but a Snowflake connection will need to be established and query results converted with `.to_pandas()` before use.

---

## Quick Start

The typical workflow is:

1. Query Snowflake to get a DataFrame containing a `GEOMETRY_WKB` column
2. Pass it through `prepare_geo_data()` to convert to a GeoDataFrame
3. Create a canvas and layer your plots on top

### In a Snowflake Notebook

```python
import wnl_mapkit as wm

# Query Snowflake
df = session.sql("SELECT * FROM my_borough_table").to_pandas()

# Convert WKB geometry to GeoDataFrame
gdf = wm.prepare_geo_data(df)

# Create canvas and plot
wm.plot_map_canvas()
wm.plot_wnl_boroughs_base(gdf, fillstyle='pastel')
wm.plot_static_boundaries(gdf, labels=True)
```

### In an IDE

```python
import wnl_mapkit as wm
from snowflake.snowpark import Session

# Establish Snowflake connection
session = Session.builder.configs(connection_params).create()

# Query and convert
df = session.sql("SELECT * FROM my_borough_table").to_pandas()

# Convert WKB geometry to GeoDataFrame
gdf = wm.prepare_geo_data(df)

# Create canvas and plot
wm.plot_map_canvas()
wm.plot_wnl_boroughs_base(gdf, fillstyle='pastel')
wm.plot_static_boundaries(gdf, labels=True)
```

---

## Function Reference

### `prepare_geo_data(df)`
Converts a DataFrame containing a `GEOMETRY_WKB` column into a GeoDataFrame ready for plotting.

| Parameter | Type | Description |
|---|---|---|
| `df` | `pd.DataFrame` | DataFrame with a `GEOMETRY_WKB` column containing WKB-encoded geometries |

Returns a `GeoDataFrame` in EPSG:4326 (WGS84).

---

### `plot_map_canvas(figsize=(12, 10))`
Creates a Matplotlib figure and axes, stored as the current canvas. Call this before any plotting functions.

| Parameter | Type | Description |
|---|---|---|
| `figsize` | `tuple` | Width and height of the figure in inches. Defaults to `(12, 10)` |

---

### `get_map_canvas()`
Returns the current `(fig, ax)` tuple created by `plot_map_canvas()`.

---

### `plot_wnl_boroughs_base(gdf, ...)`
Plots WNL borough polygons with branded fill colours.

| Parameter | Type | Description |
|---|---|---|
| `gdf` | `GeoDataFrame` | Must contain an `AREA_NAME` column |
| `fillstyle` | `str` | `'plain'`, `'pastel'` (default), or `'bold'` |
| `linewidth` | `float` | Width of boundary lines. Defaults to `1` |
| `linecolor` | `str` | Colour of boundary lines. Defaults to `'white'` |
| `zorder` | `int` | Layer order. Defaults to `2` |

---

### `plot_static_boundaries(gdf, ...)`
Plots boundary outlines with optional area name labels.

| Parameter | Type | Description |
|---|---|---|
| `gdf` | `GeoDataFrame` | GeoDataFrame containing boundary geometries |
| `linewidth` | `float` | Width of boundary lines. Defaults to `1` |
| `linecolor` | `str` | Colour of boundary lines. Defaults to `'white'` |
| `zorder` | `int` | Layer order. Defaults to `2` |
| `labels` | `bool` | If `True`, plots area names at polygon centroids. Defaults to `False` |

---

### `plot_static_continuous_choropleth(gdf, column, title, legend_title, ...)`
Plots a continuous choropleth map layer.

| Parameter | Type | Description |
|---|---|---|
| `gdf` | `GeoDataFrame` | GeoDataFrame with data and geometry |
| `column` | `str` | Column to use for the colour scale |
| `title` | `str` | Map title |
| `legend_title` | `str` | Label for the colourbar |
| `vmin` | `float` | Minimum value for colour scale. Defaults to column min |
| `vmax` | `float` | Maximum value for colour scale. Defaults to column max |
| `reverse` | `bool` | If `True`, reverses the colourmap. Defaults to `False` |
| `zorder` | `int` | Layer order. Defaults to `1` |

---

### `plot_static_categorical_choropleth(gdf, column, title, legend_title, categories, ...)`
Plots a categorical choropleth map layer.

| Parameter | Type | Description |
|---|---|---|
| `gdf` | `GeoDataFrame` | GeoDataFrame with data and geometry |
| `column` | `str` | Column to use for categories |
| `title` | `str` | Map title |
| `legend_title` | `str` | Label for the legend |
| `categories` | `list` | Ordered list of category values, e.g. `range(1, 11)` |
| `reverse` | `bool` | If `True`, reverses the colourmap. Defaults to `False` |
| `zorder` | `int` | Layer order. Defaults to `1` |

---

### `plot_static_coordinates(gdf, ...)`
Plots point coordinates as a map layer.

| Parameter | Type | Description |
|---|---|---|
| `gdf` | `GeoDataFrame` | GeoDataFrame containing point geometries |
| `pointstyle` | `str` | `'white'`, `'black'`, `'red'`, `'triangle'`, `'diamond'`, or `'plus'`. Defaults to `'white'` |
| `pointsize` | `int` | Size of point markers. Defaults to `25` |
| `zorder` | `int` | Layer order. Defaults to `3` |
| `labels` | `bool` | If `True`, plots point name annotations. Defaults to `False` |
| `label_column` | `str` | Column to use for labels. Required if `labels=True` |
