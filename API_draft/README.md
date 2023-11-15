# Specifications for SRS requirements 

* Modules
* Classes
* Functions

*Note: use `pandas` dataframes as data format for methods.*

## Modules, Classes and Functions

* Data Pre-Processing Module
  * `class Preprocessing` 
    * Method: `normalize()` : Normalize data
    * Method: `outlier_removal()` : Remove outliers from data
    * Method: `interpolation()` : Interpolate data
    * Method: `redshift_correlation()` # redshift data

* Metadata Extraction Module: 
  * `class MetadataExtraction`
    * Method: `get_attribute(attribute)` where attribute can be identifiers, coordinates, chemical abundances, redshifts, or other fields as requested by   
    * end-user : Return information on attribute provided as argument by user

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

### Modules from Annex B:

* MachineLearning Module
  * `class StarGalaxyQSOClassifier`
    *  Method: `fit()`: Train the model
    *  Method: `predict()`: Predict the classifications  
    *  Method: `predict_proba()`: Predict the classification probabilities

* Interactive Visualization Module:
  *  `class VisInteractive`
  *  Method: `plotregion(region)` : Plot region specified by user
  *  Method: `quantflux()` : Quantify the flux of spectral lines

# Task allocation among team members

* Devin: Data Pre-Processing Module 
* Elena: Data Augmentation Module
* Innocent: Metadata Extraction Module
* Ali: Wavelength Module
* Samia: Visualization Module 

* Together: 
  *  MachineLearning Module 
  *  Interactive Visualization Module 
