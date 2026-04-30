
import wnl_utils.mapkit as mapkit


def test_import_mapkit_package():
    """Package imports without error."""
    import wnl_utils.mapkit


def test_public_api_symbols_present():
    """Expected public functions are accessible on wnl_utils.mapkit."""
    assert hasattr(mapkit, "prepare_geo_data")
    assert hasattr(mapkit, "plot_static_boundaries")
    assert hasattr(mapkit, "plot_wnl_boroughs_base")
    assert hasattr(mapkit, "plot_map_canvas")
    assert hasattr(mapkit, "get_map_canvas")
