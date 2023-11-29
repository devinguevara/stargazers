import sys
import os
import pandas as pd
import pytest

# Add 'src' directory to the path for importing modules
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)
from cs107stargazers.metadata_extraction import MetadataExtractor


@pytest.fixture
def sample_data():
    """
    Fixture for creating sample data as a pandas DataFrame.

    Returns:
        pd.DataFrame: A DataFrame with sample data.
    """
    return pd.DataFrame(
        {"identifier": [1, 2, 3], "ra": [10.5, 20.5, 30.5], "dec": [15.5, 25.5, 35.5]}
    )


@pytest.fixture
def metadata_extractor(sample_data):
    """
    Fixture for creating a MetadataExtractor instance.

    Args:
        sample_data (pd.DataFrame): Sample data for the extractor.

    Returns:
        MetadataExtractor: An instance of MetadataExtractor.
    """
    return MetadataExtractor(sample_data)


def test_extract_metadata_success(metadata_extractor):
    """
    Test successful extraction of specified metadata columns.

    Args:
        metadata_extractor (MetadataExtractor): An instance of MetadataExtractor.
    """
    result = metadata_extractor.extract_metadata(["identifier", "ra"])
    assert result.columns.tolist() == ["identifier", "ra"]


def test_extract_metadata_missing_field(metadata_extractor):
    """
    Test extraction with a missing field, expecting a ValueError.

    Args:
        metadata_extractor (MetadataExtractor): An instance of MetadataExtractor.
    """
    with pytest.raises(ValueError):
        metadata_extractor.extract_metadata(["identifier", "unknown_field"])


def test_extract_specific_field_success(metadata_extractor, sample_data):
    """
    Test successful extraction of a specific field.

    Args:
        metadata_extractor (MetadataExtractor): An instance of MetadataExtractor.
        sample_data (pd.DataFrame): The sample data used for testing.
    """
    result = metadata_extractor.extract_specific_field("ra")
    assert result.equals(sample_data["ra"])


def test_extract_specific_field_not_found(metadata_extractor):
    """
    Test extraction of a non-existent field, expecting a ValueError.

    Args:
        metadata_extractor (MetadataExtractor): An instance of MetadataExtractor.
    """
    with pytest.raises(ValueError):
        metadata_extractor.extract_specific_field("unknown_field")
