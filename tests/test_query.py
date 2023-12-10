
import sys
import os
import pytest
from io import StringIO
import pandas as pd 
from astroquery.sdss import SDSS
from astropy.table import Table

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)
from cs107stargazers.query import Query

#creating a fixture for the query so it can be used across tests 


sample_query = """
SELECT
    TOP 10
    p.objID, p.ra, p.dec, p.u, p.g, p.r, p.i, p.z
FROM
    PhotoObj AS p
WHERE
    p.u BETWEEN 0 AND 19.6
""" 
@pytest.fixture
def query_fixture(): 
    return Query(sample_query)



def test_get_dataframe(query_fixture): 
    df = query_fixture.get_df()
    assert(isinstance(df, pd.DataFrame))


def test_get_table(query_fixture): 
    table = query_fixture.get_table()
    assert(isinstance(table, Table))

def test_print(query_fixture, capsys): 
    query_fixture.print()
    stdout = capsys.readouterr()
    assert(stdout != None)


