import numpy as np
import pandas as pd 
from astroquery.sdss import SDSS
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import StandardScaler

# ML class for fit(), predict(), and predict_proba()
class ml_stargazer(): 

    def __init__(self, df, fit_vars): 
        '''
        '''

        # make sure it is a pandas df --error handling
        self.data = df 
        # the vars that we will query, fit the ML model to, and use within our dataset for prediction. They must exist as columns in the df
        self.fit_vars = fit_vars 
        self.SDGClassifier = None
    
    def fit(self, ra=150, dec=2): 
        '''
        '''
        # get data from SDSS, train model
        # Example coordinates for a specific region
        ra = ra  
        dec = dec  

        # Query SDSS for spectroscopic data in the given region

        # TESTING
        fit_vars = ["s.specobjid", "s.ra"]

        query_vars = ','.join(fit_vars)

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
        # fit for the variables provided by the user for prediction, i.e. the columns in self.data
        X_train = df.drop("class", axis=1)
        scaler = StandardScaler()
        scaler.fit(X_train)  # Don't cheat - fit only on training data
        X_train = scaler.transform(X_train)

        # train with SDGClassifier
        X = np.array(X_train)
        y = np.array(df["class"])
        y[y == b'STAR'] = 1
        y[y == b'GALAXY'] = 2
        y[y == b'QSO'] = 3
        y = list(y)
        clf = SGDClassifier(loss="log_loss", penalty="l2", max_iter=1000)
        clf.fit(X, y)
        clf.predict_proba(X).shape
        len(clf.predict(X))

        self.SDGClassifier = clf

    def confusion(self):
        # produce confusion matrix for fitted model
    
    def predict(self, output="array"): 

        clf = self.SDGClassifier
        # give an error if they try to give something of the wrong shape
        clf.predict(X)

        # determine output type: array or augmented pd df
        

    def predict_prob(self, output="array"): 
        
        clf = self.SDGClassifier
        clf.predict_proba(X).shape

         # determine output type: array or augmented pd df




        try:
            # Query SDSS using the provided ADQL query
            result = SDSS.query_sql(self.ADQL_string)          
            print(result)
        
        except Exception as e:
            print(f"An error occurred. Make sure you have a valid ADQL query.")