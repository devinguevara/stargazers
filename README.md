[![Tests Workflow (Dev)](https://code.harvard.edu/CS107/team27_2023/actions/workflows/tests.yml/badge.svg?branch=dev)](https://code.harvard.edu/CS107/team27_2023/actions/workflows/tests.yml)
[![Coverage Workflow (Dev)](https://code.harvard.edu/CS107/team27_2023/actions/workflows/coverage.yml/badge.svg?branch=dev)](https://code.harvard.edu/CS107/team27_2023/actions/workflows/coverage.yml)

# cs107stargazers package & library

Package Name: `cs107stargazers`

Link to TestPyPI: https://test.pypi.org/project/cs107stargazers/

This is an astronomical research software library for the classification of celestial objects with Sloan Digital Sky Survey (SDSS) services & APIs. 
 
## Modules, Classes and Functions

* Data Pre-Processing Module
  * `class Preprocessing` 
    * Method: `normalize()` : Normalize data
    * Method: `outlier_removal()` : Remove outliers from data
    * Method: `interpolation()` : Interpolate data
    * Method: `redshift_correlation()` # redshift data

* Metadata Extraction Module: 
  * `class MetadataExtractor`
    * Method: `extract_specific_field(field_name)` where field_name can be identifiers, coordinates, chemical abundances, redshifts, or other fields as requested by end-user : Returns information on field_name provided as argument by user
    * Method: `extract_metadata(fields)` : Returns information on the list of fields provided as argument by user

* Alignment in Wavelength Module
  * `class Wavelength` 
    * Method: `align()` : Perform wavelength calibration

* Visualization Module
  * `class SDSSVis`
    * Method: `spectralplot()` : Plot spectral visualization
    * Method: `ic_overlay()` : Plot spectral visualization with inferred continuum overlay

* Data Augmentation Module
  * `class Augment`
    * Method: `derive()` : Compute derivatives and append them to the preprocessed spectra data
    * Method: `fractional_derive()` : Compute fractional derivatives and append them to the preprocessed spectra data

* MachineLearning Module
  * `class StarGalaxyQSOClassifier`
    *  Method: `fit()`: Train the model
    *  Method: `predict()`: Predict the classifications  
    *  Method: `predict_proba()`: Predict the classification probabilities

* Interactive Visualization Module:
  *  `class VisInteractive`
  *  Method: `plotregion(region)` : Plot region specified by user
  *  Method: `quantflux()` : Quantify the flux of spectral lines

## Installation and Usage

To install this package, run the following command in your terminal if you have python3 installed:

```
python3 -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ cs107stargazers
```

To use this package, you may import it's modules. Detailed documentaion can be found in the `docs` folder, inside the `html` folder. To access the documentation, open the `index.html` file in your browser.

Detailed demonstration of the package can be found on the dev branch in the `cs107stargazers_Samia_Elena_Devin_Ali_Innocent.ipynb` file in the `tutorial/`. A pdf version of this file is provided as well. ⚠️ Be sure to be in the `dev` branch to access the `tutorial` directory!
