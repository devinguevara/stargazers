import sys
import os
import pytest
import numpy as np
import pandas as pd 
from astroquery.sdss import SDSS

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)
from cs107stargazers.spectrumalignment import SpectrumAlignment
from cs107stargazers.query import Query  

# Mock Query class for testing
class MockQuery:
    def get_df(self):
        # Create a mock DataFrame with 'flux' and 'loglam' columns
        return pd.DataFrame({'flux': [1.0, 2.0, 3.0], 'loglam': [3.0, 4.0, 5.0]})

@pytest.fixture
def mock_query():
    return MockQuery()

def test_common_range_creation(mock_query):
    # Create a SpectrumAlignment instance using the mocked Query class
    spectrum_alignment = SpectrumAlignment(mock_query)

    # Mock spectra data
    spectra_data = {
        'spectrum_1': {'wavelengths': np.array([400, 500, 600]), 'flux_values': np.array([0.5, 0.8, 1.2])},
        'spectrum_2': {'wavelengths': np.array([410, 520, 630]), 'flux_values': np.array([0.6, 0.9, 1.4])}
        # Add more spectra data as needed for testing
    }

    # Test the creation of a common range of wavelengths
    spectrum_alignment._create_common_range(spectra_data)
    assert isinstance(spectrum_alignment.common_range, np.ndarray)
    assert len(spectrum_alignment.common_range) > 0

def test_interpolate_spectrum(mock_query):
    # Create a SpectrumAlignment instance using the mocked Query class
    spectrum_alignment = SpectrumAlignment(mock_query)

    # Mock wavelengths and flux values
    wavelengths = np.array([400, 500, 600])
    flux_values = np.array([0.5, 0.8, 1.2])

    # Set a common range manually for testing
    spectrum_alignment.common_range = np.arange(400, 601)

    # Test spectrum interpolation
    aligned_flux_values = spectrum_alignment._interpolate_spectrum(wavelengths, flux_values)
    assert isinstance(aligned_flux_values, np.ndarray)
    assert len(aligned_flux_values) == len(spectrum_alignment.common_range)


