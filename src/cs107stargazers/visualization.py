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
