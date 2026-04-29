
import pytest
from shapely.geometry import Polygon
from shapely import wkb
import matplotlib
matplotlib.use("Agg") 

@pytest.fixture
def valid_wkb():
    """A simple valid WKB-encoded polygon, representative of LSOA boundary geometry."""
    return wkb.dumps(Polygon([(0, 0), (1, 0), (1, 1), (0, 1)]))
    
@pytest.fixture
def valid_polygon():
    """A simple valid shapely polygon, representative of LSOA boundary geometry."""
    return Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])