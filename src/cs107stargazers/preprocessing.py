"""
Astronomical Data Preprocessing Module

This module provides a set of tools for preprocessing astronomical data, particularly from the Sloan Digital Sky Survey (SDSS). 
It includes the 'Preprocessing' class, which offers methods for data normalization, outlier removal, interpolation, 
and calculating redshift correlations. These methods are essential for preparing astronomical data for further analysis 
and research. The module relies on pandas, numpy, and scikit-learn libraries to perform various data manipulation tasks.

Classes:
--------
Preprocessing: A class for preprocessing astronomical data frames.

Dependencies:
-------------
- pandas
- numpy
- sklearn
"""


# import the proper libraries
import pandas as pd
from astroquery.sdss import SDSS
import numpy as np
from sklearn.neighbors import KNeighborsRegressor


# create the preprocessing class
class Preprocessing:
    # innit self class. Basically when initialized it should take in the data you want to process and then return what you want
    def __init__(self, data: pd.DataFrame):
        self.data = data

    # define normalize
    def normalize(self, replace=False):
        # for every column in self.data
        df = pd.DataFrame()
        for col in self.data.columns:
            type_col = self.data[col].dtype

            # normalize only numeric type columns that are not IDs
            if type_col in [int, float] and "ID" != col and "objID" != col:
                # calculate the max and the min values
                min = self.data[col].min()
                max = self.data[col].max()

                # replace the column with the new calculation of the values for that column
                df[col] = (self.data[col] - min) / (max - min)

            else:
                df[col] = self.data[col]

        # it would be cool if you can choose to replace your self.data instead of making a whole bunch of copies you know?
        if replace:
            self.data = df
        else:
            return df

    # define rm_outlier

    def rm_outlier(self, replace=False, threshold=2.5):
        # alright create your dummy df
        df = self.data.copy()
        # iterate through the columns
        for col in df:
            values = df[col]
            # calculate the z score for every entry in the column
            z_scores = np.abs((values - values.mean()) / values.std())

            # identify outliers in the column
            outliers = z_scores > threshold

            # drop outliers. This changes the df this thing is iterating through, meaning I don't have to worry about mismatched rows
            df = df.drop(df[outliers].index)

        # if replace is true then don't return just replace self.data
        if replace:
            self.data = df
        else:
            return df

    # define interpolation which is basically just making up why given x based on your already recorded data. Will be using k nearest neighbors
    def interpolate(
        self, x_to_interpolate: [], y_col: str, x_col: str, n_neighbors=3, replace=False
    ):
        df = self.data

        # CHECK IF ARGUMENTS ARE CORRECT
        if y_col not in df.columns or x_col not in df.columns:
            raise ValueError(f"Columns {y_col} or {x_col} not found in the DataFrame.")

        if not x_to_interpolate:
            raise ValueError(
                "You must put in x values to interpolate in the form of a list or array"
            )

        # make the x values and y values be in a format suitable for knn regressor model
        x_values = df[y_col].values
        y_values = df[x_col].values
        x_values_2d = x_values.reshape(-1, 1)
        y_values_2d = y_values.reshape(-1, 1)

        # reshape values to interpolate
        x_to_interpolate = np.array(x_to_interpolate).reshape(-1, 1)

        # create the regressor instance and then fit the model and then prdict
        knn_model = KNeighborsRegressor(n_neighbors=n_neighbors)
        knn_model.fit(x_values_2d, y_values_2d)
        y_interpolated = knn_model.predict(x_to_interpolate)

        # create dataframe object
        df_interpolate = pd.DataFrame(
            {
                f"{x_col}_x_interpolate": x_to_interpolate.flatten(),
                f"{y_col}_y_interpolated": y_interpolated.flatten(),
            }
        )

        if replace:
            self.data = pd.concat([df, df_interpolate], axis=1)
        else:
            return df_interpolate

    def get_redshift_corr(self, col: str):
        # check if the col is valid
        if not col or col not in self.data.columns:
            raise ValueError(
                """You need to make sure that the column you're putting in as an argument actually exists in the dataframe you initialized Preprocessing with"""
            )

        if "z" not in self.data.columns:
            raise ValueError("Make sure the redshift column 'z' is in self.data")

        return self.data[col].corr(self.data["z"])
