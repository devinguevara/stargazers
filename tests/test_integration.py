
import pandas as pd 
from astroquery.sdss import SDSS
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import StandardScaler
import numpy as np
import differint.differint as differint
import warnings
import sys
import os

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from cs107stargazers.ml_stargazer import Ml_stargazer
from cs107stargazers.augment import Augment 
from cs107stargazers.preprocessing import Preprocessing
from cs107stargazers.metadata_extraction import MetadataExtractor
from cs107stargazers.query import Query












def TestIntegration(): 
    sample_query = """
    SELECT
        TOP 10
        p.objID, p.ra, p.dec, p.u, p.g, p.r, p.i, p.z
    FROM
        PhotoObj AS p
    WHERE
        p.u BETWEEN 0 AND 19.6
    """ 
    #Using Query 
    query = Query(sample_query)
    df = query.get_df()

    #using preprocessing in order to normalize 
    pp = Preprocessing(df)
    df = pp.normalize()

    #using metadata extractor on the dataframe to get specific columns 
    md = MetadataExtractor(df)
    md = md.extract_metadata(['ra', 'dec'])

    #using augment 
    aug = Augment(df)
    df_deriv = aug.fractional_derive(0.5)


    #using ml_stargazer
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
        s.ra BETWEEN 150.0 AND 150.2
        AND s.dec BETWEEN 2.0 AND 2.2
    """

    # Use our query function to get a df of the data
    ml_query= Query(query)
    df = ml_query.get_df()

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")  # Ignore all warnings

        # Your code that triggers the warning
        ml_query = Query(query)
        df = ml_query.get_df()

        # go
        vars_predict = ["s.ra", "s.dec"]
        ml_object = Ml_stargazer(df, vars_predict)

        ml_object.fit()

        # predict where (STAR=1, GALAXY=2, QSO=3)
        test2 = ml_object.predict()
        test3 = ml_object.predict("df")

