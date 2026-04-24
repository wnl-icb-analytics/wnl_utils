# Expected tests for `prepare_geo_data`
#
# - test_prepare_geo_data_converts_wkb_to_geometry:
#   Provide a minimal DataFrame with valid WKB and assert geometry column is created.
#
# - test_prepare_geo_data_drops_geometry_wkb_column:
#   Ensure GEOMETRY_WKB is not present in the returned GeoDataFrame.
#
# - test_prepare_geo_data_preserves_non_geometry_columns:
#   Assert ordinary data columns survive transformation.
#
# - test_prepare_geo_data_handles_none_wkb_values:
#   Assert None values produce None geometries without crashing.
#
# - test_prepare_geo_data_sets_expected_crs:
#   Assert CRS is EPSG:4326 as documented.
#
# - test_prepare_geo_data_raises_on_missing_geometry_wkb_column:
#   Assert clear failure/exception when GEOMETRY_WKB is absent.

