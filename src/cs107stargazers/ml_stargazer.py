import numpy as np
import pandas as pd 
from astroquery.sdss import SDSS
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import StandardScaler

# ML class for fit(), predict(), and predict_proba()
class Ml_stargazer(): 

    '''
    Classify celestial objects as star/galaxy/QSO. (Spectra are most commonly used, but this class allows for increased flexibility of model-building
    and prediction.) fit() fits the model to SDSS data using the variables indicated by the user to drive prediction. predict() produces classification 
    predictions for each objectID in the df (self.df, for an ml_stargazer instance.) predict_proba() provides the probability of each of the 3 classifications for 
    each objectid in the df. Functions wrap around scikit SGClassifier(). https://scikit-learn.org/stable/modules/sgd.html
    '''

    def __init__(self, df, fit_vars): 
        '''
        Initialize an instance of ml_stargazer class.
        A class instance requires a pandas dataframe (df) and the list of variable names to be used in the ML
        process of both model fitting and prediction (fit_vars). fit_vars must be formatted as a list of strings corresponding
        to the columns to the names of following SDSS query shorthand: "s.ra", not "ra"; "s.___" refers to variables to be retrieved 
        from specObj, while "p.___" refers to variables to be retrieved from photoObj. 
        predict() and predict_proba() provide classification predictions from the fitted SDG Classifier (stochastic gradient descent.)
        Results from these functions can be returned either as result arrays or appended to the initial df provided, i.e. an 
        augmented df.
        '''
        if isinstance(df, pd.DataFrame) is False:
            raise ValueError('Input must be a pandas dataframe')
        # make sure it is a pandas df --error handling
        self.data = df 
        # the vars that we will query, fit the ML model to, and use within our dataset for prediction. They must exist as columns in the df
        self.fit_vars = fit_vars 
        self.SDGClassifier = None
    
    def fit(self, ra=150, dec=2): 
        '''
        Fit the SDG Classifier model to labelled SDSS data. Model will be fit using as predictive variables the list indicated in 
        self.fit_vars. Optional arguments ra and dec allow user to specify the region from which they wish the 
        training points to be. STAR=1, GALAXY=2, OQS=3. Scikit documentation: https://scikit-learn.org/stable/modules/sgd.html
        '''

        ra = ra  
        dec = dec  

        # Query SDSS for spectroscopic data in the given region
        query_vars = ','.join(self.fit_vars)

        query = f"""
            SELECT TOP 100
                {query_vars}, s.class
            FROM
                specObj AS s
            JOIN
                photoObj AS p ON s.bestobjid = p.objid
            WHERE
                s.ra BETWEEN {ra-0.1} AND {ra+0.1}
                AND s.dec BETWEEN {dec-0.1} AND {dec+0.1}
        """

        # Use astroquery to execute the query
        result = SDSS.query_sql(query)

        # Convert the result to a pandas DataFrame
        df = result.to_pandas()

        # Stochastic Gradient Descent is sensitive to feature scaling, so it is highly recommended to scale your data.
        # same scaler for fitting and prediction, & for both training and applied data
        
        # fit for the variables provided by the user for prediction, i.e. those returned by the query
        X_train = df.drop("class", axis=1) # class is y, not x, i.e. outcome tag not predictor
        scaler = StandardScaler()
        scaler.fit(X_train)  # Don't cheat - fit only on training data
        X_train = scaler.transform(X_train)

        # train with SDGClassifier
        X = np.array(X_train)
        y = np.array(df["class"])
        # code categories numerically
        y[y == b'STAR'] = 1
        y[y == b'GALAXY'] = 2
        y[y == b'QSO'] = 3
        y = list(y)
        clf = SGDClassifier(loss="log_loss", penalty="l2", max_iter=1000)
        clf.fit(X, y)

        # save fitted ML model results in object
        self.SDGClassifier = clf
    
    def predict(self, output="array"): 
        '''
        Classify objectids in self.df into 3 groups (STAR=1, GALAXY=2, QSO=3) using the SDG Classifier model
        self.SDGClassifer (fit using ml_stargazer.fit()). Optional argument output allows user to specify whether
        they would like results in array or augmented df format (i.e. appending as columns to the data being analyzed.)
        '''

        # convert variable names from query names to column names corresponding to self.df
        fit_vrz = []
        for ii in self.fit_vars:
            jj = ii.split('.', 1)[-1]
            fit_vrz.append(jj)  
        
        # extract the variables that will be used in prediction by the model [those indicated by fit_vars--which were used to train the model on different data--reformatted]
        X_predict = self.data
        X_predict = X_predict[fit_vrz]

        # scale/standardize our predictors (to match fitting procedure)
        clf = self.SDGClassifier
        scaler = StandardScaler()
        scaler.fit(X_predict)  
        X_predict = scaler.transform(X_predict)
        
        # output classification (prediction) results as either the raw array output of an augmented df of self.df (column added)
        if output == "array":
            return clf.predict(X_predict)
        elif output == "df":
            result_col = pd.DataFrame(clf.predict(X_predict), columns=["predict"])
            return pd.concat([self.data, result_col], axis=1)
        # determine output type: array or augmented pd df
    
    # def confusion(self):
    #     # produce confusion matrix for fitted model

    def predict_prob(self, output="separate"): 
        '''
        Probabilistically classify objectids in self.df into 3 groups (STAR=1, GALAXY=2, QSO=3) using the SDG Classifier model
        self.SDGClassifer (fit using ml_stargazer.fit()); output gives the probability of being in group 1, 2, or 3 for each objectid.
        Optional argument output allows user to specify whether they would like results in array or augmented df format 
        (i.e. appending as columns to the data being analyzed.)
        '''
        
        # convert variable names from query names to column names corresponding to self.df
        fit_vrz = []
        for ii in self.fit_vars:
            jj = ii.split('.', 1)[-1]
            fit_vrz.append(jj)  
        
        # extract the variables that will be used in prediction by the model [those indicated by fit_vars--which were used to train the model on different data--reformatted]
        X_predict = self.data
        X_predict = X_predict[fit_vrz]

        # scale/standardize our predictors (to match fitting procedure)
        clf = self.SDGClassifier
        scaler = StandardScaler()
        scaler.fit(X_predict)  
        X_predict = scaler.transform(X_predict)

        # output classification (prediction) results as either the raw array output of an augmented df of self.df (columns added)
        if output == "separate":
            return clf.predict_proba(X_predict)
        elif output == "df":
            result_col = pd.DataFrame(clf.predict_proba(X_predict), columns=["p_STAR", "p_GALAXY", "p_QSO"])
            return pd.concat([self.data, result_col], axis=1)
       
       
 
       
       
       
       
# confusion matrix? this was not included in the SRS.
       

#          # determine output type: array or augmented pd df



# import matplotlib.pyplot as plt
# from sklearn.datasets import make_classification
# from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
# from sklearn.model_selection import train_test_split
# from sklearn.svm import SVC
# X, y = make_classification(random_state=0)
# X_train, X_test, y_train, y_test = train_test_split(X, y,
#                                                     random_state=0)

# clf = SVC(random_state=0)
# clf.fit(X_train, y_train)
# predictions = clf.predict(X_test)


# cm = confusion_matrix(y_test, predictions, labels=clf.classes_)

# X_train, X_test, y_train, y_test = train_test_split(X, y,
#                                                     random_state=0)
# confusion_matrix(y_test, test1.predict(), labels=test1.SDGClassifier.classes_) 

# disp = ConfusionMatrixDisplay(confusion_matrix=cm,
#                               display_labels=clf.classes_)
# disp.plot()
# plt.show()






#         try:
#             # Query SDSS using the provided ADQL query
#             result = SDSS.query_sql(self.ADQL_string)          
#             print(result)
        
#         except Exception as e:
#             print(f"An error occurred. Make sure you have a valid ADQL query.")



#             clf.predict_proba(X).shape      
#             len(clf.predict(X))
