"""
SDSS Spectral Visualization Module

This module provides tools for visualizing spectral data from the Sloan Digital Sky Survey (SDSS). 
It includes the SDSSVis class, which is designed to facilitate easy and efficient plotting of 
spectroscopic data. The module is built on top of the pandas and matplotlib libraries, leveraging 
their capabilities for data handling and visualization.

Classes:
--------
SDSSVis : A class designed for plotting SDSS spectroscopic data. It provides methods to plot 
spectral data and overlay inferred continuum data for comparative analysis.

The module expects data in the form of a pandas DataFrame with specific columns for wavelength, 
flux, and optionally, inferred continuum. It simplifies the process of creating insightful 
visualizations for the analysis of spectral data.

Dependencies:
-------------
- pandas
- matplotlib
"""


import pandas as pd
import matplotlib.pyplot as plt


class SDSSVis:
    """
    A class for visualizing spectroscopic data from the Sloan Digital Sky Survey (SDSS).

    This class provides functionalities to plot spectral data and overlay inferred
    continuum on the spectral plot. It is designed to work with a DataFrame that
    contains columns for wavelength, flux, and optionally, inferred continuum.

    Attributes:
    -----------
    data : pandas.DataFrame
        A DataFrame containing the spectroscopic data. Expected to have columns
        'wavelength', 'flux', and optionally 'inferred_continuum'.

    Methods:
    --------
    spectralplot():
        Plots a spectral graph using wavelength and flux data.

    ic_overlay():
        Plots a spectral graph with an overlay of the inferred continuum on the
        spectral data.
    """

    def __init__(self, data: pd.DataFrame):
        """
        Initializes the SDSSVis object with spectroscopic data.

        Parameters:
        -----------
        data : pandas.DataFrame
            A DataFrame containing spectroscopic data with at least 'wavelength'
            and 'flux' columns.
        """
        self.data = data

    def spectralplot(self):
        """
        Plots the spectral data on a graph.

        This method creates a plot using 'wavelength' as the x-axis and 'flux'
        as the y-axis. It displays the plot with appropriate labels and title.

        Requires:
        - The 'data' attribute must contain 'wavelength' and 'flux' columns.
        """
        plt.figure(figsize=(10, 6))
        # Assuming 'wavelength' and 'flux' columns in the data
        plt.plot(self.data["wavelength"], self.data["flux"])
        plt.xlabel("Wavelength")
        plt.ylabel("Flux")
        plt.title("Spectral Plot")
        plt.show()

    def ic_overlay(self):
        """
        Plots the spectral data with an overlay of the inferred continuum.

        This method creates a plot similar to spectralplot but with an additional
        line representing the inferred continuum (if available). It includes a legend
        to distinguish between the spectral data and the inferred continuum.

        Requires:
        - The 'data' attribute must contain 'wavelength', 'flux', and 'inferred_continuum' columns.
        """
        plt.figure(figsize=(10, 6))
        # Plotting code for inferred continuum
        # For demonstration, assuming an 'inferred_continuum' column exists
        plt.plot(self.data["wavelength"], self.data["flux"], label="Spectral Data")
        plt.plot(
            self.data["wavelength"],
            self.data["inferred_continuum"],
            label="Inferred Continuum",
        )
        plt.xlabel("Wavelength")
        plt.ylabel("Flux")
        plt.title("Spectral Plot with Inferred Continuum Overlay")
        plt.legend()
        plt.show()
