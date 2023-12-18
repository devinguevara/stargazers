"""
SDSS Database Query Module

This module is designed to facilitate querying the Sloan Digital Sky Survey (SDSS) database using
the Astronomical Data Query Language (ADQL). It provides a simple yet powerful interface for
astronomers and astrophysicists to retrieve astronomical data for analysis. The module leverages
the capabilities of the 'astroquery.sdss' library and Pandas to handle and manipulate the queried data.

The core of this module is the `Query` class, which allows users to execute ADQL queries and
retrieve results in various formats, including Pandas DataFrames and Astropy Tables. This class
handles the complexities of database connectivity and query execution, providing a user-friendly
interface for data retrieval.

Classes:
--------
Query : A class that encapsulates ADQL queries to the SDSS database. It provides methods to
        execute queries and retrieve results in different formats.

The module assumes that the user has basic knowledge of ADQL and the structure of the SDSS database.
It is intended for use in astronomical research and education, providing a straightforward way to
access one of the most comprehensive astronomical databases available.

Example:
--------
To use this module, simply import it along with the required 'astroquery.sdss' and 'pandas' libraries.
Create an instance of the Query class with your ADQL query, and use the provided methods to retrieve
and manipulate the data:

# Import the required libraries and this module.

# Example ADQL query
query_string = "SELECT TOP 10 * FROM specObj WHERE class = 'GALAXY'"

# Create a Query instance
query = Query(query_string)

# Retrieve the result as a Pandas DataFrame
data_frame = query.get_df()

# Alternatively, retrieve the result as an Astropy Table
astro_table = query.get_table()

# Or simply print the query result
query.print()

Dependencies:
-------------
- astroquery
- pandas
"""


import pandas as pd
from astroquery.sdss import SDSS


# alright create the query class
class Query:
    """
    A class for querying the Sloan Digital Sky Survey (SDSS) database using ADQL (Astronomical Data Query Language).

    This class provides methods to execute ADQL queries against the SDSS database and retrieve results
    in different formats such as pandas DataFrame, Astropy Table, or simply print the results.

    Attributes:
    -----------
    ADQL_string : str
        The ADQL query string to be executed against the SDSS database.

    Methods:
    --------
    get_df():
        Executes the ADQL query and returns the result as a pandas DataFrame.

    get_table():
        Executes the ADQL query and returns the result as an Astropy Table.

    print():
        Executes the ADQL query and prints the result.
    """

    def __init__(self, ADQL_string: str):
        """
        Initializes the Query object with the given ADQL query string.

        Parameters:
        -----------
        ADQL_string : str
            The ADQL query string to be used for querying the SDSS database.
        """
        self.ADQL_string = ADQL_string
        try:
            from astroquery.sdss import SDSS
            import pandas as pd

            self.SDSS = SDSS
            self.pandas = pd
        except ImportError:
            print("Please install the required libraries using:")
            print("pip install astroquery pandas")
            # You may exit the program or take appropriate action based on your use case
            exit(1)

    def get_df(self):
        """
        Executes the stored ADQL query and returns the results as a pandas DataFrame.

        Returns:
        --------
        pandas.DataFrame
            A DataFrame containing the query results.

        Raises:
        -------
        Exception
            If an error occurs during the query execution or data conversion.
        """
        try:
            # Query SDSS using the provided ADQL query
            result = SDSS.query_sql(self.ADQL_string)
            df = result.to_pandas()
            return df

        except Exception as e:
            print(f"An error occurred. Make sure you have a valid ADQL query.")

    def get_table(self):
        """
        Executes the stored ADQL query and returns the results as an Astropy Table.

        Returns:
        --------
        astropy.table.Table
            An Astropy Table containing the query results.

        Raises:
        -------
        Exception
            If an error occurs during the query execution.
        """
        try:
            # Query SDSS using the provided ADQL query
            result = SDSS.query_sql(self.ADQL_string)
            return result

        except Exception as e:
            print(f"An error occurred. Make sure you have a valid ADQL query.")

    def print(self):
        """
        Executes the stored ADQL query and prints the results.

        This method is useful for quick checks or debugging purposes.

        Raises:
        -------
        Exception
            If an error occurs during the query execution.
        """
        try:
            # Query SDSS using the provided ADQL query
            result = SDSS.query_sql(self.ADQL_string)
            print(result)

        except Exception as e:
            print(f"An error occurred. Make sure you have a valid ADQL query.")
