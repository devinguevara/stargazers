
import pandas as pd 
from astroquery.sdss import SDSS
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import StandardScaler
import numpy as np
import differint.differint as differint
import warnings
import sys
import pytest
import os

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from cs107stargazers.ml_stargazer import Ml_stargazer
from cs107stargazers.augment import Augment 
from cs107stargazers.preprocessing import Preprocessing
from cs107stargazers.metadata_extraction import MetadataExtractor
from cs107stargazers.query import Query
from cs107stargazers.visualization import SDSSVis
from cs107stargazers.spectrumalignment import SpectrumAlignment


def TestIntegration(): 
        with pytest.raises(Exception): 
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

            
            #Okay doing visualization 
            df = pd.DataFrame({
                "wavelength": [412, 536, 615, 748, 811],
                "flux": [12, 25, 19, 23, 36],
                "inferred_continuum": [1, 2, 3, 4, 5]
            })

            vs = SDSSVis(df)
            vs.test_spectralplot()
                
            #doing spectrum
            df = pd.DataFrame({'flux': [1.0, 2.0, 3.0], 'loglam': [3.0, 4.0, 5.0]})
            sa = SpectrumAlignment(df)

            spectra_data = {
                'spectrum_1': {'wavelengths': np.array([400, 500, 600]), 'flux_values': np.array([0.5, 0.8, 1.2])},
                'spectrum_2': {'wavelengths': np.array([410, 520, 630]), 'flux_values': np.array([0.6, 0.9, 1.4])}
            }

            # Test the creation of a common range of wavelengths
            sa._create_common_range(spectra_data)

