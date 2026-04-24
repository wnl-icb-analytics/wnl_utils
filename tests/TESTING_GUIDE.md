# Testing Guide for `wnl_utils.mapkit`

This guide explains how to turn the test outline files in this folder into real tests.

## Goal of tests

Tests should prove three things:

1. the package imports correctly,
2. core functions behave as documented,
3. invalid inputs fail in a clear and expected way.

## Recommended test style

- Use `pytest`.
- Keep tests small and focused (one behavior per test).
- Use tiny synthetic data instead of large real datasets.
- Prefer deterministic assertions (avoid relying on visual inspection).

## Suggested stack

- `pytest` for test runner/assertions.
- `pandas` + `geopandas` + `shapely` for synthetic geometry test data.
- `matplotlib` in non-interactive mode for plotting tests.

## Useful pytest patterns

### 1) Basic assertion

```python
def test_true_is_true():
    assert True
```

### 2) Expected exception

```python
import pytest

def test_raises_value_error():
    with pytest.raises(ValueError):
        raise ValueError("example")
```

### 3) Parameterized cases

```python
import pytest

@pytest.mark.parametrize("value", ["white", "black", "red"])
def test_styles(value):
    assert isinstance(value, str)
```

## Project-specific examples

### Example: import smoke test

```python
import wnl_utils.mapkit as wm

def test_import_mapkit():
    assert hasattr(wm, "prepare_geo_data")
    assert hasattr(wm, "plot_map_canvas")
```

### Example: `prepare_geo_data` test

```python
import pandas as pd
from shapely.geometry import Point

import wnl_utils.mapkit as wm

def test_prepare_geo_data_converts_wkb():
    pt = Point(0, 0)
    df = pd.DataFrame({"GEOMETRY_WKB": [pt.wkb], "name": ["A"]})

    gdf = wm.prepare_geo_data(df)

    assert "geometry" in gdf.columns
    assert "GEOMETRY_WKB" not in gdf.columns
    assert gdf.crs.to_string().upper() in {"EPSG:4326", "WGS 84"}
```

### Example: plotting test pattern

```python
import geopandas as gpd
from shapely.geometry import Polygon

import wnl_utils.mapkit as wm

def test_plot_static_boundaries_returns_ax():
    poly = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
    gdf = gpd.GeoDataFrame(
        {"AREA_NAME": ["Test Area"]},
        geometry=[poly],
        crs="EPSG:4326",
    )

    wm.plot_map_canvas()
    ax = wm.plot_static_boundaries(gdf)

    assert ax is not None
```

### Example: error-path test

```python
import pytest

import wnl_utils.mapkit as wm

def test_invalid_fillstyle_raises():
    with pytest.raises(ValueError):
        wm.plot_wnl_boroughs_base(gdf=None, fillstyle="not-a-style")
```

Note: the exact setup for `gdf` should be valid in the real test; this snippet only shows the exception pattern.

## How to structure each test file

- `test_imports.py`: import/public API smoke tests.
- `test_geo.py`: `prepare_geo_data` behavior + validation.
- `test_canvas.py`: canvas lifecycle helpers.
- `test_boundaries.py`: boundary + borough base plotting behavior.
- `test_choropleth.py`: continuous/categorical choropleth behavior.
- `test_coordinates.py`: point styles + label validation behavior.

## Practical workflow for the intern

1. Open one `test_*.py` file.
2. Replace one comment stub with a real test.
3. Run tests locally.
4. Repeat until all comment stubs are implemented.
5. Keep tests readable and short.

## Running tests (once pytest is configured)

```bash
pytest -q
```

If you only want one file:

```bash
pytest -q tests/test_geo.py
```

## Quality checklist before PR

- Tests pass locally.
- At least one positive-path test and one error-path test per module.
- No large fixture files committed.
- Clear test names (`test_<function>_<expected_behavior>`).

