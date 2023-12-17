"""A module to extract metadata."""

import pandas as pd


class MetadataExtractor:
    """Metadata Extractor."""

    def __init__(self, data: pd.DataFrame):
        """Initializes the MetadataExtractor with the provided dataset.

        Args:
            data (pd.DataFrame): A pandas DataFrame containing astronomical data.
        """
        self.data = data

    def extract_metadata(self, fields: list) -> pd.DataFrame:
        """Extracts specified metadata fields from the dataset.

        Args:
            fields (list): A list of strings representing the metadata fields to extract.

        Raises:
            ValueError: When any of the fields is missing in the data.

        Returns:
            pd.DataFrame: A DataFrame containing the extracted metadata.
        """
        missing_fields = [field for field in fields if field not in self.data.columns]
        if missing_fields:
            raise ValueError(f"Missing fields in data: {missing_fields}")

        extracted_metadata = self.data[fields]
        return extracted_metadata

    def extract_specific_field(self, field_name: str) -> pd.Series:
        """Extracts a specific metadata field from the dataset.

        Args:
            field_name (str): The name of the field to extract.

        Raises:
            ValueError: When a field is missing in the data.

        Returns:
            pd.Series: A Series containing the values of the specified field.
        """
        if field_name not in self.data.columns:
            raise ValueError(f"Field '{field_name}' not found in data.")

        return self.data[field_name]
