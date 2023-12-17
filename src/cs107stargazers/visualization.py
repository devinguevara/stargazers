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
    def __init__(self, data):
        self.data = data

    def spectralplot(self):
        plt.figure(figsize=(10, 6))
        # Assuming 'wavelength' and 'flux' columns in the data
        plt.plot(self.data['wavelength'], self.data['flux'])
        plt.xlabel('Wavelength')
        plt.ylabel('Flux')
        plt.title('Spectral Plot')
        plt.show()

    def ic_overlay(self):
        plt.figure(figsize=(10, 6))
        # Plotting code for inferred continuum
        # For demonstration, assuming an 'inferred_continuum' column exists
        plt.plot(self.data['wavelength'], self.data['flux'], label='Spectral Data')
        plt.plot(self.data['wavelength'], self.data['inferred_continuum'], label='Inferred Continuum')
        plt.xlabel('Wavelength')
        plt.ylabel('Flux')
        plt.title('Spectral Plot with Inferred Continuum Overlay')
        plt.legend()
        plt.show()
