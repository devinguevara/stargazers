# test files for ml_stargazer module

# test that it is a df given to initialize
# test that error is thrown when non-pandas is given
# test that I can fit a model with the variables given
# test that the df returns the number of columns it should--+1 for predict, + 3 for predict_prob (return them to string codes)
# check that id is a column name within the df, if provided (to exclude in later steps)

import numpy as np
import pandas as pd 
from astroquery.sdss import SDSS
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import StandardScaler

import pytest 
from unittest.mock import patch
from _pytest.monkeypatch import MonkeyPatch

import sys
import os

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from ml_stargazer import Ml_stargazer



def test_Ml_stargazer(): 

    # create dummy data for testing: example expected data from astroquery -- matches data in query() test scripts
    
    query = """
    SELECT TOP 100
        s.specobjid, s.ra, s.dec,
         s.z, s.zerr,
        s.plate, s.fiberID, s.mjd,
        p.petroMag_u, p.petroMag_g, p.petroMag_r, p.petroMag_i, p.petroMag_z
    FROM
        specObj AS s
    JOIN
        photoObj AS p ON s.bestobjid = p.objid
    WHERE
        s.ra BETWEEN 149.9 AND 150.1
        AND s.dec BETWEEN 1.9 AND 2.1
    """

    # Use astroquery to execute the query
    result = SDSS.query_sql(query)

    # Convert the result to a pandas DataFrame
    df = result.to_pandas()

    # go
    vars_predict = ["s.ra", "s.dec"]
    test1 = Ml_stargazer(df, vars_predict)

    test1.fit()
        
    # predict
    test2 = test1.predict()
    test3 = test1.predict("df")

    # predict_proba
    test4 = test1.predict_prob()
    test5 = test1.predict_prob("df")

    # assert types
    assert(isinstance(test2, np.ndarray))
    assert(isinstance(test4, np.ndarray))
    assert(isinstance(test3, pd.DataFrame))
    assert(isinstance(test5, pd.DataFrame))

    # assert dimensions
    assert(len(test2)==df.shape[0])
    assert(len(test4)==df.shape[0])
    
    assert(test3.shape[0]==df.shape[0])
    assert(test3.shape[1]==df.shape[1]+1)
   
    assert(test5.shape[0]==df.shape[0])
    assert(test5.shape[1]==df.shape[1]+3)

# assert that errors are raised

    