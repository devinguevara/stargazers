import numpy as np

## NOTE: Operating under the assumption that 'spectra_data' is a dictionary with a given key being a spectrum and 
## the corresponding value being a dictionary holding wavelengths and flux values for that spectrum

"""
The goal of this class is to align the spectra because they contain different wavelengths and thus cannot be compared directly.
By creating a common range of wavelengths and using interpolation to calculate corresponding flux values, this class aims to
make it such that the different spectra are 'aligned' and therefore comparable.
"""

class SpectrumAlignment:
    def _init_(self):
        self.common_range = None

    def _create_common_range(self, spectra_data):
        # Find the minimum and maximum wavelengths across all spectra so we can create a standardized range
        all_wavelengths = np.concatenate([data['wavelengths'] for data in spectra_data.values()])
        min_wavelength = np.min(all_wavelengths)
        max_wavelength = np.max(all_wavelengths)
        
        # Create a common range of wavelengths spanning the minimum to maximum
        self.common_range = np.arange(min_wavelength, max_wavelength + 1)

    def _interpolate_spectrum(self, wavelengths, flux_values):
        # Interpolate flux values onto the common wavelength range for a single spectrum 
        aligned_flux_values = np.interp(self.common_range, wavelengths, flux_values)
        return aligned_flux_values

    def align_wavelengths(self, spectra_data):
        # Create a common range of wavelengths across all spectra
        self._create_common_range(spectra_data)

        # Initialize the dictionary that will be returned
        aligned_spectra = {}
        for spectrum, data in spectra_data.items():
            # Extract wavelengths and flux values for each spectrum
            wavelengths = data['wavelengths']
            flux_values = data['flux_values']
            
            # Interpolate flux values onto the common wavelength range for each spectrum
            aligned_flux_values = self._interpolate_spectrum(wavelengths, flux_values)
            
            # Store aligned spectra data in a dictionary
            aligned_spectra[spectrum] = {
                'wavelengths': self.common_range,
                'aligned_flux_values': aligned_flux_values
            }
        
        return aligned_spectra