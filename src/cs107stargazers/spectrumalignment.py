import numpy as np
from query.py import Query

class SpectrumAlignment:
    def __init__(self, query_obj):
        self.query = query_obj
        self.common_range = None

    def _create_common_range(self, spectra_data):
        try:
            # Find the minimum and maximum wavelengths across all spectra to create a standardized range
            all_wavelengths = np.concatenate([data['wavelengths'] for data in spectra_data.values()])
            min_wavelength = np.min(all_wavelengths)
            max_wavelength = np.max(all_wavelengths)

            # Create a common range of wavelengths spanning the minimum to maximum
            self.common_range = np.arange(min_wavelength, max_wavelength + 1)
        except Exception as e:
            print(f"An error occurred while creating the common range: {e}")

    def _interpolate_spectrum(self, wavelengths, flux_values):
        try:
            # Interpolate flux values onto the common wavelength range for a single spectrum
            aligned_flux_values = np.interp(self.common_range, wavelengths, flux_values)
            return aligned_flux_values
        except Exception as e:
            print(f"An error occurred while interpolating spectrum: {e}")

    def align_wavelengths(self, spectra_data):
        try:
            # Create a common range of wavelengths across all spectra
            self._create_common_range(spectra_data)

            # Initialize the dictionary that will be returned
            aligned_spectra = {}
            for spectrum, data in spectra_data.items():
                try:
                    # Get the data frame using the Query object's get_df method
                    result_df = self.query.get_df()

                    # Extract flux and log(wavelength) columns from the result dataframe
                    flux = result_df['flux']
                    log_wavelength = result_df['loglam']
                    wavelengths = 10 ** log_wavelength  # Convert log(wavelength) to wavelength

                    # Interpolate flux values onto the common wavelength range for each spectrum
                    aligned_flux_values = self._interpolate_spectrum(wavelengths, flux)

                    # Store aligned spectra data in a dictionary
                    aligned_spectra[spectrum] = {
                        'wavelengths': self.common_range,
                        'aligned_flux_values': aligned_flux_values
                    }
                except Exception as e:
                    print(f"An error occurred for spectrum {spectrum}: {e}")

            return aligned_spectra
        except Exception as e:
            print(f"An error occurred while aligning wavelengths: {e}")
