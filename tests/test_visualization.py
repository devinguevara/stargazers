import sys
import os
import pytest
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Add 'src' directory to the path for importing modules
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)
from cs107stargazers.visualization import SDSSVis

"""
    class SDSSVis
    Method: `spectralplot()` : Plot spectral visualization
    Method: `ic_overlay()` : Plot spectral visualization with inferred continuum overlay
"""


import sys
import os
import pandas as pd
import pytest

# Add the directory containing SDSSVis to the path for importing
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)
from cs107stargazers.visualization import SDSSVis  # Replace with actual module name


@pytest.fixture
def sample_spectral_data():
    """
    Fixture for creating sample spectral data as a pandas DataFrame.
    """
    return pd.DataFrame({
        "wavelength": [412, 536, 615, 748, 811],
        "flux": [12, 25, 19, 23, 36],
        "inferred_continuum": [1, 2, 3, 4, 5]
    })


@pytest.fixture
def sdss_vis_instance(sample_spectral_data):
    """
    Fixture for creating an SDSSVis instance.
    """
    return SDSSVis(sample_spectral_data)


def test_spectralplot(sdss_vis_instance):
    """
    Test the spectralplot function to ensure it doesn't raise errors.
    """
    try:
        sdss_vis_instance.spectralplot()
        assert True
    except Exception:
        assert False


def test_ic_overlay(sdss_vis_instance):
    """
    Test the ic_overlay function to ensure it doesn't raise errors.
    """
    try:
        sdss_vis_instance.ic_overlay()
        assert True
    except Exception:
        assert False
