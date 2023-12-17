"""
The `augment` module is designed for time series analysis, specifically focusing on the computation of derivatives and fractional derivatives (differintegrals) of time series data. It primarily consists of the Augment class, which offers encapsulated functions for these computations on Pandas DataFrames.

Key Features:
- Compute standard time series derivatives using the `derive` method of the Augment class.
- Compute fractional derivatives (differintegrals) using the `fractional_derive` method.
- Flexible handling of data columns, allowing selective computation of derivatives on specific subsets of the data.

Note:
- The module assumes the input data is pre-processed and formatted as a Pandas DataFrame.
- The accuracy of derivative computations may be affected by incomplete or missing data in the DataFrame.

Dependencies:
- numpy
- pandas
- differint
"""


# required / dependency
import numpy as np
import pandas as pd
import differint.differint as differint


class Augment:  # accept a processed pd dataframe
    """
    The Augment class provides methods for computing time series derivatives and fractional derivatives.

    This class is designed to work with time series data represented in a Pandas DataFrame. It includes methods to compute
    both standard and fractional derivatives (differintegrals) of the data. The expected input for creating an instance
    of this class is a DataFrame with each column representing a time series for a specific variable. Rows should correspond
    to different time points or indices. The class offers two main methods: `derive` and `fractional_derive`.

    Methods:
        derive: Computes the standard derivative of the time series. Optional parameters allow for the selection of specific
                columns for which the derivative should be computed.
        fractional_derive: Computes the fractional derivative (differintegral) of the time series. Requires the order of
                           the differintegral to be specified. Optional parameters include column selection and domain settings
                           for the differintegral computation.

    Note:
        This class assumes the input DataFrame is pre-processed and ready for derivative computations. Missing data in the
        DataFrame may affect the ability of the methods to accurately compute derivatives.

    Parameters:
        df_p (pandas.DataFrame): A pre-processed DataFrame where each column represents a time series of a variable.
    """

    def __init__(self, df_p):
        """
        Initializes the Augment class with a DataFrame.

        Parameters:
            df_p (pandas.DataFrame): The DataFrame to be used for derivative calculations. Each column should represent a time series of a variable.

        Raises:
            ValueError: If the input is not a Pandas DataFrame.
        """

        if isinstance(df_p, pd.DataFrame) is False:
            raise ValueError("Input must be a pandas dataframe")
        self.data = df_p  # ** assumes pd df, NOT numpy array

    def derive(self, run=None, notrun=None):
        """
        Computes the derivative of time series data in the DataFrame.

        Parameters:
            run (list of str, optional): Column names for which the derivative is to be computed. If None, derivatives for all columns are computed.
            notrun (list of str, optional): Column names for which the derivative should not be computed. Ignored if 'run' is specified.

        Returns:
            pandas.DataFrame: A DataFrame including original columns and their corresponding derivative columns.
        """

        df = self.data

        # in case not all derivates are desired: drop those not desired
        if run is not None:
            df = pd.DataFrame(
                df[run]
            )  # run = list of column names for which to perform this
        if notrun is not None:
            df = df.drop(notrun, axis="columns")

        # convert df to numpy array & apply np.gradient
        if (
            df.shape[1] == 1
        ):  # np.gradient acts up for the single column case, needs to be formatted like this
            df_ = np.array(df.iloc[:, 0])
            grad = np.gradient(df_)
        else:
            df_ = df.to_numpy(dtype=float)
            grad = np.gradient(
                df_, axis=1
            )  # default for varargs: assumes unitary increase

        # provide interpretable colnames for output derivative columns
        der_names = "d_" + df.columns  # naming for derivative columns
        der_names = der_names.values.tolist()
        der = pd.DataFrame(grad, columns=der_names)

        # concatenate i.e. augment pd df in self.data with derivatives & return pd df
        df_aug = pd.concat([self.data, der], ignore_index=False, axis=1)
        return df_aug

    def fractional_derive(
        self, frac, run=None, notrun=None, domain_start=0, domain_end=1
    ):
        """
        Computes the fractional derivative (differintegral) of time series data in the DataFrame.

        Parameters:
            frac (float): The order of the differintegral to be computed.
            run (list of str, optional): Column names for which the differintegral is to be computed. If None, differintegrals for all columns are computed.
            notrun (list of str, optional): Column names for which the differintegral should not be computed. Ignored if 'run' is specified.
            domain_start (numeric, optional): The start of the domain for the differintegral computation.
            domain_end (numeric, optional): The end of the domain for the differintegral computation.

        Returns:
            pandas.DataFrame: A DataFrame including original columns and their corresponding differintegral columns.
        """

        df = self.data

        # in case not all derivates are desired: drop those not desired
        if run is not None:
            df = pd.DataFrame(
                df[run]
            )  # run = list of column names for which to perform this
        if notrun is not None:
            df = df.drop(notrun, axis="columns")

        # provide interpretable colnames for output derivative columns
        der_names = "d_" + df.columns  # naming for derivative columns
        der_names = der_names.values.tolist()

        # calculate the fractional derivatives for each column
        # differint can only act on 1d arrays: iterate through all columns in df
        diffint_list = []
        for col_ii in range(df.shape[1]):
            diffint_col = differint.GLI(
                frac,
                df.iloc[:, col_ii],
                num_points=df.shape[0],
                domain_start=domain_start,
                domain_end=domain_end,
            )
            diffint_list.append(diffint_col)

        # return a df where each column corresponds to the fractional derivative, in order, of the columns in df
        der = pd.DataFrame(diffint_list).transpose()
        der.columns = der_names

        # concatenate i.e. augment pd df in self.data with derivatives & return pd df
        df_aug = pd.concat([self.data, der], ignore_index=False, axis=1)
        return df_aug
