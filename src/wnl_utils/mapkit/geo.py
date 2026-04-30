import geopandas as gpd
from shapely import wkb


def prepare_geo_data(df):
    """Converts a DataFrame containing WKB geometry into a GeoDataFrame ready for plotting.

    Args:
        df (pd.DataFrame): DataFrame with a 'GEOMETRY_WKB' column containing
                           Well-Known Binary (WKB) encoded geometries.

    Returns:
        gpd.GeoDataFrame: GeoDataFrame with a 'geometry' column in EPSG:4326 (WGS84),
                          ready for use with geopandas plotting functions.
    """

    if "GEOMETRY_WKB" not in df.columns:
        raise KeyError(
            "Column 'GEOMETRY_WKB' not found. Ensure your SQL query includes geography "
            "encoded with ST_ASWKB(), aliased as GEOMETRY_WKB."
            "E.g. ST_ASWKB(GEOGRAPHY) AS GEOMETRY_WKB"
        )

    df["geometry"] = df["GEOMETRY_WKB"].apply(lambda x: wkb.loads(x) if x is not None else None)

    null_count = df["geometry"].isna().sum()
    if null_count > 0:
        print( f"Warning: {null_count} row(s) could not be mapped to a geography. "
        "This may indicate a join issue between the data table and the geography table, "
        "or that some areas have no corresponding boundary (e.g. filler or non-standard codes). "
        "These rows will not be plotted.")

    gdf = gpd.GeoDataFrame(df.drop(columns=["GEOMETRY_WKB"]), geometry="geometry", crs="EPSG:4326")
    return gdf

