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
    if df["GEOMETRY_WKB"] is None:
        raise ("Geography in SQL Query must be GEOMETRY_WKB using ST_ASK")

    df["geometry"] = df["GEOMETRY_WKB"].apply(lambda x: wkb.loads(x) if x is not None else None)
    gdf = gpd.GeoDataFrame(df.drop(columns=["GEOMETRY_WKB"]), geometry="geometry", crs="EPSG:4326")
    return gdf

