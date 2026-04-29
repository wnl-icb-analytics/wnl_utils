import pytest
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, MultiPolygon
from shapely.geometry.base import BaseGeometry
from shapely import wkb
from wnl_utils.mapkit.geo import prepare_geo_data


@pytest.fixture
def minimal_df(valid_wkb):
    """Minimal DataFrame with a single valid WKB geometry."""
    return pd.DataFrame({
        "GEOMETRY_WKB": [valid_wkb],
        "area_code": ["E01000001"]
    })

def test_prepare_geo_data_converts_wkb_to_geometry(minimal_df):
    """Geometry column exists and contains valid Shapely geometries."""
    result = prepare_geo_data(minimal_df)
    assert "geometry" in result.columns
    assert isinstance(result.geometry.iloc[0], BaseGeometry)

def test_prepare_geo_data_returns_geodataframe(minimal_df):
    """Return type is a GeoDataFrame in EPSG:4326."""
    result = prepare_geo_data(minimal_df)
    assert isinstance(result, gpd.GeoDataFrame)
    assert result.crs.to_epsg() == 4326   

def test_prepare_geo_data_preserves_non_geometry_columns(minimal_df):
    """Other columns are untouched."""
    result = prepare_geo_data(minimal_df)
    assert "area_code" in result.columns
    assert result["area_code"].iloc[0] == "E01000001" 

def test_prepare_geo_data_raises_on_missing_geometry_wkb_column():
    df = pd.DataFrame({"some_other_col": [1, 2, 3]})
    with pytest.raises(KeyError, match="GEOMETRY_WKB"):
        prepare_geo_data(df)


#None / null geometry handling

def test_prepare_geo_data_handles_none_wkb_without_crashing():
    """None values in GEOMETRY_WKB should not raise an exception."""
    df = pd.DataFrame({
        "GEOMETRY_WKB": [None],
        "area_code": ["E01000999"]
    })
    result = prepare_geo_data(df)  # should not raise
    assert len(result) == 1


def test_prepare_geo_data_none_wkb_produces_none_geometry():
    """None WKB values should produce None geometry entries, not crash or silently corrupt."""
    df = pd.DataFrame({
        "GEOMETRY_WKB": [None],
        "area_code": ["E01000999"]
    })
    result = prepare_geo_data(df)
    assert result.geometry.iloc[0] is None


def test_prepare_geo_data_mixed_valid_and_none_wkb(valid_wkb):
    """Realistic Snowflake scenario: mix of valid rows and null geometries."""
    df = pd.DataFrame({
        "GEOMETRY_WKB": [valid_wkb, None, valid_wkb, None],
        "area_code": ["E01000001", "E01000002", "E01000003", "E01000004"]
    })
    result = prepare_geo_data(df)

    assert len(result) == 4                          # no rows dropped
    assert result.geometry.iloc[0] is not None      # valid rows intact
    assert result.geometry.iloc[1] is None          # nulls preserved as None
    assert result.geometry.notna().sum() == 2       # exactly 2 valid geometries


def test_prepare_geo_data_warns_on_none_geometries(capsys):
    df = pd.DataFrame({
        "GEOMETRY_WKB": [None],
        "area_code": ["E01000999"]
    })
    prepare_geo_data(df)
    captured = capsys.readouterr()
    assert "1 row(s)" in captured.out
    assert "could not be mapped to a geography" in captured.out
