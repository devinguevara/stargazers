
#alright make the correct imports 
import numpy as np
import pandas as pd
import differint.differint as differint
import pytest 
from unittest.mock import patch
from _pytest.monkeypatch import MonkeyPatch
import sys
import os


sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)
from augment import Augment 

import sys
import os

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)
from augment import Augment


def test_Augment(): 

    # create dummy data for testing: example expected data from astroquery -- matches data in query() test scripts
    
    mat = np.array([[ 1237678537416376475,  3.19855107e+02,  8.71000795e+00,
         1.83503300e+01,  1.71328500e+01,  1.66692300e+01,
         1.65660400e+01,  1.64049300e+01],
       [ 1237679321774096394,  3.99012821e+00, -6.11657840e+00,
         1.85970200e+01,  1.74749000e+01,  1.70798700e+01,
         1.69242200e+01,  1.68813200e+01],
       [ 1237679321774293108,  4.47609981e+00, -6.12668453e+00,
         1.90394200e+01,  1.83047200e+01,  1.79339100e+01,
         1.78231900e+01,  1.77951600e+01],
       [ 1237679321774293159,  4.57646000e+00, -6.07174663e+00,
         1.94511000e+01,  1.75309500e+01,  1.68065500e+01,
         1.65082700e+01,  1.63422400e+01],
       [ 1237679321776914474,  1.04572498e+01, -6.06263879e+00,
         1.81803600e+01,  1.61385500e+01,  1.53076900e+01,
         1.49969800e+01,  1.48096500e+01],
       [ 1237679321777242131,  1.13042357e+01, -6.22087296e+00,
         1.92381000e+01,  1.80435600e+01,  1.75163300e+01,
         1.73182200e+01,  1.72555000e+01],
       [ 1237679321777373209,  1.15677943e+01, -6.06065235e+00,
         1.86935600e+01,  1.74812300e+01,  1.70313800e+01,
         1.68757500e+01,  1.68162800e+01],
       [ 1237679321778683924,  1.45942689e+01, -6.01012145e+00,
         1.84718700e+01,  1.71846700e+01,  1.67297400e+01,
         1.65735300e+01,  1.65056000e+01],
       [ 1237679321779339268,  1.60360178e+01, -5.95854593e+00,
         1.76051900e+01,  1.64301900e+01,  1.59924300e+01,
         1.58010900e+01,  1.57542300e+01],
       [ 1237679321780715603,  1.92787644e+01, -5.90305902e+00,
         1.88168200e+01,  1.77291400e+01,  1.73524300e+01,
         1.72127300e+01,  1.71453500e+01]])
    
    df = pd.DataFrame(mat, columns=["objID", "ra", "dec", "u", "g", "r", "i", "z"])

    # Test class instantiation and data attribute
    test1 = Augment(df)
    assert(isinstance(test1.data, pd.DataFrame))
    # check to see that it an error happens if the wrong kind of argument is taken
    with pytest.raises(ValueError):
        test = Augment([1, 2, 3])

    # Test derive()
    # all columns (vars)
    test2 = test1.derive()
    # confirm type of object returned (pd df)
    assert(isinstance(test2, pd.DataFrame))
    # confirm correct number of rows (unchanged) & columns (doubled)
    assert(test2.shape[0] == df.shape[0])
    assert(test2.shape[1] == 2*df.shape[1])
    # confirm that columnames are as expected
    assert(test2.columns.values.tolist()[0:8] == df.columns.values.tolist())
    expected_names = "d_" + df.columns
    expected_names = expected_names.values.tolist()
    assert(test2.columns[8:16].values.tolist() == expected_names)
    # confirm that an individual column set of values are as expected
    assert(test2.iloc[3,10] == pd.DataFrame(np.gradient(df, axis=1)).iloc[3,2])  # indexing is same row, col + 8 for test2 bc of augmented format

    # notrun
    test3 = test1.derive(notrun="objID")
    # confirm type of object returned (pd df)
    assert(isinstance(test3, pd.DataFrame))
    # confirm correct number of columns
    assert(test3.shape[0] == df.shape[0])
    assert(test3.shape[1] == 2*df.shape[1]-1) # one less col [than double]
    # confirm that columnames are as expected
    assert("d_objID" not in test3.columns.values.tolist())
    # confirm that an individual column set of values are as expected
    assert(test3.iloc[3,14] == pd.DataFrame(np.gradient(df, axis=1)).iloc[3,7])  

    # run
    test4 = test1.derive(run="ra")
    # confirm type of object returned (pd df)
    assert(isinstance(test4, pd.DataFrame))
    # confirm correct number of columns
    assert(test4.shape[0] == df.shape[0])
    assert(test4.shape[1] == df.shape[1]+1) # one more col
    # confirm that columnames are as expected
    assert("d_ra"  in test4.columns.values.tolist())
    # confirm that an individual column set of values are as expected
    assert(test4.iloc[3,8] == np.gradient(df["ra"])[3])    # note: np.gradient returns diff results depending on whether you call the function on a df or a 1D array. Not clear why.

    # Test fractional_derive()
    # all columns (vars)
    test5 = test1.fractional_derive(0.5)
    # confirm type of object returned (pd df)
    assert(isinstance(test5, pd.DataFrame))
    # confirm correct number of columns
    assert(test5.shape[0] == df.shape[0])
    assert(test5.shape[1] == 2*df.shape[1])
    # confirm that columnames are as expected
    assert(test5.columns.values.tolist()[0:8] == df.columns.values.tolist())
    expected_names = "d_" + df.columns
    expected_names = expected_names.values.tolist()
    assert(test5.columns[8:16].values.tolist() == expected_names)
    # confirm that an individual column set of values are as expected
    assert(test5["d_dec"][8] == differint.GLI(0.5, df["dec"], num_points=df.shape[0])[8])

    # notrun
    test6 = test1.fractional_derive(0.5, notrun="objID")
    # confirm type of object returned (pd df)
    assert(isinstance(test6, pd.DataFrame))
    # confirm correct number of columns
    assert(test6.shape[0] == df.shape[0])
    assert(test6.shape[1] == 2*df.shape[1]-1) # one less col [than doubled]
    # confirm that columnames are as expected
    assert("d_objID" not in test6.columns.values.tolist())
    # confirm that an individual column set of values are as expected
    assert(test6["d_dec"][8] == differint.GLI(0.5, df["dec"], num_points=df.shape[0])[8])

    # run
    test7 = test1.fractional_derive(0.5, run="ra")
    # confirm type of object returned (pd df)
    assert(isinstance(test7, pd.DataFrame))
    # confirm correct number of columns
    assert(test7.shape[0] == df.shape[0])
    assert(test7.shape[1] == df.shape[1]+1) # one more col
    # confirm that columnames are as expected
    assert("d_ra"  in test7.columns.values.tolist())
    # confirm that an individual column set of values are as expected
    assert(test6["d_ra"][8] == differint.GLI(0.5, df["ra"], num_points=df.shape[0])[8])

    
