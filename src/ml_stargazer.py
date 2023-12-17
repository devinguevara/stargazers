import numpy as np
import pandas as pd 
from astroquery.sdss import SDSS
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import StandardScaler

# ML class for fit(), predict(), and predict_proba()
class ml_stargazer(): 

    '''
    '''

    def __init__(self, df, fit_vars): 
        '''
        A class instance requires a pandas dataframe (df) and a list of variables to be used in the ML
        process of both model fitting and prediction (fit_vars). fit_vars must be formatted as a list of strings corresponding
        to the columns of the dataframe (df) which the user wants to use for classification of object type. ** The strings should
        be formatted for an SDSS query. Ex: "s.ra", not "ra".
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
        # fit_vars = ["s.specobjid", "s.ra"]

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

        self.SDGClassifier = clf
    
    def predict(self, output="array"): 

        fit_vrz = []
        for ii in self.fit_vars:
            jj = ii.split('.', 1)[-1]
            fit_vrz.append(jj)  
        
        X_predict = self.data
        X_predict = X_predict[fit_vrz]

        clf = self.SDGClassifier
        scaler = StandardScaler()
        scaler.fit(X_predict)  # Don't cheat - fit only on training data
        X_predict = scaler.transform(X_predict)
        
        # give an error if they try to give something of the wrong shape
        if output == "array":
            return clf.predict(X_predict)
        elif output == "df":
            result_col = pd.DataFrame(clf.predict(X_predict), columns=["predict"])
            return pd.concat([self.data, result_col], axis=1)
        # determine output type: array or augmented pd df
    
    # def confusion(self):
    #     # produce confusion matrix for fitted model

    def predict_prob(self, output="separate"): 
        
        fit_vrz = []
        for ii in self.fit_vars:
            jj = ii.split('.', 1)[-1]
            fit_vrz.append(jj)  
        
        X_predict = self.data
        X_predict = X_predict[fit_vrz]

        clf = self.SDGClassifier
        scaler = StandardScaler()
        scaler.fit(X_predict)  # Don't cheat - fit only on training data
        X_predict = scaler.transform(X_predict)

        # give an error if they try to give something of the wrong shape
        if output == "separate":
            return clf.predict_proba(X_predict)
        elif output == "df":
            result_col = pd.DataFrame(clf.predict_proba(X_predict), columns=["p_STAR", "p_GALAXY", "p_QSO"])
            return pd.concat([self.data, result_col], axis=1)
       
       
       
query = """
    SELECT TOP 100
        s.specobjid, s.ra, s.dec,
         s.z, s.zerr,
        s.plate, s.fiberID, s.mjd,
        p.petroMag_u, p.petroMag_g, p.petroMag_r, p.petroMag_i, p.petroMag_z
    FROM
        specObj AS s
    JOIN
        photoObj AS p ON s.bestobjid = p.objid
    WHERE
        s.ra BETWEEN 149.9 AND 150.1
        AND s.dec BETWEEN 1.9 AND 2.1
"""

# Use astroquery to execute the query
result = SDSS.query_sql(query)

# Convert the result to a pandas DataFrame
df = result.to_pandas()

# go
test1 = ml_stargazer(df, ["s.ra", "s.dec"])

test1.fit()
       
# predict
test1.predict()
test1.predict("df")

# predict_proba
test1.predict_prob()
test1.predict_prob("df")
       
       
       
       




       
str_ = ['Mark: I am sending the file: abc.txt', "..3"]
print [for i in str_ str.split('.', 1)[-1]]
        [str.split('.', 1)[-1] for subl in str_]
       
       
       
       
       
       
       
       
       
        clf.predict_proba(X).shape

         # determine output type: array or augmented pd df



import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
X, y = make_classification(random_state=0)
X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    random_state=0)
clf = SVC(random_state=0)
clf.fit(X_train, y_train)
predictions = clf.predict(X_test)
cm = confusion_matrix(y_test, predictions, labels=clf.classes_)
disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                              display_labels=clf.classes_)
disp.plot()
plt.show()






        try:
            # Query SDSS using the provided ADQL query
            result = SDSS.query_sql(self.ADQL_string)          
            print(result)
        
        except Exception as e:
            print(f"An error occurred. Make sure you have a valid ADQL query.")



            clf.predict_proba(X).shape      
            len(clf.predict(X))
